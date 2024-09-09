from bpy.types import GeometryNodeTree
from bpy.types import NodeTreeInterfaceSocket


def patching():
    # 4.2几何节点修补

    # 修补GeometryNodeTree，将input重定向到interface接口上
    @property
    def inputs(tree):
        # 通过in_out属性区分输入输出
        # 目前blender版本的输入输出是按顺序排列的，暂且不需要刻意排序
        return [
            s
            for s in tree.interface.items_tree
            if s.in_out == "INPUT"
        ]
    if (getattr(GeometryNodeTree, "inputs", None)):
        GeometryNodeTree.inputs = inputs

    # 修补GeometryNodeTree，将output重定向到interface接口上
    @property
    def outputs(tree):
        # 通过in_out属性区分输入输出
        # 目前blender版本的输入输出是按顺序排列的，暂且不需要刻意排序
        return [
            s
            for s in tree.interface.items_tree
            if s.in_out == "OUTPUT"
        ]
    if (getattr(GeometryNodeTree, "outputs", None)):
        GeometryNodeTree.outputs = outputs

    # 修补NodeTreeInterfaceSocket，将type重定向到socket_type
    @property
    def socket_type(interface_socket):
        # 旧版api类型为全大写字符串，如"FLOAT"
        # 新版api类型会有NodeSocket前缀，且使用驼峰，如"NodeSocketFloat"
        bl4x_type: str = interface_socket.socket_type
        bl3x_type: str = bl4x_type.replace("NodeSocket", "")
        bl3x_type.upper()
        return bl3x_type
    if (getattr(NodeTreeInterfaceSocket, "type", None)):
        NodeTreeInterfaceSocket.type = socket_type
