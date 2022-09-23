import matplotlib.pyplot as plt
import numpy as np

# 建立 3D 圖形
fig = plt.figure()
ax = fig.gca(projection='3d')

# 產生格點資料
x, y, z = np.meshgrid(np.arange(-0.8, 1, 0.2),
                      np.arange(-0.8, 1, 0.2),
                      np.arange(-0.8, 1, 0.8))

# 產生向量場資料
u = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
v = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
w = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) *
     np.sin(np.pi * z))

# 繪製向量場
ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True)

# 顯示圖形
plt.show()
