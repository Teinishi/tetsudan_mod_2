import os
import glob
import shutil
import subprocess
import json
import xml.etree.ElementTree as ET
from lib.bail import bail
from lib.clear_directory import clear_directory
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


def scan_xml(filename, xml):
    meshes = []

    if not filename.startswith(FILENAME_PREFIX):
        bail(f'{filename} のファイル名が "{FILENAME_PREFIX}" で始まっていません')

    xml = fix_malformed_attributes(xml)
    root = ET.fromstring(xml)

    # パーツ名の警告
    if not root.attrib["name"].startswith(NAME_PREFIX):
        bail(f'{filename} のパーツ名が "{NAME_PREFIX}" で始まっていません')

    # タグの警告
    tags = [t.strip() for t in root.attrib["tags"].split(",")]
    for tag in REQUIRED_TAGS:
        if not tag in tags:
            bail(f'{filename} のタグが "{tag}" を含んでいません')

    # mesh の列挙
    for attr_name in ["mesh_data_name", "mesh_0_name", "mesh_1_name", "mesh_2_name", "mesh_editor_only_name"]:
        mesh = root.attrib.get(attr_name, None)
        if mesh is not None and mesh != "":
            if not mesh.startswith(FILENAME_PREFIX):
                bail(
                    f'{filename} の {attr_name} が "{FILENAME_PREFIX}" で始まっていません')
            meshes.append(mesh)

    return meshes


def create_tmp_files(tmp_dir, dae_dir, meshes, filename, xml):
    # 一時ファイルを作成
    os.makedirs(tmp_dir, exist_ok=True)
    with open(os.path.join(tmp_dir, filename), "w", encoding="utf-8") as f:
        f.write(xml)

    # meshをコンパイル
    for mesh in meshes:
        if not os.path.isfile(os.path.join(tmp_dir, mesh)):
            mesh_name = os.path.splitext(mesh)[0]
            compile_mesh(
                os.path.join(dae_dir, mesh_name) + ".dae",
                tmp_dir
            )


def compile_component_bin(tmp_dir, dae_dir, dist_components_dir, filename, xml):
    meshes = scan_xml(filename, xml)
    create_tmp_files(tmp_dir, dae_dir, meshes, filename, xml)

    assets = meshes

    # component_mod_compiler を呼び出す
    cmd = f'"%COMPONENT_MOD_COMPILER_PATH%" {filename} -s'
    for mesh in assets:
        cmd += f" {mesh}"
    subprocess.run(cmd, shell=True, check=True, env=env, cwd=tmp_dir)

    xml_name = os.path.splitext(filename)[0]
    bin_filename = xml_name + ".bin"

    # /dist/data/components にコピー
    os.makedirs(dist_components_dir, exist_ok=True)
    shutil.copy(
        os.path.join(tmp_dir, bin_filename),
        os.path.join(dist_components_dir, bin_filename)
    )


def compile_components():
    # 一時ファイルを作成して component_mod_compiler を呼び出す
    dirname = os.path.dirname(__file__)
    definitions_dir = os.path.join(dirname, "definitions")
    dae_dir = os.path.join(dirname, "blender", "exported")
    tmp_dir = os.path.join(dirname, ".tmp")
    dist_components_dir = os.path.join(dirname, "dist", "data", "components")

    # dist/data/components を削除
    clear_directory(dist_components_dir)
    # 一時ファイルを削除
    clear_directory(tmp_dir)

    for xml_filename in glob.glob("*.xml", root_dir=definitions_dir):
        # definitions/*.xml をコンパイル
        xml_path = os.path.join(definitions_dir, xml_filename)
        with open(xml_path, "r", encoding="utf-8") as f:
            compile_component_bin(
                tmp_dir, dae_dir, dist_components_dir, xml_filename, f.read())

    for py_filename in glob.glob("*.py", root_dir=definitions_dir):
        # definitions/*.py を実行してXMLを生成させる
        py_filepath = os.path.join(definitions_dir, py_filename)
        proc = subprocess.run(
            ["python", py_filepath],
            stdout=subprocess.PIPE,
            text=True
        )
        data = json.loads(proc.stdout)
        for (xml_filename, xml) in data.items():
            compile_component_bin(
                tmp_dir, dae_dir, dist_components_dir, xml_filename, xml)

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
