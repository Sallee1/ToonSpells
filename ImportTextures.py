import bpy
import os
from customExceptions import *
############# 导入准备好的贴图#############


def ImportTextures(path):
    # 指定图片文件夹的路径
    image_dir = path
    if (not os.path.exists(image_dir)):
        raise bl_Operator_Error(f"指定的图片文件夹{image_dir}不存在！")
    # 遍历指定文件夹中的所有文件
    for filename in os.listdir(image_dir):
        # 检查文件是否是图片文件，根据需要添加或修改文件扩展名
        if filename.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.tga')):
            # 获取图片的完整路径
            image_path = os.path.join(image_dir, filename)
            # 为图片名添加 'ZG_' 前缀以保证其唯一性
            unique_img_name = f"ZG_{filename}"
            # 加载图片到Blender，如果已存在同名图片则不进行检查
            bpy.data.images.load(image_path, check_existing=False).name = unique_img_name
