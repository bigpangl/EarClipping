"""
Author:     LanHao
Date:       2020/11/10
Python:     python3.6

"""
import logging
import math
import numpy as np

EPISON = 1e-5


def green_value(points):
    """
    格林公式用于判断顺时针还是逆时针

    大于0 逆时针,小于0 顺时针
    :param points:
    :return:
    """
    d = 0
    for i in range(len(points) - 1):
        d += -0.5 * (points[i][1] + points[i + 1][1]) * (points[i + 1][0] - points[i][0])
    return d


def is_convex_vertex(a: np.ndarray, b: np.ndarray, c: np.ndarray,green_value):
    """
    传入的三个点必须是二维平面中的点
    通过升维,判断该点是凸顶点与否

    需要满足逆时针给出点坐标
    :param v1:
    :param v2:
    :param v3:
    :return:
    """
    back_value = True
    crossp = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if green_value>0 and crossp >=0: # 逆时针排序且此处是凸角
        back_value = True
    elif green_value <0 and crossp<=0: # 顺时针,就要求此处原本计算是凹角
        back_value = True
    else:
        back_value = False
    return back_value


def get_cos_by(v1, v2):
    # 仅保留计算值本身的精度,不人工进行取舍

    v1_length = np.linalg.norm(v1)
    v2_length = np.linalg.norm(v2)

    assert v1_length != 0, Exception(f"计算向量角度,向量长度不可以为0,{v1}")
    assert v2_length != 0, Exception(f"计算向量角度,向量长度不可以为0,{v2}")

    return v1.dot(v2) / (v1_length * v2_length)


def get_angle_by(v1, v2):
    cos_value = get_cos_by(v1, v2)

    if cos_value > 1:
        cos_value = 1
    elif cos_value < -1:
        cos_value = -1

    return math.acos(cos_value) / math.pi * 180


def is_in_triangle(triangle: list, vertex: np.ndarray) -> int:
    back = 0

    v1 = triangle[0] - vertex
    v2 = triangle[1] - vertex
    v3 = triangle[2] - vertex
    angle1 = get_angle_by(v1, v2)
    angle2 = get_angle_by(v2, v3)
    angle3 = get_angle_by(v3, v1)
    # logging.debug(f"angle1:{angle1},angle2:{angle2},angle3:{angle3}")
    angles_all = angle1 + angle2 + angle3
    # logging.debug(f"angle_all:{angles_all}")
    if angle1 == 180 or angle2 == 180 or angle3 == 180:
        back = 0
    else:
        if abs((360 - angles_all)) <= EPISON:  # 误差判断
            back = -1
        else:
            back = 1

    return back


class Plane:
    u_bais: np.ndarray  # x 轴单位长度
    v_bais: np.ndarray  # y 轴单位长度
    origin: np.ndarray  # 中心点
    normal: np.ndarray  # 法向量

    def __init__(self, uBais: np.ndarray, vBais: np.ndarray, origin: np.ndarray):
        self.u_bais = uBais / np.linalg.norm(uBais)
        self.v_bais = vBais / np.linalg.norm(vBais)
        v1_length = np.linalg.norm(self.u_bais)
        v2_length = np.linalg.norm(self.v_bais)
        cos_value = self.u_bais.dot(self.v_bais) / (v1_length * v2_length)
        if abs(cos_value) > EPISON:
            raise Exception(f"平面中指定的UV 向量夹角不为90°,cos value 为:{cos_value}")
        self.origin = origin
        self.normal = np.cross(self.u_bais, self.v_bais)
        self.normal = self.normal / np.linalg.norm(self.normal)  # 单位向量,便于后面计算距离

    def distance(self, vertex: np.ndarray):
        """
        计算点到平面的距离
        :param vertex:
        :return:
        """
        value = np.dot(self.normal, (vertex - self.origin))
        return [0, value][abs(value) > EPISON]

    def uv(self, vertex: np.ndarray) -> np.ndarray:
        """
        将三维坐标转换成2维坐标,前提是这个点在平面内部,此处是否需要进行判断呢?
        :param vertex:
        :return:
        """
        distance = self.distance(vertex)
        if distance == 0:
            vertex_n = vertex - self.origin
            u = np.dot(vertex_n, self.u_bais)
            v = np.dot(vertex_n, self.v_bais)
            return np.asarray([u, v])
        else:
            raise Exception(f"点{vertex} 不在平面内:{distance}")

    def to_xyz(self, vertex: np.ndarray) -> np.ndarray:
        return self.origin + self.u_bais * vertex[0] + self.v_bais * vertex[1]


class SingleLinkNode:
    """
    单向链表
    """
    vertex: np.ndarray  # 顶点
    next_node: "SingleLinkNode" = None  #

    def __init__(self, vertex: np.ndarray):
        self.vertex = vertex


def clipping(vertices: list):
    """
    耳裁法,分割各个三角形
    :param vertices:
    :return:
    """
    # 构建单向链表
    green_value_get = green_value(vertices)
    link_head = SingleLinkNode(vertices[0])
    link_end: SingleLinkNode

    last_node = link_head
    for i in range(1, len(vertices)):
        link_end = SingleLinkNode(vertices[i])
        last_node.next_node = link_end
        last_node = link_end
    # 此时link_head 表示单链head,link_end 表示单链尾部
    triangles_back = []  # 需要返回的三角形
    node_current = link_head
    while node_current:
        node_next = node_current.next_node
        node_next_agin = node_current.next_node and node_current.next_node.next_node  # 内含and 判断省去if else
        v1 = node_current.vertex
        v2 = node_next and node_next.vertex
        v3 = node_next_agin and node_next_agin.vertex
        if v1 is not None and v2 is not None and v3 is not None:
            v_1 = v1 - v2
            v_2 = v3 - v2
            if np.linalg.norm(np.cross(v_2, v_1)) == 0:  # 三点共线
                node_next.next = node_next_agin.next_node
                node_next_agin.next_node = None
                continue
            convex_status = is_convex_vertex(v1, v2, v3,green_value_get)
            if convex_status:  # 凸角
                # 判断其他点是否在这个三角形内部
                status = True
                next_in_triangle_check = node_next_agin and node_next_agin.next_node
                while next_in_triangle_check:
                    vertex_check_current = next_in_triangle_check.vertex
                    in_triangle_status = is_in_triangle([v1, v2, v3], vertex_check_current)
                    if in_triangle_status <= 0:
                        status = False
                        break
                    next_in_triangle_check = next_in_triangle_check.next_node
                if status:
                    triangles_back.append([v1, v2, v3])
                    node_current.next_node = node_next_agin
                    node_next.next_node = None
                    continue
            node_current.next_node = None
            link_end.next_node = node_current
            link_end = node_current
            node_current = node_next
        else:
            break
    return triangles_back
