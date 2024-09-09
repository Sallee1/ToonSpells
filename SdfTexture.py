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


def SdfTexture():

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

    def assign_material_to_selected_faces(material_name):
        # 获取当前选中的对象
        obj = bpy.context.object
        if obj is None or obj.type != 'MESH':
            print("请选中一个网格对象。")
            return

        # 获取材质
        material = bpy.data.materials.get(material_name)
        if material is None:
            print(f"材质 '{material_name}' 未找到。")
            return

        # 进入编辑模式
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="FACE")

        # 为选中的面赋予材质
        bpy.ops.object.material_slot_add()
        obj.active_material = material
        bpy.ops.object.material_slot_assign()

        # 回到对象模式
        bpy.ops.object.mode_set(mode='OBJECT')

        # 制作材质的单用户副本
        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True, material=True, animation=False)
        print(f"材质 '{material_name}' 已被分配并制作单用户副本。")

    def copy_specific_geometry_nodes(target_obj, carrier_name, gn1_name, gn2_name):
        # 获取场景中的指定物体
        carrier_obj = bpy.data.objects.get(carrier_name)
        if carrier_obj is None:
            print(f"对象 '{carrier_name}' 未找到。")
            return

        # 确保正确选择对象
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = carrier_obj
        carrier_obj.select_set(True)
        target_obj.select_set(True)

        # 使用 make_links_data 将修饰器复制到目标对象
        bpy.ops.object.make_links_data(type='MODIFIERS')

        print(f"已将几何节点 '{gn1_name}' 和 '{gn2_name}' 从 '{carrier_name}' 复制到 '{target_obj.name}'。")

    def add_uv_map(obj_name, uv_map_name):
        # 获取对象
        obj = bpy.data.objects.get(obj_name)
        if obj is None:
            print(f"对象 '{obj_name}' 未找到。")
            return

        # 创建新的 UV 映射
        if uv_map_name not in obj.data.uv_layers:
            obj.data.uv_layers.new(name=uv_map_name)
            print(f"已为对象 '{obj_name}' 添加 UV 映射 '{uv_map_name}'。")
        else:
            print(f"对象 '{obj_name}' 已有名为 '{uv_map_name}' 的 UV 映射。")

    def duplicate_object(obj):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.ops.object.duplicate(linked=False)
        return bpy.context.selected_objects[0]

    def copy_modifiers_back_to_object(proxy, obj):
        existing_modifiers = {mod.name: mod for mod in obj.modifiers}

        for mod in proxy.modifiers:
            if mod.name in existing_modifiers:
                existing_mod = existing_modifiers[mod.name]
                # 更新已有的修改器
                copy_modifier_properties(mod, existing_mod)
            else:
                # 添加新修改器
                new_mod = obj.modifiers.new(name=mod.name, type=mod.type)
                copy_modifier_properties(mod, new_mod)

    def copy_modifier_properties(source_mod, target_mod):
        for attr in dir(source_mod):
            # 排除一些不必要的属性
            if not attr.startswith("_") and not callable(getattr(source_mod, attr)):
                try:
                    setattr(target_mod, attr, getattr(source_mod, attr))
                except AttributeError:
                    # 一些属性可能是只读的，跳过这些属性
                    pass

    def get_armature_modifier(obj):
        """检索对象的Armature Modifier"""
        for modifier in obj.modifiers:
            if modifier.type == 'ARMATURE':
                return modifier
        return None

    def find_head_locator_child(armature_obj):
        """检索骨架对象的子物体中名字带有“Head Locator”的物体"""
        for child in armature_obj.children:
            if "Head Locator" in child.name:
                return child
        return None

    def get_three_children(obj):
        """获取对象的三个子物体"""
        return obj.children[:3]

    def set_output_attributes(modifier, f_name, r_name):
        """设置输出属性的名称"""
        for node in modifier.node_group.nodes:
            if node.type == 'GROUP_OUTPUT':
                for socket in node.inputs:
                    if socket.name == 'f':
                        socket.name = f_name
                        print(f"设置输出属性 f 的名称为: {f_name}")
                    elif socket.name == 'r':
                        socket.name = r_name
                        print(f"设置输出属性 r 的名称为: {r_name}")
                return

    def print_geometry_node_inputs_and_set_values(obj, modifier_name, input_objs):
        # 检索物体的几何节点修改器
        for modifier in obj.modifiers:
            if modifier.type == 'NODES' and modifier.node_group and modifier.node_group.name == modifier_name:
                node_group = modifier.node_group
                print(f"几何节点修改器 '{modifier_name}' 的输入参数名称和类型:")

                # 获取节点组输入
                inputs = node_group.inputs[1:]  # 跳过第一个参数
                for i, input in enumerate(inputs):
                    # 打印参数名称和类型
                    print(f"名称: {input.name}, 类型: {input.type}")

                    # 尝试获取当前输入的物体名称并设置新的值
                    if input.type == 'OBJECT':
                        try:
                            modifier[input.identifier] = input_objs[i]
                            input_value = modifier[input.identifier]
                            if input_value and isinstance(input_value, bpy.types.Object):
                                print(f"当前对应的物体名称: {input_value.name}")
                            else:
                                print("当前没有对应的物体")
                        except AttributeError:
                            print(f"无法设置 {input.name} 的当前物体")

                # 设置输出属性名称
                set_output_attributes(modifier, "f", "r")
                return
        print(f"没有找到名为 '{modifier_name}' 的几何节点修改器。")

    # 确保有选中的对象和面
    if bpy.context.object is None or bpy.context.object.type != 'MESH':
        print("请选中一个包含选中面的网格对象。")
        return

    obj = bpy.context.object
    material_name = "Merlin_Toon_Shader_SDF 3.1"
    carrier_name = "SDF Carrier"
    gn1_name = "灯光向量常用3.1"
    gn2_name = "脸朝向常用3.1"
    uv_map_name = "UVMap2"

    # 步骤1: 检索Armature Modifier
    armature_modifier = get_armature_modifier(obj)

    if armature_modifier is None:
        raise bl_Operator_Error("选中物体没有骨架修改器")

    # 获取Armature Modifier指定的骨架对象
    armature_obj = armature_modifier.object
    if armature_obj is None:
        raise bl_Operator_Error("骨架修改器没有指定对象")

    # 步骤2: 检索骨架对象的子物体中名字带有“Head Locator”的物体
    head_locator = find_head_locator_child(armature_obj)
    if head_locator is None:
        raise bl_Operator_Error("没有找到Head Locator物体，请先使用“SDF定位咒”")
        return

    # 获取Head Locator的三个子物体并打印它们的名称
    children = get_three_children(head_locator)
    if len(children) < 3:
        raise bl_Operator_Error("Head Locator物体已损坏，请删除后再使用“SDF定位咒”")
        return

    for i, child in enumerate(children, 1):
        print(f"子物体{i}名称: {child.name}")

    # 步骤3: 设置“脸朝向常用3.1”几何节点的三个输入参数
    modifier_name = "脸朝向常用3.1"
    print_geometry_node_inputs_and_set_values(obj, modifier_name, children)
    # 为选中的面赋予材质
    assign_material_to_selected_faces(material_name)

    # 为对象添加 UV 映射
    add_uv_map(obj.name, uv_map_name)

    bpy.ops.object.mode_set(mode='OBJECT')

    # 创建代理物体
    proxy = duplicate_object(obj)
    proxy.name = "Proxy_Object"

    # 从载体物体复制几何节点到选中物体
    copy_specific_geometry_nodes(obj, carrier_name, gn1_name, gn2_name)

    # 复制修改器回原对象
    copy_modifiers_back_to_object(proxy, obj)

    bpy.data.objects.remove(proxy, do_unlink=True)

    bpy.data.objects[carrier_name].select_set(False)

    obj.select_set(True)

    bpy.context.view_layer.objects.active = obj

    print(f"对象 '{obj.name}' 已完成所有操作。")
