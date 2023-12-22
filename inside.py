from shapely.geometry import Polygon, Point
import numpy as np
from scipy.optimize import minimize

def max_inscribed_rect(poly):
    def objective(params):
        x, y, theta, w, h = params
        rect = Polygon([(x + w * np.cos(theta), y + w * np.sin(theta)),
                        (x + w * np.cos(theta) - h * np.sin(theta), y + w * np.sin(theta) + h * np.cos(theta)),
                        (x - h * np.sin(theta), y + h * np.cos(theta)),
                        (x, y)])
        intersection = poly.intersection(rect)
        return -intersection.area  # maximize the area of the intersection

    bounds = [(poly.bounds[0], poly.bounds[2]), (poly.bounds[1], poly.bounds[3]), (0, np.pi), (0, poly.length / 2), (0, poly.length / 2)]

    initial_guess = [poly.centroid.x, poly.centroid.y, 0, poly.length / 4, poly.length / 4]

    result = minimize(objective, initial_guess, bounds=bounds)
    x, y, theta, w, h = result.x

    inscribed_rect = Polygon([(x + w * np.cos(theta), y + w * np.sin(theta)),
                              (x + w * np.cos(theta) - h * np.sin(theta), y + w * np.sin(theta) + h * np.cos(theta)),
                              (x - h * np.sin(theta), y + h * np.cos(theta)),
                              (x, y)])

    return inscribed_rect
import matplotlib.pyplot as plt

# 绘制原始四边形和最大内切四边形并保存为图像
def plot_polygons(poly1, poly2, output_filename):
    x1, y1 = poly1.exterior.xy
    x2, y2 = poly2.exterior.xy

    fig, ax = plt.subplots()
    ax.plot(x1, y1, label='Original Polygon', linewidth=2, color='blue')
    ax.plot(x2, y2, label='Max Inscribed Rectangle', linewidth=2, color='red', linestyle='--')

    ax.legend()
    ax.set_aspect('equal', adjustable='datalim')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Original Polygon and Max Inscribed Rectangle')

    # 保存为图像文件
    plt.savefig(output_filename)
    plt.close()

# 调用函数绘制图像

# 示例
# 创建一个不规则四边形
vertices = np.array([(0, 0), (2, 0), (3, 1), (1, 2)])
poly = Polygon(vertices)

# 计算最大内切四边形
inscribed_rect = max_inscribed_rect(poly)
# 调用函数并保存图像
output_filename = 'output_image.png'
plot_polygons(poly, inscribed_rect, output_filename)

# 打印结果
print("原始四边形:", poly)
print("最大内切四边形:", inscribed_rect)
