import argparse
import os
import glob
import shutil
import subprocess
import json
import re
import xml.etree.ElementTree as ET
from lib.bail import bail
from lib.clear_directory import clear_directory
from lib.load_env import load_env
from lib.malformed_xml import fix_malformed_attributes

FILENAME_PREFIX = "m_tns_tetsudan_"
NAME_PREFIX = "(M)(TNS) "
REQUIRED_TAGS = ["mod", "tetsudan", "train"]

env = load_env()


def is_vanilla_asset(name):
    return os.path.isfile(os.path.join(env["STORMWORKS_ROM_PATH"], name))


def compile_mesh(target, output_dir):
    # mesh_compiler を呼び出す
    if not os.path.isfile(target):
        bail(f"{os.path.basename(target)} がありません")
    cmd = f'"%MESH_COMPILER_PATH%" "{target}" -o "{output_dir}" -s'
    subprocess.run(cmd, shell=True, check=True, env=env)


def scan_xml(filename, xml):
    meshes = []
    lua_filename = None

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
            if not mesh.startswith(FILENAME_PREFIX) and not is_vanilla_asset(mesh):
                bail(
                    f'{filename} の {attr_name} が "{FILENAME_PREFIX}" で始まっていません')
            meshes.append(mesh)

    # Lua のチェック
    if int(root.attrib.get("type")) == 66:
        lua_filename = root.attrib.get("lua_filename")

    return (meshes, lua_filename)


def scan_lua(filename, lua):
    if not filename.startswith(FILENAME_PREFIX):
        bail(f'{filename} のファイル名が "{FILENAME_PREFIX}" で始まっていません')

    pattern = re.compile(
        "--\\s*include\\s+sfx\\s+([0-9]+)\\s+(\"([^\"]*)\"|'([^\']*)')\\s*$", flags=re.MULTILINE)
    include_sfx = {int(m[0]): m[2] or m[3] for m in pattern.findall(lua)}
    sfx_files = []
    if len(include_sfx) > 0:
        for i in range(max(include_sfx.keys()) + 1):
            sfx = include_sfx.get(i, None)
            if sfx is None:
                bail(f"{filename} の include sfx {i} が抜けています")
            if not is_vanilla_asset(sfx) and not sfx.startswith(FILENAME_PREFIX):
                bail(f'{sfx} のファイル名が "{FILENAME_PREFIX}" で始まっていません。')
            sfx_files.append(sfx)
    return sfx_files


def compile_component_bin(paths, filename, xml, lua_prefix=None):
    tmp_dir = os.path.join(paths["tmp"], filename)
    dae_dir = paths["dae"]
    lua_dir = paths["lua"]
    audio_dir = paths["audio"]
    dist_components_dir = paths["dist_components"]

    meshes, lua_filename = scan_xml(filename, xml)

    # 一時ファイルを作成
    os.makedirs(tmp_dir, exist_ok=True)
    with open(os.path.join(tmp_dir, filename), "w", encoding="utf-8") as f:
        f.write(xml)

    # meshをコンパイル
    for mesh in meshes:
        if not os.path.isfile(os.path.join(tmp_dir, mesh)) and not is_vanilla_asset(mesh):
            mesh_name = os.path.splitext(mesh)[0]
            compile_mesh(
                os.path.join(dae_dir, mesh_name) + ".dae",
                tmp_dir
            )
    assets = [mesh for mesh in meshes if not is_vanilla_asset(mesh)]

    if lua_filename is not None:
        lua_src_path = os.path.join(lua_dir, lua_filename)
        if not os.path.isfile(lua_src_path):
            bail(f"{lua_filename} がありません")

        with open(lua_src_path, "r", encoding="utf-8") as f:
            lua = f.read()
            if lua_prefix is not None:
                lua = lua_prefix + lua

            # Lua に書かれている音声ファイルを追加
            sfx_files = scan_lua(lua_filename, lua)
            for sfx in sfx_files:
                if is_vanilla_asset(sfx):
                    continue
                sfx_path = os.path.join(audio_dir, sfx)
                if not os.path.isfile(sfx_path):
                    bail(f"{sfx_path} がありません")
                shutil.copy(sfx_path, os.path.join(tmp_dir, sfx))
                assets.append(sfx)

            # Luaをコピー
            with open(os.path.join(tmp_dir, lua_filename), "w", encoding="utf-8") as fw:
                fw.write(lua)

        assets.append(lua_filename)

    # component_mod_compiler を呼び出す
    cmd = f'"%COMPONENT_MOD_COMPILER_PATH%" {filename} -s'
    for item in assets:
        cmd += f" {item}"
    subprocess.run(cmd, shell=True, check=True, env=env, cwd=tmp_dir)

    xml_name = os.path.splitext(filename)[0]
    bin_filename = xml_name + ".bin"

    # /dist/data/components にコピー
    os.makedirs(dist_components_dir, exist_ok=True)
    shutil.copy(
        os.path.join(tmp_dir, bin_filename),
        os.path.join(dist_components_dir, bin_filename)
    )


def compile_components(definition_pattern=None):
    # 一時ファイルを作成して component_mod_compiler を呼び出す
    dirname = os.path.dirname(__file__)
    paths = {
        "definitions": os.path.join(dirname, "definitions"),
        "dae": os.path.join(dirname, "blender", "exported"),
        "audio": os.path.join(dirname, "audio"),
        "lua": os.path.join(dirname, "lua"),
        "tmp": os.path.join(dirname, ".tmp"),
        "dist_components": os.path.join(dirname, "dist", "data", "components")
    }

    # dist/data/components を削除
    clear_directory(paths["dist_components"])
    # 一時ファイルを削除
    clear_directory(paths["tmp"])

    definition_pattern = definition_pattern or "*"
    for filename in glob.glob(definition_pattern, root_dir=paths["definitions"]):
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext == ".xml":
            # definitions/*.xml をコンパイル
            xml_path = os.path.join(paths["definitions"], filename)
            with open(xml_path, "r", encoding="utf-8") as f:
                compile_component_bin(paths, filename, f.read())
        elif ext == ".py":
            # definitions/*.py を実行してXMLを生成させる
            py_filepath = os.path.join(paths["definitions"], filename)
            proc = subprocess.run(
                ["python", py_filepath],
                stdout=subprocess.PIPE,
                text=True
            )
            data = json.loads(proc.stdout)
            for (xml_filename, definition) in data.items():
                if isinstance(definition, dict) and "xml" in definition:
                    # 追加オプションがある場合
                    compile_component_bin(
                        paths,
                        xml_filename,
                        definition["xml"],
                        lua_prefix=definition.get("luaPrefix")
                    )
                elif type(definition) is str:
                    # 文字列ベタ書きの場合
                    compile_component_bin(paths, xml_filename, definition)
                else:
                    bail(f"{filename} の {xml_filename} が処理できません")
        else:
            print(f"WARNING: .xml でも .py でもない {filename} は処理されません")

    # mod フォルダの data/components を置き換える
    mod_path = env.get("MOD_PATH")
    if mod_path is not None:
        mod_components_dir = os.path.join(mod_path, "data", "components")
        if not os.path.isdir(mod_path):
            bail(f'Mod フォルダがありません。"{mod_path}"')
        os.makedirs(mod_components_dir, exist_ok=True)
        shutil.rmtree(mod_components_dir)
        shutil.copytree(paths["dist_components"], mod_components_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", type=str)
    args = parser.parse_args()
    compile_components(args.pattern)
