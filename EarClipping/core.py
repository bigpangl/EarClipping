"""
Author:     LanHao
Date:       2020/11/10
Python:     python3.6

"""

import numpy as np

EPISON = 1e-5


def is_convex_vertex(v1: np.ndarray, v2: np.ndarray, v3: np.ndarray):
    """
    传入的三个点必须是二维平面中的点

    通过升维,判断该点是凸顶点与否
    :param v1:
    :param v2:
    :param v3:
    :return:
    """
    v_front = v1 - v2
    v_back = v3 - v2
    v_front = np.r_[v_front, 0]
    v_back = np.r_[v_back, 0]
    normal = np.cross(v_back, v_front)
    return True if normal[2] == 1 else False


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
        if abs(cos_value)>EPISON:
            raise  Exception(f"平面中指定的UV 向量夹角不为90°,cos value 为:{cos_value}")
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
            vertex_n = vertex-self.origin
            u = np.dot(vertex_n,self.u_bais)
            v = np.dot(vertex_n,self.v_bais)
            return np.asarray([u,v])
        else:
            raise Exception(f"点{vertex} 不在平面内:{distance}")

    def to_xyz(self,vertex:np.ndarray)->np.ndarray:
        return self.origin + self.u_bais * vertex[0]+ self.v_bais*vertex[1]