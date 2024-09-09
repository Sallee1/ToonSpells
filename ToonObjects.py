import bpy
import sys
import os
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

##################################################################


def ToonObjects():

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

    # 检索名称为"Merlin_Toon_Shader 3.1"的材质
    mat_toon = bpy.data.materials.get("Merlin_Toon_Shader 3.1")

    if mat_toon is None:
        print("资源缺失")

    # 获取被选中的物体
    selected_objs = bpy.context.selected_objects

    # 遍历所有被选中的物体
    for obj in selected_objs:
        # 检查物体是否是一个网格（Mesh）对象，只有网格对象才会有材质
        if obj.type == 'MESH':
            # 添加材质到物体的最后一个材质槽
            obj.data.materials.append(mat_toon.copy())
