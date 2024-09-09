import bpy
import os

##########################检索场景中是否有指定集合，没有的话从备用资源调取并添加它##########################################

def append_collection_from_blend_file(filepath, check_collection_name, append_collection_name, exclude=False):
    # 检查是否存在名称为check_collection_name的集合
    if check_collection_name in bpy.data.collections:
        print(f"Collection {check_collection_name} already exists, skipping append operation.")
        return  # 如果已存在该集合，直接返回，不进行后续操作
    else:
        # 如果没有找到check_collection_name，那么从指定的blend文件中追加集合collection_name
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.collections = [append_collection_name]

        # 如果追加成功，链接到当前的场景
        for collection in data_to.collections:
            if collection is not None:
                bpy.context.scene.collection.children.link(collection)
                # 如果exclude参数为True，排除该集合
                if exclude:
                    for view_layer in bpy.context.scene.view_layers:
                        view_layer.layer_collection.children[collection.name].exclude = True




