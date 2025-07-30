import os
import bpy  # type: ignore
import bmesh  # type: ignore


def collection_set_hide(name, val):
    vlayer = bpy.context.scene.view_layers[0]
    if name in vlayer.layer_collection.children:
        vlayer.layer_collection.children[name].hide_viewport = val


def get_object_by_name(name):
    return bpy.data.objects.get(name)


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


def delete_objects(objs):
    select_objects(objs)
    bpy.ops.object.delete()


def duplicate_objects(objs):
    select_objects(objs)
    bpy.ops.object.duplicate()
    duplicated = [o for o in bpy.context.selected_objects]
    deselect_all_objects()
    return duplicated


def translate_vertices(obj, translate, condition=True):
    if condition == True:
        def condition(): return True

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    obj = bpy.context.active_object

    for _, v in enumerate(bm.verts):
        coord = obj.matrix_world @ v.co
        if condition(coord):
            v.select = True
    bpy.ops.transform.translate(value=translate)

    bpy.ops.object.mode_set(mode='OBJECT')


def export_objects(objs, filepath):
    select_objects(objs)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.ops.wm.collada_export(
        filepath=filepath,
        apply_modifiers=True,
        selected=True
    )


def auto_export(collection_name, path, prefix, origin_offset=False):
    for obj in bpy.data.collections[collection_name].objects:
        dup = duplicate_objects([obj])[0]
        if origin_offset:
            dup.location = (0, 0, 0)
        export_objects(
            [dup],
            os.path.join(path, f"{prefix}{obj.name}.dae")
        )
        delete_objects([dup])
