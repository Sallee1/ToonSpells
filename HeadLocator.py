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

############################### 定位脸部朝向###################################


def HeadLocator():

    ###################################################################

    # 追加资源
    blend_file_path = os.path.join(dir_path, MARLIN_TOON_SHADER_FILE_NAME)
    AppendResources.append_collection_from_blend_file(blend_file_path, "Mihoyo Carrier", "Mihoyo Carrier")

    ############ 找到骨架并将头骨设为Mihoyo Carrier的父级############

    # 保存对原先选中物体的引用
    parent_obj = bpy.context.object

    # 获取场景中的 "Mihoyo_Carrier" 对象
    mihoyo_carrier_obj = bpy.data.objects.get("Mihoyo_Carrier")

    if mihoyo_carrier_obj is None:
        print("没有找到名为 'Mihoyo_Carrier' 的对象")

    # 清除所有选中的物体
    bpy.ops.object.select_all(action='DESELECT')

    armature_obj = None

    # 确认一个物体被选中，且这个物体是网格类型的
    for obj in parent_obj.children:
        # 如果子物体的名称包含 "_arm"
        if "_arm" in obj.name and obj.type == 'ARMATURE':
            # 选中子物体
            obj.select_set(True)
            # 将选中的物体设为活动对象
            bpy.context.view_layer.objects.active = obj
            armature_obj = obj

            # 进入编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 在编辑模式下查找名为 "頭" 的骨骼
            edit_bone = armature_obj.data.edit_bones.get("頭")

            if edit_bone:
                # 将 "頭" 骨骼的扭转角度设置为 0
                edit_bone.roll = 0.0

                # 在这里添加您的操作，比如将 "Mihoyo_Carrier" 对象与骨骼建立父子关系
                mihoyo_carrier_obj.parent = armature_obj
                mihoyo_carrier_obj.parent_bone = edit_bone.name
                mihoyo_carrier_obj.parent_type = 'BONE'
            else:
                print("没有找到名为 '頭' 的编辑骨骼")

            # 退出编辑模式
            bpy.ops.object.mode_set(mode='OBJECT')

            # 退出循环
            break
    else:
        print("没有找到名为 '_arm' 的对象")

    # 清除所有选中的物体
    bpy.ops.object.select_all(action='DESELECT')

    ############ 定位到mesh############

    if armature_obj:
        for obj in armature_obj.children:
            # 如果子物体的名称包含"_mesh"
            if "_mesh" in obj.name:
                # 选中子物体
                obj.select_set(True)
                # 将选中的物体设为活动对象
                bpy.context.view_layer.objects.active = obj
                # 退出循环
                break
