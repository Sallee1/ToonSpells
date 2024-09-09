import bpy

##############调整脸部描边厚度###############

def AdjustFaceOutline():
    
    ##############找到脸部的顶点，调整这些顶点的挤出程度###############

    def select_and_assign(mesh, material_name, group_name):
        # 切换到物体模式
        bpy.ops.object.mode_set(mode='OBJECT')

        # 为物体创建一个顶点组
        group = mesh.vertex_groups.new(name=group_name) if group_name not in mesh.vertex_groups else mesh.vertex_groups[group_name]
        
        # 遍历材质槽
        for i, mat in enumerate(mesh.data.materials):
            if mat.name == material_name:
                # 切换到编辑模式以便操作面
                bpy.ops.object.mode_set(mode='EDIT')
                # 清除所有选中
                bpy.ops.mesh.select_all(action='DESELECT')
                # 选中对应材质槽的面
                mesh.active_material_index = i
                bpy.ops.object.material_slot_select()
                # 切换回物体模式
                bpy.ops.object.mode_set(mode='OBJECT')
                # 将选中的面的顶点添加到顶点组
                for poly in mesh.data.polygons:
                    if poly.select:
                        for v in poly.vertices:
                            group.add([v], 1.0, 'ADD')
                # 清除所有选中
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')

    # 遍历所有物体
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and "mesh" in obj.name:
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)

            # 如果名字包含mesh，调整修改器设置
            # 遍历所有的修改器，找到 Armature Deform 修改器
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE':
                    # 勾选 'Preserve Volume' 选项
                    mod.use_deform_preserve_volume = True

            # 添加 Corrective Smooth 修改器，并把它调整到第二位
            new_mod = obj.modifiers.new(name="CorrectiveSmooth", type='CORRECTIVE_SMOOTH')
            while obj.modifiers.find(new_mod.name) > 1:
                bpy.ops.object.modifier_move_up(modifier=new_mod.name) 
            
            # 勾选 Pin Boundaries 选项
            new_mod.use_pin_boundary = True

            # 如果名字中包含 "mesh_身体" ,调整脸部描边厚度
            if "身体_mesh" in obj.name:
                # 创建新的顶点组"OutlineExcluded"
                if "描边权重" not in obj.vertex_groups:
                    group = obj.vertex_groups.new(name="描边权重")
                else:
                    group = obj.vertex_groups["描边权重"]

                # 找到所有使用"脸prep"材质的面并选中
                select_and_assign(obj, "脸prep", "描边权重")


