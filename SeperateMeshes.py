import bpy

def SeperateMeshes():

    def select_faces_by_material(obj, mat_names):
        # 切换到编辑模式
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        # 取消所有的选择
        bpy.ops.mesh.select_all(action='DESELECT')

        # 切换到面选择模式
        bpy.ops.mesh.select_mode(type="FACE")

        # 遍历材质插槽，如果插槽名称在给定的材质名称列表中，则设置为活动插槽并选择所有面
        for i, slot in enumerate(obj.material_slots):
            if slot.name in mat_names:
                obj.active_material_index = i
                bpy.ops.object.material_slot_select()

        # 检查是否有任何面被选中，只有在有面被选中时才进行分离操作
        if bpy.context.tool_settings.mesh_select_mode[2] and bpy.context.object.data.total_face_sel > 0:
            # 分离选择的面
            bpy.ops.mesh.separate(type='SELECTED')

        # 切换回到物体模式
        bpy.ops.object.mode_set(mode='OBJECT')



    # 指定要使用的材质名称
    mat_groups = [
        ["眉毛"],
        ["牙齿", "舌头", "口腔"],
        ["头发","馬尾"],
        ["表情"],
        ["眼睛", "眼睛1", "眼白","目光","瞳孔","二重"]
    ]

    # 保存原始活动对象
    original_obj = bpy.context.active_object

    # 对于每一组材质名称，选择并分离面
    for mat_names in mat_groups:
        select_faces_by_material(original_obj, mat_names)

    # 切换回原始活动对象
    bpy.context.view_layer.objects.active = original_obj

    bpy.ops.object.material_slot_remove_unused()

    # 材质名称到物体名称的映射
    material_to_object_name = {
        "脸": "身体_mesh",
        "眉毛": "眉毛_mesh",
        "头发": "头发_mesh",
        "表情": "表情_mesh",
        "口腔": "口腔_mesh",
        "眼睛": "眼睛_mesh"
    }

    # 获取所有选中的物体
    selected_objects = bpy.context.selected_objects

    # 遍历所有选中的物体
    for obj in selected_objects:
        # 如果物体类型是MESH
        if obj.type == 'MESH':
            # 遍历物体的所有材质插槽
            for slot in obj.material_slots:
                # 如果插槽的材质名称在映射字典中
                if slot.name in material_to_object_name:
                    # 将物体名称设置为映射字典中的值
                    obj.name = material_to_object_name[slot.name]
                    
#SeperateMeshes()