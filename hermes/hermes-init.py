import yaml, os, subprocess

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

with open(config_path, 'w') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

if not os.path.exists('/mnt/hermes_cli/__init__.py'):
    print('copying hermes source to shared volume...')
    subprocess.run(['cp', '-a', '/opt/hermes/.', '/mnt/'], check=True)
    print('copy done')

with open('/mnt/bin/zsh', 'w') as f:
    f.write('#!/bin/bash\nexec bash -i\n')
os.chmod('/mnt/bin/zsh', 0o755)
print('init done')
