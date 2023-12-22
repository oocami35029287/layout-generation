import numpy as np
import cv2 as cv
import largestinteriorrectangle as lir
def largest_rect_in_non_convex_poly(points):
    # Convert points to NumPy array
    points = np.array(points, dtype=np.float32)

    # Create a matrix big enough to not lose points during rotation
    bbox = cv2.boundingRect(points)
    max_dim = max(bbox[2], bbox[3])
    work = np.zeros((2 * max_dim, 2 * max_dim), dtype=np.uint8)

    # Prepare transformation matrix
    R = cv2.getRotationMatrix2D((max_dim, max_dim), 0, 1)

    # Apply transformation
    cv2.warpAffine(points.reshape(1, -1, 2), R, (2 * max_dim, 2 * max_dim), work)

    # Store best data
    best_rect = (0, 0, 0, 0)
    best_angle = 0

    # For each angle
    for angle in range(0, 90, 1):
        print(angle)

        # Rotate the points
        R = cv2.getRotationMatrix2D((max_dim, max_dim), angle, 1)
        rotated_points = cv2.transform(points.reshape(1, -1, 2), R).reshape(-1, 2)

        # Keep the crop with the polygon
        bbox = cv2.boundingRect(rotated_points)
        crop = work[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]].copy()

        # Invert colors
        crop = ~crop

        # Solve the problem: "Find largest rectangle containing only zeros in an binary matrix"
        r = find_min_rect(crop)

        # If best, save result
        if r[2] * r[3] > best_rect[2] * best_rect[3]:
            best_rect = (r[0] + bbox[0], r[1] + bbox[1], r[2], r[3])
            best_angle = angle

    # Apply the inverse rotation
    R_inv = cv2.getRotationMatrix2D((max_dim, max_dim), -best_angle, 1)
    rotated_rect_points = cv2.transform(np.array([best_rect[:2], [best_rect[0] + best_rect[2], best_rect[1]],
                                                  best_rect[2:], [best_rect[0], best_rect[1] + best_rect[3]]], dtype=np.float32).reshape(1, -1, 2), R_inv).reshape(-1, 2)

    # Get the rotated rect
    rrect = cv2.minAreaRect(rotated_rect_points)

    return rrect
def rotate_polygon(polygon, angle):
    center = (np.mean(polygon[:, 0], axis=0))
    rotation_matrix = cv.getRotationMatrix2D(center, angle, 1)
    rotated_polygon = cv.transform(polygon, rotation_matrix)
    return rotated_polygon

def calculate_polygon_area(polygon):
    return 0.5 * np.abs(np.dot(polygon[:, 0, 0], np.roll(polygon[:, 0, 1], 1)) - np.dot(polygon[:, 0, 1], np.roll(polygon[:, 0, 0], 1)))



polygon = np.array([[[20, 0], [40, 20], [20, 40], [0,20]]], np.int32)
rectangle = lir.lir(polygon)


max_rectangle = None
max_rectangle_area = 0
for angle in range(0, 360, 5):
    rotated_polygon = rotate_polygon(polygon, angle)
    rectangle = lir.lir(rotated_polygon)

    # Get the area of the inscribed rectangle
    rectangle_area = calculate_polygon_area(rectangle)

    if rectangle_area > max_rectangle_area:
        max_rectangle = rectangle
        max_rectangle_area = rectangle_area





img = np.zeros((160, 240, 3), dtype="uint8")

cv.polylines(img, [polygon], True, (0, 0, 255), 1)
cv.rectangle(img, lir.pt1(rectangle), lir.pt2(rectangle), (255, 0, 0), 1)

cv2.imwrite('inscribeout.jpg', img)