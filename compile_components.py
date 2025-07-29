import sys
import os
import glob
import shutil
import subprocess
import xml.etree.ElementTree as ET
from lib.bail import bail
from lib.load_env import load_env
from lib.malformed_xml import fix_malformed_attributes

FILENAME_PREFIX = "m_tns_"
NAME_PREFIX = "(M)(TNS) "
REQUIRED_TAGS = ["mod", "tetsudan", "train"]

env = load_env()


def compile_mesh(target, output_dir):
    # mesh_compiler を呼び出す
    if not os.path.isfile(target):
        bail(f"{os.path.basename(target)} がありません")
    cmd = f'"%MESH_COMPILER_PATH%" "{target}" -o "{output_dir}" -s'
    subprocess.run(cmd, shell=True, check=True, env=env)


def compile_components():
    # 一時ファイルを作成して component_mod_compiler を呼び出す
    dirname = os.path.dirname(__file__)
    definitions_dir = os.path.join(dirname, "definitions")
    dae_dir = os.path.join(dirname, "blender", "exported")
    tmp_dir = os.path.join(dirname, ".tmp")
    dist_components_dir = os.path.join(dirname, "dist", "data", "components")

    # dist/data/components を削除
    shutil.rmtree(dist_components_dir)

    compiled_assets = set()

    for xml_filename in glob.glob("*.xml", root_dir=definitions_dir):
        if not xml_filename.startswith(FILENAME_PREFIX):
            bail(f'{xml_filename} のファイル名が "{FILENAME_PREFIX}" で始まっていません')

        xml_path = os.path.join(definitions_dir, xml_filename)

        meshes = []

        with open(xml_path, "r", encoding="utf-8") as f:
            content = fix_malformed_attributes(f.read())
            root = ET.fromstring(content)

            # パーツ名の警告
            if not root.attrib["name"].startswith(NAME_PREFIX):
                bail(f'{xml_filename} のパーツ名が "{NAME_PREFIX}" で始まっていません')

            # タグの警告
            tags = [t.strip() for t in root.attrib["tags"].split(",")]
            for tag in REQUIRED_TAGS:
                if not tag in tags:
                    bail(f'{xml_filename} のタグが "{tag}" を含んでいません')

            # mesh の列挙
            for attr_name in ["mesh_data_name", "mesh0_name", "mesh1_name", "mesh2_name", "mesh_editor_only_name"]:
                mesh = root.attrib.get(attr_name, None)
                if mesh is not None and mesh != "":
                    if not mesh.startswith(FILENAME_PREFIX):
                        bail(
                            f'{xml_filename} の {attr_name} が "{FILENAME_PREFIX}" で始まっていません')
                    meshes.append(mesh)

        # 一時ファイルを作成
        xml_name = os.path.splitext(xml_filename)[0]
        os.makedirs(tmp_dir, exist_ok=True)
        shutil.copy(xml_path, os.path.join(tmp_dir, xml_filename))

        # meshをコンパイル
        for mesh in meshes:
            mesh_name = os.path.splitext(mesh)[0]
            if mesh_name not in compiled_assets:
                compile_mesh(
                    os.path.join(dae_dir, mesh_name) + ".dae",
                    tmp_dir
                )
                compiled_assets.add(mesh_name)

        # component_mod_compiler を呼び出す
        cmd = f'"%COMPONENT_MOD_COMPILER_PATH%" {xml_filename} -s'
        for mesh in meshes:
            cmd += f" {mesh}"
        subprocess.run(cmd, shell=True, check=True, env=env, cwd=tmp_dir)

        bin_filename = xml_name + ".bin"

        # /dist/data/components にコピー
        os.makedirs(dist_components_dir, exist_ok=True)
        shutil.copy(
            os.path.join(tmp_dir, bin_filename),
            os.path.join(dist_components_dir, bin_filename)
        )

    # mod フォルダの data/components を置き換える
    mod_path = env.get("MOD_PATH")
    if mod_path is not None:
        mod_components_dir = os.path.join(mod_path, "data", "components")
        if not os.path.isdir(mod_path):
            bail(f'Mod フォルダがありません。"{mod_path}"')
        os.makedirs(mod_components_dir, exist_ok=True)
        shutil.rmtree(mod_components_dir)
        shutil.copytree(dist_components_dir, mod_components_dir)


if __name__ == "__main__":
    compile_components()
