import glob
import os
import subprocess
from lib.load_env import load_env


def blender_export():
    env = load_env()
    for blend in glob.glob("blender/*.blend"):
        # /blender 内の .blend と .py のペアを探し、Blender をバックグラウンドで起動してスクリプトを実行
        py = os.path.splitext(blend)[0] + ".py"
        if not os.path.exists(py):
            continue
        cmd = f'"%BLENDER_PATH%" --background "{blend}" --python "{py}"'
        subprocess.run(cmd, shell=True, check=True, env=env)


if __name__ == "__main__":
    blender_export()
