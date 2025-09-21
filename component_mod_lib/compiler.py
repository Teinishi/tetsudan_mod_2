from pathlib import Path
import re
import json
from dataclasses import dataclass, field
import importlib.util
import time
import xml.etree.ElementTree as ET
import os
import shutil
import subprocess
from component_mod_lib.malformed_xml import fix_malformed_attributes
from component_mod_lib.load_env import load_env

env = load_env()


_include_sfx_pattern = re.compile(
    "--\\s*include\\s+sfx\\s+(?P<index>[0-9]+)\\s+(\"(?P<filename1>[^\"]*)\"|'(?P<filename2>[^\']*)')\\s*$", flags=re.MULTILINE)


def _default_path(path: Path | str | None, default: str, root_path: Path) -> Path:
    if isinstance(path, Path):
        return path
    elif type(path) is str:
        return root_path.joinpath(path)
    else:
        return root_path.joinpath(default)


def _is_vanilla_asset(name: str) -> bool:
    return Path(env["STORMWORKS_ROM_PATH"]).joinpath(name).is_file()


def _export_blend_file(blend_file: Path, py_file: Path):
    # blender.exe を実行
    result = subprocess.run(
        f'"%BLENDER_PATH%" --background "{blend_file}" --python "{py_file}"',
        shell=True, check=True, capture_output=True, text=True, encoding="utf-8", env=env
    )
    if result.stderr is not None and len(result.stderr.strip()) > 0:
        raise RuntimeError(
            f'{result.stderr}\nBlender script execution failed: "{blend_file}"')


def _compile_mesh(dae_file: Path, output_dir: Path):
    # mesh_compiler を呼び出す
    subprocess.run(
        f'"%MESH_COMPILER_PATH%" "{dae_file}" -o "{output_dir}" -s',
        shell=True, check=True, env=env
    )


@dataclass
class DefinitionDependencies:
    mesh_names: list[str] = field(default_factory=list)
    lua_name: str | None = None
    sfx_names: list[str] = field(default_factory=list)

    def assets(self) -> list[str]:
        assets = self.sfx_names + self.mesh_names
        if self.lua_name is not None:
            assets.append(self.lua_name)
        return assets


class DependencyCache:
    _last_mesh_compile: float | None
    _last_definition_compile: float | None
    _meshes_data: dict[str, str]
    _definitions_data: dict

    def __init__(self):
        self._last_mesh_compile = None
        self._last_definition_compile = None
        self._meshes_data = {}
        self._definitions_data = {}

    def open(self, filepath: Path):
        if not filepath.is_file():
            return
        with filepath.open("r", encoding="utf-8") as f:
            data = json.load(f)
            self._last_mesh_compile = data["last_compile"]["mesh"]
            self._last_definition_compile = data["last_compile"]["definition"]
            self._meshes_data = data["meshes"]
            self._definitions_data = data["definitions"]

    def save(self, filepath: Path, mesh_time: float, definition_time: float):
        with filepath.open("w", encoding="utf-8") as f:
            json.dump({
                "last_compile": {
                    "mesh": mesh_time,
                    "definition": definition_time
                },
                "meshes": self._meshes_data,
                "definitions": self._definitions_data,
            }, f)

    def newer_than_last_mesh_compile(self, path: Path) -> bool:
        if self._last_mesh_compile is None:
            return True
        return path.stat().st_mtime > self._last_mesh_compile

    def newer_than_last_definition_compile(self, path: Path) -> bool:
        if self._last_definition_compile is None:
            return True
        return path.stat().st_mtime > self._last_definition_compile

    def add_mesh(self, name: str, blend_name: str):
        self._meshes_data[name] = blend_name

    def get_mesh_blend_name(self, name: str) -> str:
        if name not in self._meshes_data:
            raise KeyError(f'Unknown mesh file "{name}"')
        return self._meshes_data[name]

    def remove_blend_name(self, blend_name: str):
        keys_to_remove = [
            k for k, v in self._meshes_data.items() if v == blend_name]
        for k in keys_to_remove:
            del self._meshes_data[k]

    def add_definition(self, name: str, dependency: DefinitionDependencies):
        self._definitions_data[name] = {
            "mesh": dependency.mesh_names,
            "lua": dependency.lua_name,
            "sfx": dependency.sfx_names
        }

    def get_definition(self, name: str) -> None | DefinitionDependencies:
        if name not in self._definitions_data:
            return None
        d = self._definitions_data[name]
        return DefinitionDependencies(
            mesh_names=d.get("mesh", []),
            lua_name=d.get("lua", None),
            sfx_names=d.get("sfx", [])
        )


class Compiler:
    _root_path: Path
    _definitions_path: Path
    _blender_path: Path
    _dae_path: Path
    _meshes_path: Path
    _audio_path: Path
    _lua_path: Path
    _tmp_path: Path
    _dist_path: Path
    _filename_prefix: str | None
    _name_prefix: str | None
    _required_tags: str | None
    _dependency_cache: DependencyCache

    def __init__(
        self,
        root: Path | None = None,
        definitions_path: Path | str | None = None,
        blender_path: Path | str | None = None,
        dae_path: Path | str | None = None,
        audio_path: Path | str | None = None,
        lua_path: Path | str | None = None,
        cache_path: Path | str | None = None,
        dist_path: Path | str | None = None,
        filename_prefix: str | None = None,
        name_prefix: str | None = None,
        required_tags: list[str] | None = None
    ):
        root = root or Path.cwd()
        self._root_path = root
        self._definitions_path = _default_path(
            definitions_path, "definitions", root)
        self._blender_path = _default_path(blender_path, "blender", root)
        self._dae_path = _default_path(
            dae_path, "exported", self._blender_path)
        self._audio_path = _default_path(audio_path, "audio", root)
        self._lua_path = _default_path(lua_path, "lua", root)
        self._tmp_path = _default_path(cache_path, ".compiler", root)
        self._dist_path = _default_path(
            dist_path, "dist/data/components", root)
        self._meshes_path = self._tmp_path.joinpath("meshes")

        self._filename_prefix = filename_prefix
        self._name_prefix = name_prefix
        self._required_tags = required_tags

        self._dependency_cache = DependencyCache()

    def _check_filename_prefix(self, filename: Path | str):
        if isinstance(filename, Path):
            filename = filename.name
        if self._filename_prefix is not None and not filename.startswith(self._filename_prefix):
            raise ValueError(
                f'File name does not start with "{self._filename_prefix}": {filename}')

    def compile(self, sync_mod_folder: bool = False):
        cache_file = self._tmp_path.joinpath("cache.json")
        compile_path = self._tmp_path.joinpath("compile")
        self._dependency_cache.open(cache_file)
        known_definitions: set[str] = set()
        compiled: set[str] = set()

        mesh_compile_start_time = time.time()
        self.export_meshes()

        definition_compile_start_time = time.time()
        # .xml 形式の定義ファイル
        for file in self._definitions_path.glob("*.xml"):
            if not file.is_file():
                continue

            name = file.with_suffix("").name
            with file.open("r", encoding="utf-8") as f:
                try:
                    bin_file = self.compile_definition(
                        {"xml": f.read()}, name, file, compile_path)
                except Exception as e:
                    raise RuntimeError(
                        f'{e}:\n    At definition file "{file}"') from e
            known_definitions.add(name)
            if bin_file is not None:
                compiled.add(name)

        # .py 形式の定義ファイル
        for file in self._definitions_path.glob("*.py"):
            if not file.is_file():
                continue

            relative_path = file.relative_to(self._root_path)
            module_name = ".".join(relative_path.with_suffix("").parts)
            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if not hasattr(module, "definitions"):
                raise AttributeError(
                    f'"definitions" does not exist in module: "{file}"')
            if not isinstance(module.definitions, dict):
                raise TypeError(
                    f'Attribute "definitions" is not dict in module: "{file}"')

            for name, data in module.definitions.items():
                try:
                    if isinstance(data, dict):
                        bin_file = self.compile_definition(
                            data, name, file, compile_path)
                    else:
                        bin_file = self.compile_definition(
                            {"xml": data}, name, file, compile_path)
                except Exception as e:
                    raise RuntimeError(
                        f'{e}:\n    At definition file "{file}"') from e
                known_definitions.add(name)
                if bin_file:
                    compiled.add(name)

        # definitions に存在しない一時ファイルは削除
        for entry in self._tmp_path.joinpath("compile").iterdir():
            if not entry.is_dir():
                continue
            if entry.name not in known_definitions:
                print(f'Removing component temporary folder "{entry.name}"')
                shutil.rmtree(entry)

        # dist/data/components にコピー
        self._sync_bin_files(compile_path, self._dist_path)

        if sync_mod_folder:
            # Mod フォルダも過不足ない状態にする
            mod_path = Path(env["MOD_PATH"]) if "MOD_PATH" in env else None
            if not mod_path.is_dir():
                print(f'WARNING: MOD_PATH in env does not exist: "{mod_path}"')
                mod_path = None
            if mod_path is not None:
                self._sync_bin_files(
                    compile_path, mod_path.joinpath("data", "components"))

        self._dependency_cache.save(
            cache_file, mesh_compile_start_time, definition_compile_start_time)
        print(f"{len(compiled)} components compiled")

    def export_meshes(self):
        known_blend_names: set[str] = set()

        # 前回のコンパイルより更新が新しい .blend はエクスポート
        for blend_file in self._blender_path.glob("*.blend"):
            if not blend_file.is_file():
                continue

            blend_name = blend_file.with_suffix("").name
            known_blend_names.add(blend_name)
            meshes_path = self._meshes_path.joinpath(blend_name)
            if meshes_path.is_dir() and not self._dependency_cache.newer_than_last_mesh_compile(blend_file):
                continue
            print(f'Exporting meshes from blend file: "{blend_file}"')
            self._dependency_cache.remove_blend_name(blend_name)

            # エクスポート先を空にしておく
            for dae_file in self._dae_path.glob("*.dae"):
                os.remove(dae_file)

            py_file = blend_file.with_suffix(".py")
            if not py_file.is_file():
                py_file = self._blender_path.joinpath("default.py")

            _export_blend_file(blend_file, py_file)

            # .mesh の出力先を空にしておく
            if meshes_path.is_dir():
                shutil.rmtree(meshes_path)
            os.makedirs(meshes_path)
            for dae_file in self._dae_path.glob("*.dae"):
                if not dae_file.is_file():
                    continue
                _compile_mesh(dae_file, meshes_path)
                self._dependency_cache.add_mesh(
                    dae_file.with_suffix(".mesh").name, blend_name)

        # .blend が存在しない meshes フォルダは削除
        for entry in self._meshes_path.iterdir():
            if not entry.is_dir():
                continue
            if entry.name not in known_blend_names:
                print(f"Removing meshes from {entry.name}.blend")
                shutil.rmtree(entry)
                self._dependency_cache.remove_blend_name(entry.name)

    def compile_definition(self, data: dict, name: str, source_file: Path, compile_path: Path) -> Path | None:
        self._check_filename_prefix(name)
        compile_path = compile_path.joinpath(name)
        recompile = not compile_path.is_dir() \
            or self._dependency_cache.newer_than_last_definition_compile(source_file)

        dependency = self._dependency_cache.get_definition(name)
        if dependency is None:
            recompile = True
        else:
            # 依存ファイルの更新日時を確認
            files: list[Path] = [
                self._meshes_path.joinpath(
                    self._dependency_cache.get_mesh_blend_name(n),
                    n
                ) for n in dependency.mesh_names
            ]
            if dependency.lua_name is not None:
                files.append(
                    self._lua_path.joinpath(dependency.lua_name))
            files += [
                self._audio_path.joinpath(n)
                for n in dependency.sfx_names
            ]
            for file in files:
                if self._dependency_cache.newer_than_last_definition_compile(file):
                    recompile = True
                    break

        if not recompile:
            return
        print(f'Compiling component mod: "{name}"')

        root = ET.fromstring(fix_malformed_attributes(data["xml"]))
        self._check_definition(root)
        dependency = DefinitionDependencies(
            mesh_names=self._get_meshes(root))

        # Lua のチェック
        lua_script: tuple[str, str] | None = None
        if int(root.attrib.get("type")) == 66:
            lua_name = root.attrib.get("lua_filename")
            if lua_name is not None:
                dependency.lua_name = lua_name
                lua_file = self._lua_path.joinpath(lua_name)
                self._check_filename_prefix(lua_file)
                with lua_file.open("r", encoding="utf-8") as f:
                    lua = f.read()
                    if "luaPrefix" in data:
                        lua = data["luaPrefix"] + lua

                    # Lua に書かれている音声ファイルを追加
                    dependency.sfx_names.extend(self._get_sfx_from_lua(lua))
                    lua_script = (lua_name, lua)

        # 依存関係をキャッシュ
        self._dependency_cache.add_definition(name, dependency)

        # コンパイル用に一時ファイルを作成
        xml_file = compile_path.joinpath(name).with_suffix(".xml")
        os.makedirs(compile_path, exist_ok=True)
        with xml_file.open("w", encoding="utf-8") as f:
            f.write(data["xml"])
        for mesh_name in dependency.mesh_names:
            shutil.copy(
                self._meshes_path.joinpath(
                    self._dependency_cache.get_mesh_blend_name(mesh_name), mesh_name),
                compile_path.joinpath(mesh_name)
            )
        for sfx_name in dependency.sfx_names:
            shutil.copy(
                self._audio_path.joinpath(sfx_name),
                compile_path.joinpath(sfx_name)
            )
        if lua_script is not None:
            with compile_path.joinpath(lua_script[0]).open("w", encoding="utf-8") as f:
                f.write(lua_script[1])

        # component_mod_compiler を呼び出す
        cmd = f'"%COMPONENT_MOD_COMPILER_PATH%" "{xml_file.relative_to(compile_path)}" -s'
        for item in dependency.assets():
            cmd += f" {item}"
        subprocess.run(cmd, shell=True, check=True, env=env, cwd=compile_path)

        return xml_file.with_suffix(".bin")

    def _check_definition(self, root: ET.Element):
        # パーツ名の警告
        if self._name_prefix is not None and not root.attrib["name"].startswith(self._name_prefix):
            raise ValueError(
                f'Component name does not start with "{self._name_prefix}"')

        # タグの警告
        if self._required_tags is not None:
            tags = [t.strip() for t in root.attrib["tags"].split(",")]
            for required_tag in self._required_tags:
                if required_tag not in tags:
                    raise ValueError(
                        f'Component does not have required tag "{required_tag}"')

    def _get_meshes(self, root: ET.Element) -> list[str]:
        meshes: list[str] = []
        # mesh の列挙
        for attr_name in ["mesh_data_name", "mesh_0_name", "mesh_1_name", "mesh_2_name", "mesh_editor_only_name"]:
            mesh = root.attrib.get(attr_name, None)
            if mesh is None or len(mesh) == 0 or _is_vanilla_asset(mesh):
                continue
            self._check_filename_prefix(mesh)
            meshes.append(mesh)
        return meshes

    def _get_sfx_from_lua(self, lua: str) -> list[str]:
        include_sfx = {
            int(m.group("index")): m.group("filename1") or m.group("filename2")
            for m in _include_sfx_pattern.finditer(lua)
        }
        sfx_names: list[str] = []
        if len(include_sfx) > 0:
            for i in range(max(include_sfx.keys()) + 1):
                sfx_name = include_sfx.get(i, None)
                if sfx_name is None:
                    raise ValueError(f'include sfx {i} is missing')
                sfx_file = self._audio_path.joinpath(sfx_name)
                self._check_filename_prefix(sfx_file)
                if not sfx_file.is_file():
                    raise FileNotFoundError(
                        f'Audio file does not exist: "{sfx_file}"')
                sfx_names.append(sfx_name)
        return sfx_names

    def _sync_bin_files(self, compile_path: Path, target: Path):
        os.makedirs(target, exist_ok=True)

        to_copy = {p.name: p for p in compile_path.glob("*/*.bin")}
        for file in target.glob("*.bin"):
            if not file.is_file():
                continue
            name = file.name
            if name not in to_copy:
                print(f'Removing file: "{file}"')
                os.remove(file)
                continue
            src_file = to_copy[name]
            mtime = file.stat().st_mtime
            src_mtime = src_file.stat().st_mtime
            if mtime >= src_mtime:
                del to_copy[name]

        for name, src_path in to_copy.items():
            shutil.copy(src_path, target.joinpath(src_path.name))
