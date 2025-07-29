import glob
import os
import subprocess
from lib.load_env import load_env

env = load_env()


def blender_export():
    dirname = os.path.dirname(__file__)
    blender_dir = os.path.join(dirname, "blender")

    for blend_filename in glob.glob("*.blend", root_dir=blender_dir):
        # /blender 内の .blend と .py のペアを探し、Blender をバックグラウンドで起動してスクリプトを実行
        blend_path = os.path.join(blender_dir, blend_filename)
        py_path = os.path.splitext(blend_path)[0] + ".py"
        if not os.path.exists(py_path):
            py_path = os.path.join(blender_dir, "default.py")

        cmd = f'"%BLENDER_PATH%" --background "{blend_path}" --python "{py_path}"'
        subprocess.run(cmd, shell=True, check=True, env=env)


if __name__ == "__main__":
    blender_export()
