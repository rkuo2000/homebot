from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

# 建立 3D 圖形
fig = plt.figure()
ax = fig.gca(projection='3d')

# 產生測試資料
X, Y, Z = axes3d.get_test_data(0.05)

# 繪製 Wireframe 圖形
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

# 顯示圖形
plt.show()
