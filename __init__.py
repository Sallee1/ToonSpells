bl_info = {
    "name": "卡渲秘咒",
    "author": "Merlin", "ZGabriel"
    "version": (3, 1),
    "blender": (3, 4, 0),
    "location": "View3D > Sidebar",
    "description": "梅宝和ZG宝带给大家的卡通渲染咒语",
    "warning": "test version",
    "doc_url": "",
    "category": "Texture",
}

import bpy
import os
from bpy.types import (Panel, Operator)
from bpy.types import Operator, Menu
import sys
import importlib
from bpy.props import StringProperty

########################################################################

# dir_path = os.path.dirname(bpy.data.filepath)

# if dir_path not in sys.path:
#    sys.path.append(dir_path)

# import AppendResources
# import AddOutline
# import ToonObjects
# import MMDtoToon
# import HeadLocator
# import RegulateModel
# import MeshMaterialSorting
# import ImportMaterialPreset
# import ImportTextures
# import ReplaceTextures
# import AdjustFaceOutline

########################################################################

dir_path = os.path.dirname(os.path.realpath(__file__))

if dir_path not in sys.path:
    sys.path.append(dir_path)

import AppendResources
import AddOutline
import ToonObjects
import MMDtoToon
import HeadLocator
import RegulateModel
import SeperateMeshes
import ReplaceMaterials
import ImportTextures
import ReplaceTextures
import AdjustFaceOutline
import SdfLocator
import SdfTexture
import blender4xpatch
from constValue import *
from customExceptions import *

##################### 向Shift A菜单添加我们的节点组####################


class Add_Custom_Group(Operator):
    bl_idname = "node.add_custom_group"
    bl_label = "Add Custom Node Group"
    bl_options = {'REGISTER', 'UNDO'}

    group_name: bpy.props.StringProperty()  # 添加节点组名称的属性

    # 添加节点组的具体逻辑
    def execute(self, context):

        # 追加资源
        blend_file_path = os.path.join(dir_path, MARLIN_TOON_SHADER_FILE_NAME)
        AppendResources.append_collection_from_blend_file(blend_file_path, "Merlin Toon Carrier 3.1(不要修改)", "Merlin Toon Carrier 3.1(不要修改)")

        # 查找名为“Merlin Toon Carrier 3.1(不要修改)”的集合
        collection_name = "Merlin Toon Carrier 3.1(不要修改)"
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

        # 尝试获取指定名称的节点组
        node_group = bpy.data.node_groups.get(self.group_name)
        if node_group:
            # 获取当前节点树
            tree = context.space_data.edit_tree

            # 清除当前的节点选择
            for node in tree.nodes:
                node.select = False

            # 创建新的节点组实例
            new_node = tree.nodes.new('ShaderNodeGroup')
            new_node.node_tree = node_group
            # 放置节点在视图中心
            new_node.location = context.space_data.cursor_location

            # 设置新节点为选中状态
            new_node.select = True
            # 使新节点成为活动节点
            tree.nodes.active = new_node

            return {'FINISHED'}
        else:
            self.report({'WARNING'}, f"Node group '{self.group_name}' not found")
            return {'CANCELLED'}


# 自定义菜单类
class MERLINTOON_MT_LightModelNodes(Menu):
    bl_label = "卡渲秘咒-光照模型"
    bl_idname = "MERLINTOON_MT_LightModelNodes"

    def draw(self, context):
        self.layout.operator_context = 'INVOKE_DEFAULT'
        # 为每个节点组添加一个菜单项
        groups = ["标准二分 3.1", "有过渡的二分 3.1", "脸部sdf 3.1", "受光源影响的二分 3.1", "半调风格 3.1"]  # 假设您有多个节点组
        for group_name in groups:
            op = self.layout.operator("node.add_custom_group", text=group_name)
            op.group_name = group_name


class MERLINTOON_MT_MainNodes(Menu):
    bl_label = "卡渲秘咒-主节点"
    bl_idname = "MERLINTOON_MT_MainNodes"

    def draw(self, context):
        self.layout.operator_context = 'INVOKE_DEFAULT'
        # 为每个节点组添加一个菜单项
        groups = ["主节点 3.1", "全局光照 3.1"]  # 假设您有多个节点组
        for group_name in groups:
            op = self.layout.operator("node.add_custom_group", text=group_name)
            op.group_name = group_name


class MERLINTOON_MT_EffectNodes(Menu):
    bl_label = "卡渲秘咒-更多效果"
    bl_idname = "MERLINTOON_MT_EffectNodes"

    def draw(self, context):
        self.layout.operator_context = 'INVOKE_DEFAULT'
        # 为每个节点组添加一个菜单项
        groups = ["高光 3.1", "环境光遮蔽 3.1", "辅光 3.1", "边缘光 3.1", "动态描边 3.1"]  # 假设您有多个节点组
        for group_name in groups:
            op = self.layout.operator("node.add_custom_group", text=group_name)
            op.group_name = group_name


class MERLINTOON_MT_SpecialNodes(Menu):
    bl_label = "卡渲秘咒-特殊材质类型"
    bl_idname = "MERLINTOON_MT_SpecialNodes"

    def draw(self, context):
        self.layout.operator_context = 'INVOKE_DEFAULT'
        # 为每个节点组添加一个菜单项
        groups = ["透明 3.1", "金属效果 3.1"]  # 假设您有多个节点组
        for group_name in groups:
            op = self.layout.operator("node.add_custom_group", text=group_name)
            op.group_name = group_name

##################### 为选中物体添加梅林的卡通材质预设####################


class ToonObjectsSpell(bpy.types.Operator):
    """为选中物体添加梅林的卡通材质预设"""
    bl_idname = "toon.operator"
    bl_label = "Toon Operator"

    def execute(self, context):
        # 撤销开始
        bpy.ops.ed.undo_push(message="为选中物体添加梅林的卡通材质预设")
        try:
            ToonObjects.ToonObjects()
        except bl_Operator_Error as err:
            self.report({'ERROR'}, str(err))
        finally:
            bpy.ops.ed.undo_push(message="为选中物体添加梅林的卡通材质预设")
        # 撤销结束
        return {'FINISHED'}

##################### 为选中物体添加几何节点描边####################


class AddOutlineSpell(bpy.types.Operator):
    """为选中物体添加几何节点描边"""
    bl_idname = "outline.operator"
    bl_label = "Outline Operator"

    def execute(self, context):
        # 撤销开始
        bpy.ops.ed.undo_push(message="为选中物体添加几何节点描边")
        try:
            AddOutline.AddOutline()
        except bl_Operator_Error as err:
            self.report({'ERROR'}, str(err))
        finally:
            bpy.ops.ed.undo_push(message="为选中物体添加几何节点描边")
        # 撤销结束
        return {'FINISHED'}

##################### 去除选中物体的几何节点描边####################


class CleanOutlineSpell(bpy.types.Operator):
    """去除选中物体的几何节点描边"""
    bl_idname = "cleanoutline.operator"
    bl_label = "CleanOutline Operator"

    def execute(self, context):
        # 撤销开始
        bpy.ops.ed.undo_push(message="去除选中物体的几何节点描边")
        try:
            AddOutline.CleanOutline()
        except bl_Operator_Error as err:
            self.report({'ERROR'}, str(err))
        finally:
            bpy.ops.ed.undo_push(message="去除选中物体的几何节点描边边")
        # 撤销结束
        return {'FINISHED'}

##################### 添加SDF定位物体####################


class SdfLocatorSpell(bpy.types.Operator):
    """添加SDF定位物体"""
    bl_idname = "sdflocator.operator"
    bl_label = "SdfLocator Operator"

    def execute(self, context):
        # 撤销开始
        bpy.ops.ed.undo_push(message="添加SDF定位物体")
        try:
            SdfLocator.SdfLocator()
        except bl_Operator_Error as err:
            self.report({"ERROR"}, err.message)
        finally:
            bpy.ops.ed.undo_push(message="添加SDF定位物体")
        # 撤销结束
        return {'FINISHED'}

##################### 添加SDF材质####################


class SdfTextureSpell(bpy.types.Operator):
    """添加SDF材质"""
    bl_idname = "sdftexture.operator"
    bl_label = "SdfTexture Operator"

    def execute(self, context):
        # 撤销开始
        bpy.ops.ed.undo_push(message="添加SDF材质")
        try:
            SdfTexture.SdfTexture()
        except bl_Operator_Error as err:
            self.report({"ERROR"}, err.message)
        finally:
            bpy.ops.ed.undo_push(message="添加SDF材质")
        # 撤销结束
        return {'FINISHED'}

###################### 将MMD材质替换为通用卡渲材质#######################


class MMDtoToonSpell(bpy.types.Operator):
    """将MMD材质替换为通用卡渲材质"""
    bl_idname = "mmdtotoon.operator"
    bl_label = "MMD to Toon Operator"

    def execute(self, context):
        bpy.ops.ed.undo_push(message="将MMD材质替换为通用卡渲材质")
        try:
            MMDtoToon.MMDtoToonSpell()
        except bl_Operator_Error as err:
            self.report({"ERROR"}, err.message)
        finally:
            bpy.ops.ed.undo_push(message="将MMD材质替换为通用卡渲材质")
        return {'FINISHED'}

###################### 一键仿星铁渲染#######################


class HKSRSpell(bpy.types.Operator):
    """一键仿星铁渲染"""
    bl_idname = "hksr.operator"
    bl_label = "HKSR Operator"

    bpy.types.Scene.my_path = StringProperty(
        name="",
        description="选择材质文件夹路径",
        default="选择材质文件夹",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    def execute(self, context):
        bpy.ops.ed.undo_push(message="一键仿星铁渲染")
        try:
            HeadLocator.HeadLocator()
            RegulateModel.RegulateModel()
            SeperateMeshes.SeperateMeshes()
            ReplaceMaterials.ReplaceMaterials()
            ImportTextures.ImportTextures(bpy.context.scene.my_path)
            ReplaceTextures.ReplaceTextures()
            AdjustFaceOutline.AdjustFaceOutline()
        except bl_Operator_Error as err:
            self.report({"ERROR"}, err.message)
        finally:
            bpy.ops.ed.undo_push(message="一键仿星铁渲染")
        return {'FINISHED'}

############################## 面板################################


class MERLINTOON_PT_Root(bpy.types.Panel):
    bl_label = "卡渲秘咒"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "卡渲秘咒"

    def draw(self, context):
        layout = self.layout


class MERLINTOON_PT_BaseToon(bpy.types.Panel):
    bl_label = "基础卡渲咒"
    bl_parent_id = "MERLINTOON_PT_Root"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "卡渲秘咒"

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.operator(ToonObjectsSpell.bl_idname, text="基础卡渲咒", icon='SHADING_RENDERED')
        row = layout.row(align=True)
        row.operator(AddOutlineSpell.bl_idname, text="描边咒", icon='MESH_MONKEY')
        row.operator(CleanOutlineSpell.bl_idname, text="清除描边咒", icon='MESH_MONKEY')
        row = layout.row(align=True)
        row.operator(SdfLocatorSpell.bl_idname, text="SDF定位咒", icon='MESH_MONKEY')
        row.operator(SdfTextureSpell.bl_idname, text="SDF材质咒", icon='MESH_MONKEY')


class MERLINTOON_PT_Caterpillar(bpy.types.Panel):
    bl_label = "毛毛豆咒"
    bl_parent_id = "MERLINTOON_PT_Root"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "卡渲秘咒"

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.operator(MMDtoToonSpell.bl_idname, text="通用毛毛豆咒", icon='SHADING_RENDERED')


class MERLINTOON_PT_StarRail(bpy.types.Panel):
    bl_label = "星铁咒"
    bl_parent_id = "MERLINTOON_PT_Root"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "卡渲秘咒"

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.operator(HKSRSpell.bl_idname, text="星铁咒", icon='SHADING_RENDERED')
        layout.prop(context.scene, "my_path")  # 在面板上显示选定的路径

###################### 注册和注销#######################


classes = [
    ToonObjectsSpell,
    AddOutlineSpell,
    CleanOutlineSpell,
    MMDtoToonSpell,
    HKSRSpell,
    SdfLocatorSpell,
    SdfTextureSpell,
    MERLINTOON_PT_Root,
    MERLINTOON_PT_BaseToon,
    MERLINTOON_PT_Caterpillar,
    MERLINTOON_PT_StarRail,
    Add_Custom_Group,
    MERLINTOON_MT_LightModelNodes,
    MERLINTOON_MT_MainNodes,
    MERLINTOON_MT_EffectNodes,
    MERLINTOON_MT_SpecialNodes
]


def register():
    print(os.path.dirname(__file__))
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.NODE_MT_add.append(menu_func)
    # 4.0版本api修补
    blender4xpatch.patching()

# 将自定义菜单添加到节点编辑器


def menu_func(self, context):
    self.layout.menu(MERLINTOON_MT_LightModelNodes.bl_idname)
    self.layout.menu(MERLINTOON_MT_MainNodes.bl_idname)
    self.layout.menu(MERLINTOON_MT_EffectNodes.bl_idname)
    self.layout.menu(MERLINTOON_MT_SpecialNodes.bl_idname)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    if (getattr(bpy.types.Scene, "my_path", None)):
        del bpy.types.Scene.my_path

    bpy.types.NODE_MT_add.remove(menu_func)

#    del bpy.types.Scene.outline_thickness


if __name__ == "__main__":
    register()
