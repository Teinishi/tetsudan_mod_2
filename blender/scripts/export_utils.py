import os
import bpy  # type: ignore


def collection_set_hide(name, val):
    vlayer = bpy.context.scene.view_layers[0]
    if name in vlayer.layer_collection.children:
        vlayer.layer_collection.children[name].hide_viewport = val


def deselect_all_objects():
    bpy.ops.object.select_all(action="DESELECT")


def select_object(obj, add=False):
    if not add:
        deselect_all_objects()
    for collection in obj.users_collection:
        collection_set_hide(collection.name, False)
    obj.hide_set(False)
    obj.select_set(True)


def select_objects(objs, add=False):
    for obj in objs:
        select_object(obj, add=add)
        add = True


def export_objects(objs, filepath):
    select_objects(objs)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.ops.wm.collada_export(
        filepath=filepath,
        apply_modifiers=True,
        selected=True
    )


def auto_export(collection_name, prefix):
    for obj in bpy.data.collections[collection_name].objects:
        export_objects([obj], os.path.join(
            os.path.dirname(bpy.data.filepath),
            "exported",
            f"m_tns_{prefix}{obj.name}.dae"
        ))
