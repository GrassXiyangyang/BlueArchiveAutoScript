import json
import sys

from modules.baas import baas, home


def get_config(self):
    if len(sys.argv) < 2:
        return 'baas.json'
    return sys.argv[1]


def config_path(self):
    return './configs/{0}'.format(get_config(self))


def load_ba_config(self):
    with open(config_path(self), 'r', encoding='utf-8') as f:
        data = json.load(f)
    self.bc = data


def save_ba_config(self):
    with open(config_path(self), 'w', encoding='utf-8') as f:
        f.write(json.dumps(self.bc, indent=4, ensure_ascii=False))


load_map = {
    'baas': baas.load_data,
    'home': home.load_data,
}
save_map = {
    'baas': baas.save_config,
    'home': home.save_config
}
