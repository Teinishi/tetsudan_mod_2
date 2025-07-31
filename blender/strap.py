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

# つり革
SCALE_STRAP = 1.5
for strap_type, strap_length in itertools.product(("circle", "pentagon", "triangle1", "triangle2"), ("short", "medium", "long")):
    obj_name = f"{strap_type}_{strap_length}"
    if not export_utils.object_exists(obj_name):
        continue

    obj = export_utils.get_object_by_name(obj_name)
    children = obj.children_recursive

    belt_cover_objs = [o for o in children if "belt_cover" in o.name]
    belt_binder_objs = [o for o in children if "belt_binder" in o.name]

    export_patterns = []

    if strap_length == "short" or strap_length == "medium":
        if len(belt_cover_objs) > 0:
            export_patterns.append((
                list(set([obj] + children) - set(belt_binder_objs)),
                "_cover"
            ))
        if len(belt_binder_objs) > 0:
            export_patterns.append((
                list(set([obj] + children) - set(belt_cover_objs)),
                "_binder"
            ))
    else:
        export_patterns.append(([obj] + children, ""))

    for pattern, suffix in export_patterns:
        objs = export_utils.duplicate_objects(pattern)
        export_utils.unparent_objects(objs)
        export_utils.apply_modifiers_on_objects(objs, {"CURVE"})
        export_utils.scale_objects(objs, SCALE_STRAP)
        export_utils.export_objects(
            objs,
            f"m_tns_train_strap_{strap_type}_{strap_length}{suffix}.dae",
            dirname=export_path
        )
        export_utils.delete_objects(objs)

# パイプ
for name in ("pipe_straight", "pipe_t", "pipe_curve"):
    export_utils.export_each_object(
        [export_utils.get_object_by_name(name)],
        export_path,
        "m_tns_train_strap_"
    )

for support_name in ("pipe_support_1", "pipe_support_2", "pipe_support_3"):
    support_obj = export_utils.get_object_by_name(support_name)

    for pipe_obj_name, suffix in ((None, ""), ("pipe_straight", "_middle"), ("pipe_end", "_end1"), ("pipe_end2", "_end2")):
        if support_name == "pipe_support_1" and pipe_obj_name == "pipe_end2":
            continue

        objs = [support_obj]
        if pipe_obj_name is not None:
            objs.append(export_utils.get_object_by_name(pipe_obj_name))
        export_utils.export_objects(
            objs,
            f"m_tns_train_strap_{support_name}{suffix}.dae",
            dirname=export_path
        )

# ワクベ矢印
export_utils.collection_export("arrow", export_path, "m_tns_train_")
