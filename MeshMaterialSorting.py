import bpy
import os #获取图片名称用
import re #重命名网格用

###################################################################

def MeshMaterialSorting():

    ###################################################################

    #存储mesh最初的名字
    global initial_object_name

    initial_object_name = ""

    def separate_by_material():
        global initial_object_name

        # 获取当前选中的物体
        obj = bpy.context.object
        if not obj or obj.type != 'MESH':
            print("没有选中的网格物体")
            return
        
        # 存储mesh最初的名字
        initial_object_name = obj.name

    ###############按材质拆分mesh###############
        
        # 获取材质数量
        total_materials = len(obj.data.materials)

        # 进入编辑模式
        bpy.ops.object.mode_set(mode='EDIT') 
        # 取消选择所有面
        bpy.ops.mesh.select_all(action='DESELECT')

        # 处理每个材质
        for mat_index in range(total_materials):
            # 进入对象模式
            bpy.ops.object.mode_set(mode='OBJECT')

            # 选择使用当前材质的面
            for poly in obj.data.polygons:
                poly.select = (poly.material_index == mat_index)

            # 进入编辑模式并分离选择的面
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.separate(type='SELECTED')
            # 取消选择所有面
            bpy.ops.mesh.select_all(action='DESELECT')

        # 返回对象模式
        bpy.ops.object.mode_set(mode='OBJECT')

        # 清除所有选中（新创建的）物体的未使用材质
        for obj in bpy.context.selected_objects:
            used_materials = {poly.material_index for poly in obj.data.polygons}
            obj.data.materials.update()

            unused_materials = [i for i, mat in enumerate(obj.data.materials) if i not in used_materials]
            for i in sorted(unused_materials, reverse=True): 
                obj.data.materials.pop(index=i)
            
            # 如果物体没有面，删除物体
            if len(obj.data.polygons) == 0:
                bpy.data.objects.remove(obj)
            else:
                # 检查物体的材质中“mmd_base_tex”节点使用的图片名称，如果名称包含“内侧”，则删除这个物体
                for mat in obj.data.materials:
                    # 获取 "mmd_base_tex" 节点
                    tex_node = mat.node_tree.nodes.get("mmd_base_tex")
                    if tex_node is not None:
                        # 如果该节点的图片名包含“内侧”，则删除这个物体
                        if "内侧" in tex_node.image.name:
                            bpy.data.objects.remove(obj)
                            break


    # 运行函数
    separate_by_material()

    ###############按贴图合并mesh###############

    def merge_by_texture():
        
        # 获取当前选中的物体（应该是我们分离的原始物体）
        obj = bpy.context.object

        # 字典用于按图像名称存储物体
        obj_dict = {}

        # 处理每个物体
        for obj in bpy.context.selected_objects:
            # 如果物体没有材质，则跳过
            if not obj.data.materials:
                continue
            
            # 假设第一个材质是我们要处理的材质
            mat = obj.data.materials[0]
            mmd_base_tex_node = next((node for node in mat.node_tree.nodes if node.type == 'TEX_IMAGE' and node.name == 'mmd_base_tex'), None)

            # 如果没有'mmd_base_tex'节点或图像为空，则跳过
            if mmd_base_tex_node is None or mmd_base_tex_node.image is None:
                continue

            # 获取图像名称
            img_name = mmd_base_tex_node.image.name

            # 将物体添加到列表中
            if img_name in obj_dict:
                obj_dict[img_name].append(obj)
            else:
                obj_dict[img_name] = [obj]

        # 按图像合并物体
        for img_name, objs in obj_dict.items():
            # 如果图像名称包含"脸.png"，则跳过
            print(img_name)
            
            if "脸.png" in img_name:
                continue

            # 跳过单个物体
            if len(objs) <= 1:
                continue
            
            # 选择物体
            bpy.ops.object.select_all(action='DESELECT')
            for obj in objs:
                obj.select_set(True)
            
            # 设置活动物体
            bpy.context.view_layer.objects.active = objs[0]

            # 合并物体
            bpy.ops.object.join()

    # 运行函数
    merge_by_texture()

    ##############分别合并口腔和眼睛###############

    def merge_by_material_name(material_names):
        # 获取所有物体
        all_objects = bpy.context.scene.objects

        # 存储使用指定材质的物体的列表
        obj_list = []

        # 处理每个物体
        for obj in all_objects:
            # 如果物体未被选择或没有材质，则跳过
            if not obj.select_get() or not obj.data.materials:
                continue
            
            # 检查材质名称是否在列表中
            for mat in obj.data.materials:
                # 如果材质名称包含任何material_names中的名称，则将物体添加到列表中
                if any(name in mat.name for name in material_names):
                    obj_list.append(obj)
                    break
            
        # 如果列表中只有一个或没有物体，则跳过
        if len(obj_list) <= 1:
            return

        # 选择物体
        bpy.ops.object.select_all(action='DESELECT')
        for obj in obj_list:
            obj.select_set(True)
        
        # 设置活动物体
        bpy.context.view_layer.objects.active = obj_list[0]

        # 合并物体
        bpy.ops.object.join()


    # 使用两组材质名称运行函数

    # 选择所有具有原始物体名称的物体
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if initial_object_name in obj.name:
            obj.select_set(True)

    merge_by_material_name(["口腔", "舌头", "牙齿"])

    # 选择所有具有原始物体名称的物体
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if initial_object_name in obj.name:
            obj.select_set(True)

    merge_by_material_name(["眼白", "眼睛", "眼睛1","目光"])

    ##############删除没有用的材质###############

    def remove_extra_materials():
        # 处理每个物体
        for obj in bpy.context.selected_objects:
            if obj.type != 'MESH' or len(obj.data.materials) <= 1:
                continue

            # 保留材质名称中包含"眼"的材质
            materials_to_keep = [mat for mat in obj.data.materials if "眼睛" in mat.name]
            
            # 如果没有名称中包含"眼"的材质，则保留第一个材质
            if not materials_to_keep:
                materials_to_keep.append(obj.data.materials[0])
                
            # 倒序删除其余的材质
            for mat_index in reversed(range(len(obj.data.materials))):
                if obj.data.materials[mat_index] not in materials_to_keep:
                    obj.data.materials.pop(index=mat_index)

    # 用名字检索选中所有分离出的mesh
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if initial_object_name in obj.name:
            obj.select_set(True)
            
    remove_extra_materials()

    def merge_by_material_name_excluding_keywords(keywords):
        # 获取所有物体
        all_objects = bpy.context.scene.objects

        # 存储使用指定材质的物体的列表
        obj_list = []

        # 处理每个物体
        for obj in all_objects:
            # 如果物体未被选择或没有材质，则跳过
            if not obj.select_get() or not obj.data.materials:
                continue
            
            # 检查材质名称是否在列表中
            for mat in obj.data.materials:
                # 如果材质名称中包含任何关键词，则跳过此物体
                if any(keyword in mat.name for keyword in keywords):
                    break
            else:
                # 如果材质名称不包含任何关键词，则将物体添加到列表中
                obj_list.append(obj)

        # 如果列表中只有一个或没有物体，则跳过
        if len(obj_list) <= 1:
            return

        # 选择物体
        bpy.ops.object.select_all(action='DESELECT')
        for obj in obj_list:
            obj.select_set(True)
        
        # 设置活动物体
        bpy.context.view_layer.objects.active = obj_list[0]

        # 合并物体
        bpy.ops.object.join()

    # 使用关键词运行函数
    merge_by_material_name_excluding_keywords(["头发", "眼", "眉毛", "表情", "牙齿", "舌头", "口腔"])

    ##############删除没有用的材质###############

    # 用名字检索选中所有分离出的mesh
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if initial_object_name in obj.name:
            obj.select_set(True)

    # 创建一个包含所有选定物体的列表
    selected_objects = list(bpy.context.selected_objects)

    # 遍历列表
    for obj in selected_objects:
        # 从物体的名字中移除最后4个字符（".xxx"）
        obj.name = obj.name[:-4]

        # 根据材质名添加后缀
        for mat in obj.data.materials:
            if "脸" in mat.name:
                obj.name += "_身体"
                break
            elif "眼睛" in mat.name:
                obj.name += "_眼睛"
                break
            elif any(substring in mat.name for substring in ["牙齿", "舌头", "口腔"]):
                obj.name += "_口腔"
                break
            elif "眉毛" in mat.name:
                obj.name += "_眉毛"
                break
            elif "表情" in mat.name:
                obj.name += "_表情"
                break
            elif "头发" in mat.name:
                obj.name += "_头发"
                break

    #############重命名保留的材质###############

        # 再次遍历材质以重命名它们
        if "_身体" in obj.name:
            for mat in obj.data.materials:
                if "脸" not in mat.name:
                    # 获取“mmd_base_tex”节点
                    tex_node = mat.node_tree.nodes.get("mmd_base_tex")
                    if tex_node is not None:
                        # 如果该节点的图片名为“衣服”，则将材质名改为“身体1”
                        if tex_node.image.name == "衣服.png" or tex_node.image.name == "衣服.jpg":
                            mat.name = "身体1"
                        else:
                            mat.name = "身体2"
                    else:
                        print(f"在材质 {mat.name} 中找不到 mmd_base_tex 节点")
        elif "_口腔" in obj.name:
            for mat in obj.data.materials:
                mat.name = "口腔"