#!/usr/bin/env bash
set -euo pipefail

export HOME=/opt/data
HERMES_UID="${HERMES_UID:-10010}"

usermod -u "$HERMES_UID" -d /opt/data hermes 2>/dev/null || true
chown -R "$HERMES_UID:$HERMES_UID" /opt/data

echo "==> Configuring memory provider: holographic"
hermes config set memory.provider holographic
hermes config set plugins.hermes-memory-store.auto_extract true
hermes config set plugins.hermes-memory-store.default_trust 0.7

echo "==> Preparing Claude Code OAuth token store"
# Agent runs as hermes with HOME=/opt/data and cannot traverse /root (700).
# If root has a token (from `claude auth login` as root), copy it to hermes home.
if [ -f /root/.claude.json ]; then
  cp /root/.claude.json "$HOME/.claude.json"
elif [ ! -f "$HOME/.claude.json" ]; then
  touch "$HOME/.claude.json"
fi
chmod 644 "$HOME/.claude.json"

echo "==> Symlinking Claude auth token into Hermes terminal home"
mkdir -p /opt/data/home
ln -sf /opt/data/.claude.json /opt/data/home/.claude.json

echo "==> Putting claude CLI on PATH for agent terminal sessions"
grep -q "hermes-shared/bin" "$HOME/.profile" 2>/dev/null || echo 'export PATH="/opt/hermes-shared/bin:$PATH"' >> "$HOME/.profile"

echo "==> Installing Claude Code skill on all profiles"
SKILL_URL="https://raw.githubusercontent.com/NousResearch/hermes-agent/main/skills/autonomous-ai-agents/claude-code/SKILL.md"
SKILL_MD=$(curl -fsSL "$SKILL_URL")
for profile in default coder tester reviewer architect orchestrator tech-writer pm; do
  SKILL_DIR="/opt/data/profiles/$profile/skills/claude-code"
  mkdir -p "$SKILL_DIR"
  echo "$SKILL_MD" > "$SKILL_DIR/SKILL.md"
  echo "    -> $profile: written"
done

echo "==> Configuring daily backup cron (VPS)"
SCRIPTS_DIR="${HERMES_HOME:-$HOME/.hermes}/scripts"
mkdir -p "$SCRIPTS_DIR"
printf '#!/usr/bin/env bash\nexport GIT_SSH_COMMAND="ssh -F $HOME/.ssh/config -o IdentitiesOnly=yes -i $HOME/.ssh/id_ed25519"\nbash <(curl -fsSL https://raw.githubusercontent.com/mcadac/open-vault/main/hermes/hermes-backup.sh)\n' > "$SCRIPTS_DIR/hermes-backup.sh"
chmod +x "$SCRIPTS_DIR/hermes-backup.sh"
hermes cron create "0 3 * * *" \
  --name "Daily Hermes backup" \
  --script hermes-backup.sh \
  --no-agent 2>/dev/null || true

echo "==> Fixing ownership of files written outside the hermes binary"
chown -R "$HERMES_UID:$HERMES_UID" /opt/data
echo "==> Done."
