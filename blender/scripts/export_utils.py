import os
import bpy  # type: ignore
import bmesh  # type: ignore


def collection_set_hide(name, val):
    vlayer = bpy.context.scene.view_layers[0]
    if name in vlayer.layer_collection.children:
        vlayer.layer_collection.children[name].hide_viewport = val


def object_exists(name):
    return name in bpy.data.objects


def get_object_by_name(name):
    obj = bpy.data.objects.get(name)
    if obj is None:
        raise NameError(f'No object named "{name}" found')
    return obj


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


def translate_objects(objs, value):
    select_objects(objs)
    bpy.ops.transform.translate(value=value)


def scale_objects(objs, value, center=(0, 0, 0)):
    select_objects(objs)
    if isinstance(value, int) or isinstance(value, float):
        value = (value, value, value)
    bpy.ops.transform.resize(value=value, center_override=center)


def rotate_objects(objs, value, axis, center=(0, 0, 0)):
    select_objects(objs)
    bpy.ops.transform.rotate(
        value=value, orient_axis=axis, center_override=center)


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


def unparent_objects(objs):
    for obj in objs:
        obj.parent = None


def apply_modifiers_on_object(obj, modifier_types):
    bpy.context.view_layer.objects.active = obj
    for modifier in obj.modifiers:
        if modifier.type in modifier_types:
            bpy.ops.object.modifier_apply(modifier=modifier.name)


def apply_modifiers_on_objects(objs, modifier_types):
    for obj in objs:
        apply_modifiers_on_object(obj, modifier_types)


def export_objects(objs, filepath, dirname=None):
    if dirname is not None:
        filepath = os.path.join(dirname, filepath)
    select_objects(objs)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.ops.wm.collada_export(
        filepath=filepath,
        apply_modifiers=True,
        selected=True
    )


def export_each_object(objs, path, prefix, origin_offset=False):
    for obj in objs:
        dup = duplicate_objects([obj])[0]
        if origin_offset:
            dup.location = (0, 0, 0)
        export_objects(
            [dup],
            os.path.join(path, f"{prefix}{obj.name}.dae")
        )
        delete_objects([dup])


def collection_export(collection_name, path, prefix, origin_offset=False):
    export_each_object(
        bpy.data.collections[collection_name].objects, path, prefix, origin_offset=origin_offset)
