import numpy as np
import matplotlib.pyplot as plt

# 建立 3D 圖形
fig = plt.figure()
ax = fig.gca(projection='3d')

# 產生 3D 座標資料
z = np.linspace(0, 15, 100)
x = np.sin(z)
y = np.cos(z)

# 繪製 3D 曲線
ax.plot(x, y, z, color='gray', label='My Curve')

# 產生 3D 座標資料
x2 = np.sin(z) + 0.1 * np.random.randn(100)
y2 = np.cos(z) + 0.1 * np.random.randn(100)

# 繪製 3D 座標點
ax.scatter(x2, y2, z, c=z, cmap='jet', label='My Points')

# 顯示圖例
ax.legend()

# 顯示圖形
plt.show()
