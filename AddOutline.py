import bpy
import sys
import os
from customExceptions import *
from constValue import *
###################################################################
# dir_path = os.path.dirname(bpy.data.filepath)

# if dir_path not in sys.path:
#    sys.path.append(dir_path)

# import AppendResources

###################################################################

dir_path = os.path.dirname(os.path.realpath(__file__))

if dir_path not in sys.path:
    sys.path.append(dir_path)

import AppendResources

############################## 添加描边####################################


def AddOutline():

    ##################################################################

    # 追加资源
    blend_file_path = os.path.join(dir_path, MARLIN_TOON_SHADER_FILE_NAME)
    AppendResources.append_collection_from_blend_file(blend_file_path, MARLIN_TOON_SHADER_COLLECTION_NAME, MARLIN_TOON_SHADER_COLLECTION_NAME)

    # 查找名为“Merlin Toon Carrier 3.1(不要修改)”的集合
    collection_name = MARLIN_TOON_SHADER_COLLECTION_NAME
    collection = bpy.data.collections.get(collection_name)
    # 定义一个函数来递归查找并隐藏指定的集合

    def hide_collection(layer_collection, name):
        if layer_collection.collection.name == name:
            layer_collection.hide_viewport = True
            return True
        for child in layer_collection.children:
            if hide_collection(child, name):
                return True
        return False

    # 从视图层的根开始查找并隐藏集合
    if hide_collection(bpy.context.view_layer.layer_collection, collection_name) and collection:
        collection.hide_render = True

        # 强制更新场景
        bpy.context.view_layer.update()
        print(f'Collection "{collection_name}" has been hidden in viewport and disabled in renders.')
    else:
        print(f'Collection "{collection_name}" not found.')

    ##################################################################

    # 获取名为'描边'的节点组
    outline_node_group = bpy.data.node_groups.get("通用描边3.1")

    if outline_node_group is None:
        print("资源缺失")

    # 检索名称为"Outline"的材质
    outline_material = bpy.data.materials.get("Outline")

    if outline_material is None:
        print("资源缺失")

    else:
        # 获取所选物体
        selected_objs = bpy.context.selected_objects

        for obj in selected_objs:
            if obj.type == 'MESH':
                # 创建新的几何节点修改器
                geo_node_mod = obj.modifiers.new(type="NODES", name="通用描边3.1")

                # 设置修改器的节点组为描边节点组
                geo_node_mod.node_group = outline_node_group

                # 添加材质到物体的最后一个材质槽
                obj.data.materials.append(outline_material)

                # 创建一个名为'描边权重'的空顶点组
                obj.vertex_groups.new(name="描边权重")

############################### 清除描边###################################


def CleanOutline():

    # 获取当前被选中的物体
    selected_objects = bpy.context.selected_objects

    for obj in selected_objects:
        # 将物体激活为活动项
        bpy.context.view_layer.objects.active = obj
        # 倒序检索并删除名字包含“描边”的修改器
        for i in reversed(range(len(obj.modifiers))):
            if '描边' in obj.modifiers[i].name:
                obj.modifiers.remove(obj.modifiers[i])
        # 倒序检索并删除名字包含“Outline”的材质
        for i in reversed(range(len(obj.material_slots))):
            if 'Outline' in obj.material_slots[i].name:
                # 先将材质槽设为活动材质槽，然后删除
                obj.active_material_index = i
                bpy.ops.object.material_slot_remove()
