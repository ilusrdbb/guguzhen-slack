import os

import yaml


def read():
    config_data = []
    config_dir = "./config"
    for filename in os.listdir(config_dir):
        if filename.endswith(".yaml"):
            with open(os.path.join(config_dir, filename), 'r', encoding='utf-8') as f:
                config_data.append(yaml.safe_load(f))
    return config_data