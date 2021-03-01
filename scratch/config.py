from yaml import safe_load

with open('config.yml') as f:
    load_configs = safe_load(f)
