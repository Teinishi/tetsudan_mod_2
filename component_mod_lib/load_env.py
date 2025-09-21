from pathlib import Path

REQUIRED_ENV_KEYS = [
    "BLENDER_PATH",
    "MESH_COMPILER_PATH",
    "COMPONENT_MOD_COMPILER_PATH"
]

env_file = Path.cwd().joinpath(".env")


def load_env():
    env = {}
    with env_file.open("r", encoding="utf-8") as f:
        for line in f.readlines():
            key, value = line.split("=", maxsplit=1)
            value = value.strip()
            if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
            env[key.strip()] = value

    for key in REQUIRED_ENV_KEYS:
        if key not in env:
            raise KeyError(f'.env file missing key "{key}"')

    return env
