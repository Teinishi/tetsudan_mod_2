import argparse
import glob
import os
import subprocess
from lib.load_env import load_env

env = load_env()


def blender_export(pattern: str | None):
    dirname = os.path.dirname(__file__)
    blender_dir = os.path.join(dirname, "blender")

    pattern = pattern or "*.blend"
    for filename in glob.glob(pattern, root_dir=blender_dir):
        if os.path.splitext(filename)[1] != ".blend":
            continue
        # /blender 内の .blend と .py のペアを探し、Blender をバックグラウンドで起動してスクリプトを実行
        blend_path = os.path.join(blender_dir, filename)
        py_path = os.path.splitext(blend_path)[0] + ".py"
        if not os.path.exists(py_path):
            py_path = os.path.join(blender_dir, "default.py")

        cmd = f'"%BLENDER_PATH%" --background "{blend_path}" --python "{py_path}"'
        r = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True, encoding="utf-8", env=env)

        if r.stderr is not None and len(r.stderr.strip()) > 0:
            print(f"[{filename}]")
            print(r.stderr)
            if "Traceback (most recent call last):" in r.stderr:
                print(f"Blender script failed!")
                return

    print("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", type=str)
    args = parser.parse_args()
    blender_export(args.pattern)
