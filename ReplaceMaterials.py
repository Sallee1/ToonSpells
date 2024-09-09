import bpy
import os
import sys

###################################################################
# dir_path = os.path.dirname(bpy.data.filepath)

# if dir_path not in sys.path:
#    sys.path.append(dir_path)

###################################################################

dir_path = os.path.dirname(os.path.realpath(__file__))

if dir_path not in sys.path:
    sys.path.append(dir_path)

###################################################################


def ReplaceMaterials():

    ####################################################################

    # 获取激活的对象
    active_obj = bpy.context.active_object

    # 选择所有你想复制修改器的对象
    bpy.ops.object.select_all(action='DESELECT')
    selected_objects = [obj for obj in bpy.context.scene.objects if "身体" in obj.name or "头发" in obj.name]
    for obj in selected_objects:
        obj.select_set(True)

    if (len(selected_objects) == 0):
        print("未找到对象!")
        return

    # 获取 Mihoyo_Carrier 对象
    mihoyo_carrier = bpy.data.objects.get('Mihoyo_Carrier')
    if not mihoyo_carrier:
        print("Mihoyo_Carrier未找到!")
        exit()

    # 确保 Mihoyo_Carrier 是活动对象
    bpy.context.view_layer.objects.active = mihoyo_carrier
    mihoyo_carrier.select_set(True)

    # 从第一个选中的对象中复制修改器到 Mihoyo_Carrier
    for mod in selected_objects[0].modifiers:
        new_mod = mihoyo_carrier.modifiers.new(mod.name, mod.type)
        settings = {name: getattr(mod, name) for name in dir(mod) if not name.startswith(("_", "error", "rna"))}
        for name, val in settings.items():
            try:
                setattr(new_mod, name, val)
            except AttributeError:
                pass

        # 移动刚复制的修改器到最顶部
        bpy.ops.object.modifier_move_to_index(modifier=new_mod.name, index=0)

    # 将修改器复制到所有选中的对象
    bpy.ops.object.make_links_data(type='MODIFIERS')

    bpy.context.view_layer.objects.active = active_obj

    # 获取活动对象的父对象
    parent_obj = bpy.context.object.parent

    # 清除所有选中的对象
    bpy.ops.object.select_all(action='DESELECT')

    # 检查父对象是否存在
    if parent_obj:
        # 遍历父对象的所有子对象
        for obj in parent_obj.children:
            # 如果子对象的名称包含 "_mesh"
            if "_mesh" in obj.name:
                # 选中子对象
                obj.select_set(True)
    else:
        print("活动对象没有父对象。")

    # 从文件中读取列表
    def read_list_from_file(filename):
        with open(filename, "r") as file:
            lines = file.readlines()
        return [line.strip() for line in lines]

    # 使用材质的 user_remap 方法来重映射材质
    def remap_material(old_material_name, new_material_name):
        materials = bpy.data.materials
        if old_material_name in materials and new_material_name in materials:
            materials[old_material_name].user_remap(materials[new_material_name])
        else:
            print(f"Material '{old_material_name}' or '{new_material_name}' not found.")

    # 处理身体

    def process_body(obj, filename):
        list_from_file = read_list_from_file(filename)
        for mat_slot in obj.material_slots:
            if mat_slot.name == "脸":
                remap_material("脸", "脸prep")
            elif "mmd_base_tex" in mat_slot.material.node_tree.nodes:
                image_node = mat_slot.material.node_tree.nodes["mmd_base_tex"]
                if any(word in image_node.image.name for word in list_from_file[0].split(',')) or any(word in image_node.image.name for word in list_from_file[2].split(',')):
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='DESELECT')
                    obj.active_material_index = obj.material_slots.find(mat_slot.name)
                    bpy.ops.object.material_slot_select()
                    bpy.ops.mesh.delete(type='FACE')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.data.materials.remove(mat_slot.material)
                elif any(word in image_node.image.name for word in list_from_file[1].split(',')):
                    remap_material(mat_slot.name, "身体2prep")
                elif any(word in image_node.image.name for word in list_from_file[3].split(',')):
                    remap_material(mat_slot.name, "身体1prep")

    # 删除所有材质并添加新材质

    def replace_materials(obj, new_material_name):
        for mat in obj.data.materials:
            remap_material(mat.name, new_material_name)

    # 主程序
    def ReplaceTex():
        dictionary_path = os.path.join(dir_path, "RenameList.txt")
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                if obj.name == "身体_mesh":
                    process_body(obj, dictionary_path)
                elif obj.name in ["口腔_mesh", "眉毛_mesh"]:
                    replace_materials(obj, "脸prep")
                elif obj.name == "头发_mesh":
                    replace_materials(obj, "头发prep")
                elif obj.name == "表情_mesh":
                    replace_materials(obj, "表情prep")
                elif obj.name == "眼睛_mesh":
                    remap_material("眼白", "脸prep")
                    remap_material("眼睛", "脸prep")
                    remap_material("目光", "脸prep")
                    remap_material("瞳孔", "脸prep")
                    remap_material("二重", "脸prep")
                    remap_material("眼睛1", "眼睛1prep")

    # 运行主程序
    ReplaceTex()

    bpy.ops.object.material_slot_remove_unused()

    def CleanSlots():
        # 对所有被选中的物体进行操作
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                # 创建一个空字典来存储已经出现过的材质和它们第一次出现时的槽位索引
                mat_dict = {}
                # 创建一个列表来存储所有需要删除的材质槽的索引
                to_remove = []
                # 获取所有的材质槽位
                mats = obj.data.materials
                # 遍历所有的材质槽位
                for i, mat in enumerate(mats):
                    if mat.name in mat_dict:
                        # 如果这个材质已经在字典中，那么我们把当前的槽位索引添加到待删除列表中
                        to_remove.append(i)
                    else:
                        # 如果这个材质不在字典中，那么我们把它和当前的槽位索引添加到字典中
                        mat_dict[mat.name] = i

                # 切换到编辑模式以便操作面
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                # 遍历所有需要删除的材质槽
                for i in to_remove:
                    # 先取消所有已选中的面
                    bpy.ops.mesh.select_all(action='DESELECT')
                    # 选中当前槽位的所有面
                    obj.active_material_index = i
                    bpy.ops.object.material_slot_select()
                    # 将这些面的槽位赋予第一次出现这个材质的槽位
                    obj.active_material_index = mat_dict[mats[i].name]
                    bpy.ops.object.material_slot_assign()
                # 切换回物体模式
                bpy.ops.object.mode_set(mode='OBJECT')
                # 删除收集到的所有重复的材质槽位
                for i in reversed(to_remove):
                    obj.active_material_index = i
                    bpy.ops.object.material_slot_remove()

    CleanSlots()

    # 检索名称为"Outline"的材质
    outline_material = bpy.data.materials.get("HoyoOutline")

    if outline_material is None:
        print("资源缺失")

    else:
        # 检索所有选中的对象
        selected_objs = bpy.context.selected_objects
        for obj in selected_objs:
            # 检查名称是否包含 "身体" 或 "头发"
            if "身体" in obj.name or "头发" in obj.name:
                # 检查对象是否已经有这个材质，如果没有就添加
                if "HoyoOutline" not in obj.data.materials:
                    obj.data.materials.append(outline_material)

    # 复制完后隐藏 Mihoyo_Carrier
    mihoyo_carrier.hide_viewport = True


# ReplaceMaterials()
