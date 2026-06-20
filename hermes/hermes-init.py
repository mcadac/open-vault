import yaml, glob, os, subprocess

data_dir = '/opt/data'
config_path = data_dir + '/config.yaml'

if not os.path.exists(config_path):
    os.makedirs(data_dir, exist_ok=True)
    with open(config_path, 'w') as f:
        yaml.dump({'model': {'default': 'anthropic/claude-opus-4.6', 'provider': 'openrouter'}}, f)
    print('created initial config.yaml with openrouter provider')
else:
    with open(config_path) as f:
        config = yaml.safe_load(f) or {}
    config.setdefault('model', {})['provider'] = 'openrouter'
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    print('patched config.yaml: model.provider=openrouter')

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

if not os.path.exists('/mnt/hermes_cli/__init__.py'):
    print('copying hermes source to shared volume...')
    subprocess.run(['cp', '-a', '/opt/hermes/.', '/mnt/'], check=True)
    print('copy done')

with open('/mnt/bin/zsh', 'w') as f:
    f.write('#!/bin/bash\nexec bash -i\n')
os.chmod('/mnt/bin/zsh', 0o755)
print('init done')
