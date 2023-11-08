import json


def config_path(con):
    return './configs/{0}.json'.format(con)


def load_ba_config(con):
    with open(config_path(con), 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def save_ba_config(con, data):
    with open(config_path(con), 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
