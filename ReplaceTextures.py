import bpy
import os
import sys

###################################################################
#dir_path = os.path.dirname(bpy.data.filepath)

#if dir_path not in sys.path:
#    sys.path.append(dir_path)

###################################################################

dir_path = os.path.dirname(os.path.realpath(__file__))

if dir_path not in sys.path:
    sys.path.append(dir_path)

##################################################################

def ReplaceTextures():

    #############将准备好的材质替换到正确位置############

    # 定义原始图片名与新图片名的部分的映射关系
    image_mapping = {
        "头发_prep": "ZG_头发",
        "头发光照_prep": "Hair_LightMap",
        "头发冷ramp_prep": "Hair_Cool_Ramp",
        "头发暖ramp_prep": "Hair_Warm_Ramp",
        "脸_prep": "ZG_脸",
        "脸光照_prep": "FaceMap",
        "表情_prep": "ZG_表情",
        "身体1_prep": "ZG_身体1",
        "身体2_prep": "ZG_身体2",
        "身体1内侧_prep": "ZG_身体1内侧",
        "身体2内侧_prep": "ZG_身体2内侧",
        "身体1光照_prep": "Body1_LightMap",
        "身体2光照_prep": "Body2_LightMap",
        "身体1丝袜_prep": "Body1_Stockings",
        "身体2丝袜_prep": "Body2_Stockings",
        "身体冷ramp_prep": "Body_Cool_Ramp",
        "身体暖ramp_prep": "Body_Warm_Ramp"
    }

    # 先读取txt文件
    dictionary_path=os.path.join(dir_path,"RenameList.txt")
    with open(dictionary_path, 'r') as file:
        lines = file.readlines()

    # 获取需要替换成 "ZG_身体2内侧" 的字符串列表
    replace_to_body2_back_list = [s.strip() for s in lines[0].split(',')]
    # 获取需要替换成 "ZG_身体2" 的字符串列表
    replace_to_body2_list = [s.strip() for s in lines[1].split(',')]
    # 获取需要替换成 "ZG_身体1内侧" 的字符串列表
    replace_to_body1_back_list = [s.strip() for s in lines[2].split(',')]
    # 获取需要替换成 "ZG_身体1" 的字符串列表
    replace_to_body1_list = [s.strip() for s in lines[3].split(',')]
    # 获取需要替换成 "ZG_脸" 的字符串列表
    replace_to_face_list = [s.strip() for s in lines[4].split(',')]
    # 获取需要替换成 "ZG_头发" 的字符串列表
    replace_to_hair_list = [s.strip() for s in lines[5].split(',')]
    # 获取需要替换成 "ZG_表情" 的字符串列表
    replace_to_bq_list = [s.strip() for s in lines[6].split(',')]
    
    # 遍历所有名字包含“ZG_”的images
    for image in bpy.data.images:
        if "ZG_" in image.name:
            # 按规则修改图片名称的某一部分
            if "Body_LightMap" in image.name:
                image.name = image.name.replace("Body_LightMap", "Body1_LightMap")
            elif "Body_Stockings" in image.name:
                image.name = image.name.replace("Body_Stockings", "Body2_Stockings")
            elif "00_Cool_Ramp" in image.name:
                image.name = image.name.replace("00_Cool_Ramp", "00_Body_Cool_Ramp")
            elif "00_Warm_Ramp" in image.name:
                image.name = image.name.replace("00_Warm_Ramp", "00_Body_Warm_Ramp")
            # 检查该图像名是否需要替换
            for old_str in replace_to_body2_back_list:
                if old_str in image.name and "身体" not in image.name:
                    image.name = image.name.replace(old_str, "身体2内侧")        
            for old_str in replace_to_body2_list:
                if old_str in image.name and "身体" not in image.name:
                    image.name = image.name.replace(old_str, "身体2")
            for old_str in replace_to_body1_back_list:
                if old_str in image.name and "身体" not in image.name:
                    image.name = image.name.replace(old_str, "身体1内侧")
            for old_str in replace_to_body1_list:
                if old_str in image.name and "身体" not in image.name:
                    image.name = image.name.replace(old_str, "身体1")
            for old_str in replace_to_face_list:
                if old_str in image.name and "脸" not in image.name:
                    image.name = image.name.replace(old_str, "脸")
            for old_str in replace_to_hair_list:
                if old_str in image.name and "头发" not in image.name:
                    image.name = image.name.replace(old_str, "头发")
            for old_str in replace_to_bq_list:
                if old_str in image.name and "表情" not in image.name:
                    image.name = image.name.replace(old_str, "表情")
                    
    # 创建一个字典来保存旧图片的颜色空间设置
    color_spaces = {}

    # 定义一个函数，检查特定名称的图片是否存在
    def image_exists(image_name):
        for image in bpy.data.images:
            if image_name in image.name:
                return True
        return False

    # 首先，创建一张黑色图片，并命名为"temp_backup"
    bpy.ops.image.new(name="temp_backup", width=1024, height=1024, color=(0, 0, 0, 1))

    # 遍历 Blender 中的所有图片
    for old_image in bpy.data.images:
        # 如果图片名在映射字典中
        if old_image.name in image_mapping.keys():
            new_image_name_part = image_mapping[old_image.name]
            # 保存旧图片的颜色空间设置
            color_spaces[old_image.name] = old_image.colorspace_settings.name
            # 找到与新图片名部分匹配的图片
            for possible_new_image in bpy.data.images:
                # 如果新图片名部分在可能的新图片的名称中
                if new_image_name_part in possible_new_image.name:
                    # remap user
                    bpy.data.images[old_image.name].user_remap(bpy.data.images[possible_new_image.name])
                    # 将旧图片的颜色空间设置复制到新图片
                    possible_new_image.colorspace_settings.name = color_spaces[old_image.name]
                    break
            # 如果是身体1内侧_prep或身体2内侧_prep，并且没有对应的新图片，则remap user到包含"ZG_身体1"或"ZG_身体2"的图片
            if old_image.name in ["身体1内侧_prep", "身体2内侧_prep"] and not image_exists(new_image_name_part):
                remap_image_name_part = "ZG_身体1" if old_image.name == "身体1内侧_prep" else "ZG_身体2"
                for possible_new_image in bpy.data.images:
                    if remap_image_name_part in possible_new_image.name:
                        # remap user
                        bpy.data.images[old_image.name].user_remap(bpy.data.images[possible_new_image.name])
                        # 将旧图片的颜色空间设置复制到新图片
                        possible_new_image.colorspace_settings.name = color_spaces[old_image.name]
                        break
            # 如果旧图片是“身体1丝袜_prep”或“身体2丝袜_prep”，并且没有对应的新图片，则remap user到“temp_backup”，并复制旧图片的颜色空间设置
            if old_image.name in ["身体1丝袜_prep", "身体2丝袜_prep"] and not image_exists(new_image_name_part):
                # remap user to "temp_backup"
                bpy.data.images[old_image.name].user_remap(bpy.data.images["temp_backup"])
                # 将旧图片的颜色空间设置复制到新图片
                bpy.data.images["temp_backup"].colorspace_settings.name = color_spaces[old_image.name]

