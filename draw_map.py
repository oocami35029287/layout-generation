import cv2
import numpy as np

shelf_points = [
    [{'x': 89.0, 'y': 16.0, 'rot': 4.63242305654131}],
    # ... (the rest of your shelf points)
]

shelf_size = [80, 40]

# Create an empty white image
image_size = (1200, 800, 3)  # Adjust these dimensions based on your data
image = np.ones(image_size, dtype=np.uint8) * 255

# Draw each shelf as a filled rectangle
for shelf_group in shelf_points:
    for shelf in shelf_group:
        x = int(shelf['x'])
        y = int(shelf['y'])
        rotation = shelf['rot']

        # Create a rotation matrix around the top-left corner
        rotation_matrix = cv2.getRotationMatrix2D((x, y), rotation, 1)

        # Create a rectangle
        rect_points = np.array([[0, 0],
                                [shelf_size[0], 0],
                                [shelf_size[0], shelf_size[1]],
                                [0, shelf_size[1]]])

        # Rotate the rectangle points
        rect_points_rotated = cv2.transform(np.array([rect_points]), rotation_matrix)

        # Draw the filled rectangle on the image
        cv2.fillPoly(image, [np.int32(rect_points_rotated)], color=(0, 0, 0))

# Save the image as a PNG file
cv2.imwrite("shelf_rectangles.png", image)
