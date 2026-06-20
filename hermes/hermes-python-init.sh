#!/bin/bash
set -e

if [ ! -f /opt/hermes/.venv313/bin/hermes ]; then
  echo "installing uv..."
  pip install uv --quiet
  export UV_PYTHON_INSTALL_DIR=/opt/hermes/.python313
  echo "downloading standalone Python 3.13 into volume..."
  uv python install 3.13
  echo "creating hermes venv313..."
  uv venv /opt/hermes/.venv313 --python 3.13
  echo "installing hermes from source (downloading deps)..."
  uv pip install --python /opt/hermes/.venv313 -e /opt/hermes --quiet
  echo "installing tmux and runtime libs into shared volume..."
  apt-get update -q && apt-get install -y --no-install-recommends tmux
  cp /usr/bin/tmux /opt/hermes/bin/tmux
  mkdir -p /opt/hermes/lib
  find /usr/lib -name "libevent_core-2.1*" -exec cp -P {} /opt/hermes/lib/ \;
  find /usr/lib -name "libutempter*" -exec cp -P {} /opt/hermes/lib/ \;
  echo "venv installed"
fi

if [ ! -f /opt/hermes/bin/gh ]; then
  echo "installing gh CLI..."
  apt-get update -q && apt-get install -y --no-install-recommends curl gpg
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    | gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
  chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    > /etc/apt/sources.list.d/github-cli.list
  apt-get update -q && apt-get install -y --no-install-recommends gh
  cp /usr/bin/gh /opt/hermes/bin/gh
  echo "gh installed"
fi

echo "done"
