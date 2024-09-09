import bpy
import os
import sys

# 开发者使用的路径
# sys.path.append(r"C:\Users\willo\Desktop\addontest")
# blend_file_path = r'C:\Users\willo\Desktop\addontest\resources\Merlin_MMD_Toon_Shader_3_1.blend'

# 从材质中删除一个节点组
def remove_node_group_from_material(material, node_group_name):
    if material.use_nodes:
        node_tree = material.node_tree
        # 找到要删除的节点
        nodes_to_remove = [node for node in node_tree.nodes if node.type == 'GROUP' and node.node_tree.name == node_group_name]
        # 删除找到的节点
        for node in nodes_to_remove:
            node_tree.nodes.remove(node)

# 向材质中添加一个节点组
def add_node_group_to_material(material, node_group_name, x_location, y_location):
    if material.use_nodes:
        node_tree = material.node_tree
        
        # 如果节点组不存在于当前blend文件的数据中，则打印“资源缺失”
        if node_group_name not in bpy.data.node_groups:
            print("资源缺失")
            return None
        
        # 在指定位置创建新的节点组
        group_node = node_tree.nodes.new(type='ShaderNodeGroup')
        group_node.node_tree = bpy.data.node_groups[node_group_name]
        group_node.location = (x_location, y_location)
        return group_node  # 返回创建的节点以便后续使用


# 从源节点复制参数到目标节点
def copy_parameters(source_node, target_node, parameters):
    for param in parameters:
        if param in source_node.inputs and param in target_node.inputs:
            target_node.inputs[param].default_value = source_node.inputs[param].default_value

# 连接源节点和目标节点的插座
def connect_node_groups(node_tree, src_node, src_socket_name, tgt_node, tgt_socket_name):
    src_socket = src_node.outputs.get(src_socket_name)
    tgt_socket = tgt_node.inputs.get(tgt_socket_name)
    if src_socket and tgt_socket:
        node_tree.links.new(src_socket, tgt_socket)

# 检查节点组是否在节点树中被使用
def is_node_group_used(node_tree, target_group):
    for node in node_tree.nodes:
        if node.type == 'GROUP':
            # 如果节点组在节点树中被使用，返回True
            if node.node_tree == target_group:
                return True
            # 递归调用以检查节点组是否在子节点树中被使用
            elif is_node_group_used(node.node_tree, target_group):  
                return True
    return False
