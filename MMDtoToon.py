import bpy
import sys
import os
from constValue import *
# from ToonSpells import NodeGroupOperator

###################################################################
# dir_path = os.path.dirname(bpy.data.filepath)

# if dir_path not in sys.path:
#    sys.path.append(dir_path)

# import AppendResources
# import NodeGroupOperator

###################################################################

dir_path = os.path.dirname(os.path.realpath(__file__))

if dir_path not in sys.path:
    sys.path.append(dir_path)

import AppendResources
import NodeGroupOperator

##################################################################

# 将所有选中的对象/网格的由MMD工具生成的MMD材质转化为Toon材质


def MMDtoToonSpell():

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

    node_group_name = "MMDShaderDev"
    target_node_group_name = "MMD主节点 3.1"
    target_node_group_name2 = "全局光照 3.1"

    # 列出需要复制的参数
    parameters_to_copy = ["Sphere Mul/Add", "Double Sided", "Alpha", "Base Tex Fac", "Toon Tex Fac", "Sphere Tex Fac"]

    # 遍历所有选中的对象，检查它们是否是网格以及它们是否有材质
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH' and obj.data.materials is not None:

            # 遍历每个选中的网格的所有材质
            for mat_slot in obj.material_slots:
                if mat_slot.material is not None:

                    # 如果材质使用了MMDShaderDev节点组，则向节点树中添加Toon shader core节点组
                    toon_node = NodeGroupOperator.add_node_group_to_material(mat_slot.material, target_node_group_name, 0, 1500)
                    source_node = next((node for node in mat_slot.material.node_tree.nodes if node.type == 'GROUP' and node.node_tree.name == node_group_name), None)
                    if source_node and toon_node:
                        NodeGroupOperator.copy_parameters(source_node, toon_node, parameters_to_copy)
                    NodeGroupOperator.remove_node_group_from_material(mat_slot.material, node_group_name)

                    # 向节点树中添加全局光照 3.1节点组
                    global_light_node = NodeGroupOperator.add_node_group_to_material(mat_slot.material, target_node_group_name2, -200, 1300)
                    if toon_node and global_light_node:
                        NodeGroupOperator.connect_node_groups(mat_slot.material.node_tree, global_light_node, "全局主光颜色", toon_node, "主光颜色")
                        NodeGroupOperator.connect_node_groups(mat_slot.material.node_tree, global_light_node, "全局阴影颜色", toon_node, "阴影颜色")

                    # 获取'mmd_base_tex'节点
                    mmd_base_tex_node = next((node for node in mat_slot.material.node_tree.nodes if node.name == 'mmd_base_tex'), None)
                    if mmd_base_tex_node and toon_node:
                        # 将'mmd_base_tex'的'Color'输出连接到'MMD主节点 3.1'的'Base Color'输入
                        NodeGroupOperator.connect_node_groups(mat_slot.material.node_tree, mmd_base_tex_node, "Color", toon_node, "Base Tex")
                        # 将'mmd_base_tex'的'Alpha'输出连接到'MMD主节点 3.1'的'Base Alpha'输入
                        NodeGroupOperator.connect_node_groups(mat_slot.material.node_tree, mmd_base_tex_node, "Alpha", toon_node, "Base Alpha")

                    # 获取'mmd_toon_tex'节点
                    mmd_toon_tex_node = next((node for node in mat_slot.material.node_tree.nodes if node.name == 'mmd_toon_tex'), None)
                    if mmd_toon_tex_node and toon_node:
                        # 将'mmd_toon_tex'的'Color'输出连接到'MMD主节点 3.1'的'Toon Color'输入
                        NodeGroupOperator.connect_node_groups(mat_slot.material.node_tree, mmd_toon_tex_node, "Color", toon_node, "Toon Tex")
                        # 将'mmd_toon_tex'的'Alpha'输出连接到'MMD主节点 3.1'的'Toon Alpha'输入
                        NodeGroupOperator.connect_node_groups(mat_slot.material.node_tree, mmd_toon_tex_node, "Alpha", toon_node, "Toon Alpha")

                    # 获取'mmd_sphere_tex'节点
                    mmd_sphere_tex_node = next((node for node in mat_slot.material.node_tree.nodes if node.name == 'mmd_sphere_tex'), None)
                    if mmd_sphere_tex_node and toon_node:
                        # 将'mmd_sphere_tex'的'Color'输出连接到'MMD主节点 3.1'的'Sphere Color'输入
                        NodeGroupOperator.connect_node_groups(mat_slot.material.node_tree, mmd_sphere_tex_node, "Color", toon_node, "Sphere Tex")
                        # 将'mmd_sphere_tex'的'Alpha'输出连接到'MMD主节点 3.1'的'Sphere Alpha'输入
                        NodeGroupOperator.connect_node_groups(mat_slot.material.node_tree, mmd_sphere_tex_node, "Alpha", toon_node, "Sphere Alpha")

                    # 获取材质输出节点
                    material_output_node = next((node for node in mat_slot.material.node_tree.nodes if node.type == 'OUTPUT_MATERIAL'), None)
                    if material_output_node and toon_node:
                        # 将'MMD主节点 3.1'的'Color'输出连接到材质输出节点的'Surface'输入
                        NodeGroupOperator.connect_node_groups(mat_slot.material.node_tree, toon_node, "Result", material_output_node, "Surface")
