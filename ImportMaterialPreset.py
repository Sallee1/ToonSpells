import bpy

def ImportMaterialPreset():

    #############导入材质预设#############

    # 获取激活的对象
    active_obj = bpy.context.active_object

    # 选择所有你想复制修改器的对象
    bpy.ops.object.select_all(action='DESELECT')
    selected_objects = [obj for obj in bpy.context.scene.objects if "身体" in obj.name or "头发" in obj.name]
    for obj in selected_objects:
        obj.select_set(True)

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

    # 复制修改器后，我们来替换材质
    for obj in bpy.context.selected_objects:
        if obj.data.materials:
            for slot in obj.material_slots:
                if "身体1" in slot.material.name and "身体1prep" in bpy.data.materials:
                    slot.material = bpy.data.materials["身体1prep"]
                elif "身体2" in slot.material.name and "身体2prep" in bpy.data.materials:
                    slot.material = bpy.data.materials["身体2prep"]
                elif "脸" in slot.material.name and "脸prep" in bpy.data.materials:
                    slot.material = bpy.data.materials["脸prep"]
                elif "眼睛1" in slot.material.name and "眼睛1prep" in bpy.data.materials:
                    slot.material = bpy.data.materials["眼睛1prep"]
                elif "眼睛" in slot.material.name and not "眼睛1" in slot.material.name and "脸prep" in bpy.data.materials:
                    slot.material = bpy.data.materials["脸prep"]
                elif "口腔" in slot.material.name and "脸prep" in bpy.data.materials:
                    slot.material = bpy.data.materials["脸prep"]
                elif "眉毛" in slot.material.name and "脸prep" in bpy.data.materials:
                    slot.material = bpy.data.materials["脸prep"]
                elif "头发" in slot.material.name and "头发prep" in bpy.data.materials:
                    slot.material = bpy.data.materials["头发prep"]
                elif "表情" in slot.material.name and "表情prep" in bpy.data.materials:
                    slot.material = bpy.data.materials["表情prep"]
                    
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

