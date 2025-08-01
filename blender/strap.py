import itertools
import os
import sys
import importlib

dirname = os.path.dirname(os.path.realpath(__file__))

# 共通スクリプトインポート
module_path = os.path.join(dirname, "scripts")
if module_path not in sys.path:
    sys.path.append(module_path)
export_utils = importlib.import_module("export_utils")

export_path = os.path.join(dirname, "exported")


def export_strap(handle_type, handle_offset, belt_type, suffix="", decoratives=[]):
    # つり革可動部のエクスポート
    objs = []

    handle_obj = export_utils.duplicate_objects(
        [export_utils.get_object_by_name(f"handle_{handle_type}")]
    )[0]
    export_utils.translate_objects(
        [handle_obj],
        (0, 0, handle_offset)
    )
    objs.append(handle_obj)

    belt_obj = export_utils.duplicate_objects(
        [export_utils.get_object_by_name(f"belt_{belt_type}")]
    )[0]
    objs.append(belt_obj)

    for name, offset in decoratives:
        obj = export_utils.duplicate_objects(
            [export_utils.get_object_by_name(name)]
        )[0]
        export_utils.translate_objects([obj], (0, 0, offset))
        objs.append(obj)

    export_utils.apply_modifiers_on_objects(objs, {"CURVE"})
    export_utils.scale_objects(objs, 1.5)
    export_utils.export_objects(
        objs,
        f"m_tns_tetsudan_strap_{handle_type}_{belt_type}{suffix}.dae",
        dirname=export_path
    )
    export_utils.delete_objects(objs)


# Short, Medium
for handle_type, (handle_offset, belt_type, decorative_offset) in itertools.product(
    ["circle", "pentagon", "triangle1"],
    [(-0.1, 1, -0.06), (-0.16, 3, -0.1)]
):
    export_strap(
        handle_type,
        handle_offset,
        belt_type,
        "_binder",
        decoratives=[("binder", decorative_offset)]
    )
    export_strap(
        handle_type,
        handle_offset,
        belt_type,
        "_cover",
        decoratives=[("cover", decorative_offset)]
    )

# Long
for handle_type in ["circle", "pentagon", "triangle1"]:
    export_strap(
        handle_type, -0.28, 4,
        decoratives=[("binder", -0.09), ("cover", -0.18)]
    )

# 六角カバー・二等辺三角形
export_strap("triangle2", -0.12, 2, decoratives=[("hexagonal_cover", -0.07)])
export_strap("triangle3", -0.1, 1, decoratives=[("hexagonal_cover", -0.06)])

# 吊り棒
for name in ("bar_straight", "bar_t", "bar_curve"):
    export_utils.export_each_object(
        [export_utils.get_object_by_name(name)],
        export_path,
        "m_tns_tetsudan_strap_"
    )

# 支柱
for support_name in ("support_1", "support_2", "support_3"):
    support_obj = export_utils.get_object_by_name(support_name)

    for bar_obj_name, suffix in ((None, ""), ("bar_straight", "_middle"), ("bar_end", "_end1"), ("bar_end2", "_end2")):
        if support_name == "bar_support_1" and bar_obj_name == "bar_end2":
            continue

        objs = [support_obj]
        if bar_obj_name is not None:
            objs.append(export_utils.get_object_by_name(bar_obj_name))
        export_utils.export_objects(
            objs,
            f"m_tns_tetsudan_strap_{support_name}{suffix}.dae",
            dirname=export_path
        )
