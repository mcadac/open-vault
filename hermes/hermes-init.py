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

if not os.path.exists(config_path):
    os.makedirs(data_dir, exist_ok=True)
    with open(config_path, 'w') as f:
        yaml.dump({'model': model_patch}, f)
    print('created initial config.yaml with nous provider')
else:
    with open(config_path) as f:
        config = yaml.safe_load(f) or {}
    config.setdefault('model', {}).update(model_patch)
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    print('patched config.yaml: model.provider=custom (nous inference)')

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

installed = 0
for profile in PROFILES:
    profile_dir = f'{data_dir}/profiles/{profile}'
    os.makedirs(profile_dir, exist_ok=True)
    for fname in ['config.yaml', 'SOUL.md']:
        url = f'{PROFILES_BASE}/{profile}/{fname}'
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                content = resp.read().decode('utf-8')
            with open(f'{profile_dir}/{fname}', 'w') as f:
                f.write(content)
        except Exception as e:
            print(f'warn: failed to fetch {profile}/{fname}: {e}')
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
