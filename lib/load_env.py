def load_env(env_path):
    env = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            key, value = line.split("=", maxsplit=1)
            env[key.strip()] = value.strip()
    return env
