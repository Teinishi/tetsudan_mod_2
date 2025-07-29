import sys
import os
from .bail import bail

REQUIRED_ENV_KEYS = [
    "BLENDER_PATH",
    "MESH_COMPILER_PATH",
    "COMPONENT_MOD_COMPILER_PATH"
]

env_path = os.path.join(os.path.dirname(__file__), "../.env")


def load_env():
    if not os.path.isfile(env_path):
        bail(".env ファイルがありません。.env.sample を参考に、各々の環境に合わせて設定してください。")

    env = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            key, value = line.split("=", maxsplit=1)
            value = value.strip()
            if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
            env[key.strip()] = value

    for key in REQUIRED_ENV_KEYS:
        if key not in env:
            bail(f".env ファイルに {key} の項目が不足しています。")

    return env
