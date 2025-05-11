import os

import yaml


def load_config():
    path = os.path.join(os.path.dirname(__file__), "../../etc/config.yml")
    with open(path, "r") as f:
        return yaml.safe_load(f)
