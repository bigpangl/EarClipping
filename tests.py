"""
Author:     LanHao
Date:       2020/11/10
Python:     python3.6

"""

import numpy as np

from EarClipping.core import Plane


u_bas = np.asarray([1,0,0])
v_bas = np.asarray([0,1,0])
origin = np.asarray([1,1,1])
plane = Plane(u_bas,v_bas,origin)
uv_need = np.asarray([2,2,1])
uv = plane.uv(uv_need)
print(uv)
print(plane.to_xyz(uv))