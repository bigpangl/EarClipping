"""
Author:     LanHao
Date:       2020/11/10
Python:     python3.6

"""
import logging
import numpy as np

from EarClipping.core import Plane3D, clip

logging.basicConfig(level=logging.DEBUG)

points = [{"x": 0, "y": 0, "z": 0}, {"x": 0, "y": 0, "z": 257}, {"x": 0, "y": 480, "z": 257},
          {"x": 0, "y": 480, "z": 424}, {"x": 0, "y": 740, "z": 424},
          {"x": 0, "y": 740, "z": 591}, {"x": 0, "y": 1000, "z": 591},
          {"x": 0, "y": 1000, "z": 757}, {"x": 0, "y": 1260, "z": 757},
          {"x": 0, "y": 1260, "z": 924}, {"x": 0, "y": 1520, "z": 924},
          {"x": 0, "y": 1520, "z": 1091}, {"x": 0, "y": 1780, "z": 1091},
          {"x": 0, "y": 1780, "z": 1257}, {"x": 0, "y": 2040, "z": 1257},
          {"x": 0, "y": 2040, "z": 1424}, {"x": 0, "y": 2300, "z": 1424},
          {"x": 0, "y": 2300, "z": 1590}, {"x": 0, "y": 2780, "z": 1590},
          {"x": 0, "y": 2780, "z": 1422}, {"x": 0, "y": 2520, "z": 1422},
          {"x": 0, "y": 300, "z": 0}]

u_bas = np.asarray([0, 1, 0])
v_bas = np.asarray([0, 0, 1])
origin = np.asarray([0, 0, 0])

plane = Plane3D(u_bas, v_bas, origin)
point_np_all = []
for point in points:
    point_tmp = np.asarray([point["x"], point["y"], point["z"]])
    uv = plane.project(point_tmp)
    # print(f"{point_tmp}:{uv}")
    point_np_all.append([uv.U,uv.V])
print(point_np_all)
#
# # print(green_value(point_np_all))
#
# # print(point_np_all)
# data = clipping(point_np_all)
# for triangle in data:
#     print(plane.to_xyz(triangle[0]))
#     print(plane.to_xyz(triangle[1]))
#     print(plane.to_xyz(triangle[2]))
