# import cv2
# import numpy as np

# # 读取图像
# image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# # 使用Canny边缘检测
# edges = cv2.Canny(image, 50, 150)  # 调整阈值以适应您的图像

# # 使用Otsu二值化
# _, otsu_threshold = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# # 保存处理后的图像
# cv2.imwrite('canny_edges.jpg', edges)
# cv2.imwrite('otsu_threshold.jpg', otsu_threshold)


import cv2
import numpy as np

def edge_detection(image_path, output_path, low_threshold, high_threshold):
    # 讀取影像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 使用Canny邊緣檢測
    edges = cv2.Canny(image, low_threshold, high_threshold)
    
    # 使用Otsu二值化
    _, otsu_threshold = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 保存Canny結果
    cv2.imwrite("canny_result.jpg", otsu_threshold)

    return edges

def hough_transform(edges, original_image, output_path, rho, theta, threshold, min_line_length, max_line_gap):
    # 執行Hough直線變換
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), minLineLength=min_line_length, maxLineGap=max_line_gap)

    # 創建一個與原始影像相同大小的黑色背景
    line_image = np.zeros_like(original_image)

    # 迭代所有偵測到的直線
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 將直線繪製到黑色背景上

    cv2.imwrite("hough_line.jpg",line_image)
    # 合併原始影像與偵測到的直線
    result = cv2.addWeighted(original_image, 0.8, line_image, 1, 0)

    # 保存結果
    cv2.imwrite(output_path, result)

if __name__ == "__main__":
    # 輸入影像路徑
    input_image_path = "image.jpg"

    # 設定輸出影像路徑
    output_image_path = "output_line_image.jpg"

    # 設定Canny邊緣檢測的閾值
    low_threshold = 50
    high_threshold = 150

    # 設定Hough直線變換的參數
    rho = 1
    theta = np.pi / 180
    threshold = 50
    min_line_length = 100
    max_line_gap = 10

    # 進行邊緣檢測
    edges = edge_detection(input_image_path, "canny_result.jpg", low_threshold, high_threshold)

    # 讀取原始影像
    original_image = cv2.imread(input_image_path)

    # 進行Hough直線變換
    hough_transform(edges, original_image, output_image_path, rho, theta, threshold, min_line_length, max_line_gap)

    print("Hough直線變換完成，結果保存在", output_image_path)
