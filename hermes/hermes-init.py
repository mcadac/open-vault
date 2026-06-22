import yaml, glob, os, subprocess, urllib.request

data_dir = '/opt/data'
config_path = data_dir + '/config.yaml'

nous_key = os.environ.get('NOUS_API_KEY', '')
model_patch = {
    'provider': 'custom',
    'base_url': 'https://inference-api.nousresearch.com/v1',
    'default': 'anthropic/claude-sonnet-4.6',
}
if nous_key:
    model_patch['api_key'] = nous_key

os.makedirs(data_dir, exist_ok=True)
if os.path.exists(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f) or {}
    print('patched config.yaml: model.provider=custom (nous inference)')
else:
    config = {}
    print('created initial config.yaml with nous provider')

config.setdefault('model', {}).update(model_patch)

session_token = os.environ.get('HERMES_DASHBOARD_SESSION_TOKEN', '')
if session_token:
    try:
        from plugins.dashboard_auth.basic import hash_password
        config.setdefault('dashboard_auth', {})['basic'] = {
            'username': 'hermes',
            'password_hash': hash_password(session_token),
        }
        print('configured dashboard basic auth from session token')
    except Exception as e:
        print(f'warn: dashboard auth setup failed: {e}')
else:
    print('warn: HERMES_DASHBOARD_SESSION_TOKEN not set — dashboard auth not configured')

with open(config_path, 'w') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

patched = 0
for p in glob.glob(data_dir + '/profiles/*/config.yaml'):
    with open(p) as f:
        pc = yaml.safe_load(f) or {}
    changed = False
    if pc.get('platforms', {}).get('api_server', {}).get('enabled') is not False:
        pc.setdefault('platforms', {})['api_server'] = {'enabled': False}
        changed = True
    if pc.get('platforms', {}).get('discord', {}).get('enabled') is not False:
        pc.setdefault('platforms', {})['discord'] = {'enabled': False}
        changed = True
    if changed:
        with open(p, 'w') as f:
            yaml.dump(pc, f, default_flow_style=False, allow_unicode=True)
        patched += 1
if patched:
    print('patched ' + str(patched) + ' profile config(s): api_server+discord disabled')

PROFILES_BASE = 'https://raw.githubusercontent.com/mcadac/open-vault/main/hermes/profiles'
PROFILES = ['orchestrator', 'pm', 'architect', 'coder', 'reviewer', 'tester', 'tech-writer']

def _fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.read().decode('utf-8')
    except Exception as e:
        print(f'warn: fetch failed {url}: {e}')
        return None

def _fetch_write(url, path):
    content = _fetch(url)
    if content is not None:
        with open(path, 'w') as f:
            f.write(content)
        return True
    return False

installed = 0
for profile in PROFILES:
    profile_dir = f'{data_dir}/profiles/{profile}'
    os.makedirs(profile_dir, exist_ok=True)

    for fname in ['config.yaml', 'SOUL.md']:
        _fetch_write(f'{PROFILES_BASE}/{profile}/{fname}', f'{profile_dir}/{fname}')

    skills_list = _fetch(f'{PROFILES_BASE}/{profile}/skills-list.txt')
    if skills_list:
        skill_count = 0
        for skill in skills_list.splitlines():
            skill = skill.strip()
            if not skill:
                continue
            skill_dir = f'{profile_dir}/skills/{skill}'
            os.makedirs(skill_dir, exist_ok=True)
            if _fetch_write(f'{PROFILES_BASE}/{profile}/skills/{skill}/SKILL.md', f'{skill_dir}/SKILL.md'):
                skill_count += 1
        print(f'  {profile}: {skill_count} skill(s) installed')

    installed += 1
print(f'installed {installed} profiles from open-vault')

if not os.path.exists('/mnt/hermes_cli/__init__.py'):
    print('copying hermes source to shared volume...')
    subprocess.run(['cp', '-a', '/opt/hermes/.', '/mnt/'], check=True)
    print('copy done')

with open('/mnt/bin/zsh', 'w') as f:
    f.write('#!/bin/bash\nexec bash -i\n')
os.chmod('/mnt/bin/zsh', 0o755)
print('init done')
