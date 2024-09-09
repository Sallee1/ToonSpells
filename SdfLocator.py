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

##################################################################


def SdfLocator():

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

    def duplicate_objects_simulating_shift_d(name, target_collection_name):
        # 确保正确的上下文
        bpy.ops.object.mode_set(mode='OBJECT')  # 切换到对象模式

        # 查找并选择指定的对象及其子对象
        target_object = bpy.data.objects.get(name)
        if not target_object:
            print(f"错误：没有找到名为'{name}'的对象。")
            return None

        # 清除当前的选择
        bpy.ops.object.select_all(action='DESELECT')

        # 选择目标对象及其所有子对象
        target_object.select_set(True)
        for child in target_object.children:
            child.select_set(True)

        # 模拟 Shift+D 复制
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'})

        # 获取新复制的对象（它们应该是当前选中的对象，并且没有标记）
        duplicated_objects = [obj for obj in bpy.context.selected_objects if not obj.get("duplicated")]
        print(f"复制操作后找到的对象数量: {len(duplicated_objects)}")  # 调试信息
        for obj in duplicated_objects:
            print(f"找到的对象名称: {obj.name}")  # 打印所有找到的对象名称

        duplicated_main_object = duplicated_objects[0] if duplicated_objects else None

        # 清除标记
        if duplicated_main_object:
            duplicated_main_object["duplicated"] = False
            for child in duplicated_main_object.children:
                child["duplicated"] = False

        # 取消所有对象的选择
        bpy.ops.object.select_all(action='DESELECT')

        if duplicated_main_object:
            print(f"'{name}'及其子集已被复制。")
            # 打印被复制对象的名称
            print(f"复制的对象名称: {duplicated_main_object.name}")

            # 移动复制的对象到目标集合
            target_collection = bpy.data.collections.get(target_collection_name)
            if target_collection:
                for obj in duplicated_objects:
                    for collection in obj.users_collection:
                        collection.objects.unlink(obj)
                    target_collection.objects.link(obj)
                print(f"复制的对象已移动到集合 '{target_collection_name}' 中。")
            else:
                print(f"未找到名为 '{target_collection_name}' 的集合。")

            return duplicated_main_object.name
        else:
            print("复制失败。")
            return None

    def main():
        # 步骤1: 记录当前被选中的骨骼名称和它所处的骨架的名称
        armature_obj = bpy.context.active_object
        active_bone = bpy.context.active_pose_bone

        collection_name = MARLIN_TOON_SHADER_COLLECTION_NAME
        if (active_bone is None):
            hide_collection(bpy.context.view_layer.layer_collection, collection_name)
            raise bl_Operator_Error("未选择骨骼，请选择控制头部的骨骼，然后重试")
        bone_name = active_bone.name
        armature_name = armature_obj.name
        print(f"记录信息：骨骼名 '{bone_name}', 骨架名 '{armature_name}'")

        # 执行复制操作
        locator_name = "Head Locator 3.1"
        target_collection_name = armature_obj.users_collection[0].name
        locator_name2 = duplicate_objects_simulating_shift_d(locator_name, target_collection_name)

        # 步骤4: 根据之前记录的骨架名重新选择骨架
        armature_obj = bpy.data.objects.get(armature_name)
        if not armature_obj:
            print(f"未找到名为 '{armature_name}' 的骨架。")
            return
        bpy.context.view_layer.objects.active = armature_obj
        armature_obj.select_set(True)

        # 步骤5: 进入姿态模式，根据之前记录的骨骼名选中骨骼
        bpy.ops.object.mode_set(mode='POSE')
        armature_obj.data.bones.active = armature_obj.pose.bones[bone_name].bone
        armature_obj.data.bones.active.select = True

        print("完成操作：已重新选择骨骼。")

        return locator_name2

    # 定义一个函数来递归查找并取消指定集合的隐藏状态
    def unhide_collection(layer_collection, name):
        if layer_collection.collection.name == name:
            layer_collection.hide_viewport = False
            return True
        for child in layer_collection.children:
            if unhide_collection(child, name):
                return True
        return False

    # 定义一个函数来递归查找并打开指定集合的隐藏状态
    def hide_collection(layer_collection, name):
        if layer_collection.collection.name == name:
            layer_collection.hide_viewport = True
            return True
        for child in layer_collection.children:
            if hide_collection(child, name):
                return True
        return False

    # 查找名为“Merlin Toon Carrier 3.1(不要修改)”的集合
    collection_name = MARLIN_TOON_SHADER_COLLECTION_NAME
    if unhide_collection(bpy.context.view_layer.layer_collection, collection_name):
        print(f'集合 "{collection_name}" 的隐藏状态已关闭。')
    else:
        print(f'未找到名为 "{collection_name}" 的集合。')

    # 运行主函数
    locator_name_duplicated = main()

    def set_parent_to_selected_bone(object_name):
        # 获取当前活动对象和选中的骨骼
        armature_obj = bpy.context.active_object
        active_bone = bpy.context.active_pose_bone

        # 确保当前选中的对象是骨架，并且有一个选中的骨骼
        if not armature_obj or armature_obj.type != 'ARMATURE' or not active_bone:
            print("请确保选中了骨架和骨骼。")
            return

        # 获取要设置父级的对象
        target_object = bpy.data.objects.get(object_name)
        if not target_object:
            print(f"错误：没有找到名为'{object_name}'的对象。")
            return

        # 设置父级
        target_object.parent = armature_obj
        target_object.parent_type = 'BONE'
        target_object.parent_bone = active_bone.name
        print(f"'{object_name}'的父级现在设置为骨骼'{active_bone.name}'在骨架'{armature_obj.name}'中。")

    # 运行函数，将空物体“Head Locator 3.002”的父级设为当前被选中的骨骼
    set_parent_to_selected_bone(locator_name_duplicated)

    if hide_collection(bpy.context.view_layer.layer_collection, collection_name):
        print(f'集合 "{collection_name}" 的隐藏状态已打开。')
    else:
        print(f'未找到名为 "{collection_name}" 的集合。')
