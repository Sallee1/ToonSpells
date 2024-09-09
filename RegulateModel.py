import bpy
import os
import sys

def RegulateModel():

###################################################################

    # 获取当前选中的物体
    obj = bpy.context.object

    # 将当前物体设为活动物体
    bpy.context.view_layer.objects.active = obj

    def ModifyMaterials():
        # 创建一个集合来储存要被删除的材质名
        materials_to_remove = set(["颜+", "顏+","Face_Mask_Mat1","裙內側2+","上衣內襯+","內遮","袖內襯+","上半身+","顏遮"])

        # 定义材质名的映射字典
        material_name_mapping = {
            "颜": "脸",
            "顏":"脸",
            "臉":"脸",
            "眉目": "眉毛",
            "眼": "眼睛",
            "目": "眼睛",
            "口齿": "口腔",
            "髪": "头发",
            "biaoq": "表情",
            "目影": "眼睛1",
            "白目":"眼白",
            "眉眼": "眉毛",
            "齿": "牙齿",
            "口": "口腔",
            "口齒": "口腔"
        }
        
        # 对所有被选中的物体进行操作
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                # 切换到编辑模式
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                # 获取所有的材质槽位
                mats = obj.data.materials
                # 检查每个材质槽
                for i in reversed(range(len(mats))):
                    # 如果材质存在
                    if mats[i]:
                        # 如果材质的名字在要被删除的材质名的集合中
                        if mats[i].name in materials_to_remove:
                            # 先取消所有已选中的面
                            bpy.ops.mesh.select_all(action='DESELECT')
                            # 选中当前槽位的所有面
                            obj.active_material_index = i
                            bpy.ops.object.material_slot_select()
                            # 删除正在使用这个材质的所有面
                            bpy.ops.mesh.delete(type='FACE')
                            # 删除这个材质
                            bpy.data.materials.remove(mats[i])
#                            # 删除空的材质槽
#                            bpy.ops.object.material_slot_remove()
                        # 如果材质的名字在映射字典中
                        elif mats[i].name in material_name_mapping.keys():
                            # 使用映射字典中的新名字重命名材质
                            mats[i].name = material_name_mapping[mats[i].name]
                # 切换回物体模式
                bpy.ops.object.mode_set(mode='OBJECT')

    ModifyMaterials()

    bpy.ops.object.material_slot_remove_unused()

#RegulateModel()