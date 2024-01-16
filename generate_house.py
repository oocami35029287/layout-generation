import cv2
import numpy as np    
import largestinteriorrectangle as lir
import shelf_module
import math
import array
import random
import sys
import rectangle_packing_solver as rps
from scipy.spatial import distance
import json

#global image storage path
abs_path = ""
# 設定方形的基本尺寸
base_width = 700
base_height = 800
random_adj = 0.1
door_size = 300

aisle_size = 70
shelf_size = [106, 42]

def walls_generation():
    # 計算方形的四個角的坐標
    top_left = [0, 0]
    top_right = [base_width,0]
    bottom_right = [base_width, base_height]
    bottom_left = [0, base_height]

    # 計算偏移量的範圍
    width_max_offset = int(random_adj* base_width)
    height_max_offset = int(random_adj* base_height)

    # 加上偏移量
    if(width_max_offset>0 and height_max_offset>0):
        top_left[0]     += np.random.randint(0, width_max_offset*2 ) - width_max_offset
        top_left[1]     += np.random.randint(0, height_max_offset*2 ) - height_max_offset

        top_right[0]    += np.random.randint(0, width_max_offset*2 )  - width_max_offset
        top_right[1]    += np.random.randint(0, height_max_offset *2) - height_max_offset

        bottom_right[0] += np.random.randint(0, width_max_offset *2) - width_max_offset
        bottom_right[1] += np.random.randint(0, height_max_offset *2) - height_max_offset

        bottom_left[0]  += np.random.randint(0, width_max_offset *2) - width_max_offset
        bottom_left[1]  += np.random.randint(0, height_max_offset *2) - height_max_offset
        
    #max (offset for output, not affect other generation part)
    max_width = (bottom_right[0] if bottom_right[0]>top_right[0] else top_right[0])- (bottom_left[0] if bottom_left[0]<top_left[0] else top_left[0]) +20
    max_height = (bottom_left[1] if bottom_left[1]>bottom_right[1] else bottom_right[1])- (top_left[1] if top_left[1]<top_right[1] else top_right[1]) +20
    room_size = (max_width,max_height)
    top = (top_left[1] if top_left[1]<top_right[1] else top_right[1]) -10
    left = (bottom_left[0] if bottom_left[0]<top_left[0] else top_left[0]) -10
    off_top_left    = [top_left[0]    -left  ,top_left[1]    -top   ]
    off_top_right   = [top_right[0]   -left  ,top_right[1]   -top  ] 
    off_bottom_right = [bottom_right[0]-left  , bottom_right[1]-top   ]
    off_bottom_left  = [bottom_left[0] -left  , bottom_left[1] -top  ]
    
    return np.array([[off_top_left,off_top_right,off_bottom_right,off_bottom_left]], np.int32), room_size
    # return np.array([[top_left,top_right,bottom_right,bottom_left]], np.int32)


def door_generation(house):
    # 定義方形的線段數組
    house_walls = np.array([
        [house[0][0], house[0][1]],
        [house[0][1], house[0][2]],
        [house[0][2], house[0][3]],
        [house[0][3], house[0][0]],
    ], dtype=np.int32)

    door_wall = np.random.randint(0, len(house_walls))
    line = house_walls[door_wall]  # 修正这一行，使用正确的索引范围

    ret_walls = []  # 添加這一行，初始化 ret_walls 列表

    for i, wall in enumerate(house_walls):
        if i == door_wall:
            ret_walls += [[wall, "door"]]
        else:
            ret_walls += [[wall, "no_door"]]

    width = line[0][0] - line[1][0]
    height = line[0][1] - line[1][1]
    length = (width ** 2 + height ** 2) ** 0.5
    if length > door_size:
        mid = np.random.uniform(door_size/2, length - door_size/2)  # 使用uniform而不是randint
        angle = np.arctan2(height, width)  # 计算线段的角度
        x = line[1][0] + mid * np.cos(angle)  # 计算x坐标
        y = line[1][1] + mid * np.sin(angle)  # 计算y坐标
        point1 = [int(np.round(x - door_size/2 * np.cos(angle))), int(np.round(y - door_size/2 * np.sin(angle)))] # 计算线段起点
        point2 = [int(np.round(x + door_size/2 * np.cos(angle))), int(np.round(y + door_size/2 * np.sin(angle)))] # 计算线段终点
        return (point1, point2), ret_walls
    else:
        print("Error: door size larger than wall.")
        sys.exit()

def generate_shelf_along_wall(walls):
    module = shelf_module.Module1.generate_modules(aisle_size, shelf_size)
    module_size = module.get_size()
    vector_arr = []
    length_arr = []
    walls_no_door = []
    all_modules = []
    bounding_points = []
    for wall in walls:
        if wall[1] == "no_door":
            vector = wall[0][1] - wall[0][0]
            vector_arr.append(vector/np.linalg.norm(vector))
            length_arr.append(np.linalg.norm(vector))
            walls_no_door.append(wall)


    for i, wall in enumerate(walls_no_door):
        num = math.floor((length_arr[i] - 2*module_size[0])/module_size[0])
        if num<0: num = 0
        for j in range(num):
            # print("num " ,num)
            rot = math.atan2(vector_arr[i][1], vector_arr[i][0])
            x = wall[0][0][0]+module_size[0]*math.cos(rot)*(j+1)
            y = wall[0][0][1]+module_size[0]*math.sin(rot)*(j+1)
            #print(wall[0])
            pos = (x.astype(int),y.astype(int))
            #print("pos",pos)
            all_modules.append(shelf_module.ModuleContainer(module, pos, math.degrees(rot)))
            if j ==0:
                x1 = x+ module_size[1]*math.cos(rot+math.radians(90))
                y1 = y+ module_size[1]*math.sin(rot+math.radians(90))
                bounding_points.append((x1.astype(int),y1.astype(int)))
                #print(rot)
            if j ==(num-1):
                x1 = x+ module_size[1]*math.cos(rot+math.radians(90))+module_size[0]*math.cos(rot)
                y1 = y+ module_size[1]*math.sin(rot+math.radians(90))+module_size[0]*math.sin(rot)
                bounding_points.append((x1.astype(int),y1.astype(int)))
    return all_modules, bounding_points

def generate_inside_modules(inscribe):
    space_size = np.array(lir.pt2(inscribe)) - np.array(lir.pt1(inscribe)) 
    inscribe_pos = lir.pt1(inscribe)
    print(space_size)
    module2_array = shelf_module.Module2.generate_modules(aisle_size, shelf_size, space_size)
    
    all_modules = []    # original
    all_modules_list = [] #shuffled
    all_modules_sq = [] #shuffled for sequence pair
    for module2 in module2_array.values():
        # print(module2)
        for i in range(10):
            mod = shelf_module.ModuleContainer(module2, (0,0), 0)
            all_modules.append(mod)      

    all_modules_list = list(all_modules)
    random.shuffle(all_modules_list)
    for mod in all_modules_list:
        all_modules_sq.append(mod.get_sq_problem()) 
        # print(mod)
    problem = rps.Problem(rectangles=all_modules_sq)
    # print("problem:", problem)
    print("\n=== Solving with width/height constraints ===")
    solution = rps.Solver().solve(problem=problem, height_limit=space_size[1], show_progress=True, seed=1111)
    # print("solution:", solution)
    rps.Visualizer().visualize(solution=solution, path=abs_path+"floorplan_example_limit.jpg")

    output_sq = solution.floorplan.positions
    new_array = []
    for i, mod1 in enumerate(output_sq):
        if(mod1['x']+mod1['width']<space_size[0]):
            if mod1['width'] != all_modules_list[i].get_module().get_size()[0]:  #rotated
                all_modules_list[i].set_pos((mod1['x']+inscribe_pos[0]+mod1['width'],mod1['y']+inscribe_pos[1]))
                all_modules_list[i].set_inner_module_rot()
            else:   #not rotated
                all_modules_list[i].set_pos((mod1['x']+inscribe_pos[0],mod1['y']+inscribe_pos[1]))
            new_array.append(all_modules_list[i])
            print(all_modules_list[i])
    return new_array

def transfer_to_floor_map(room_size,shelf_points,door, walls):

    # Create an empty white image
    image_size = (room_size[1],room_size[0], 3)  # Adjust these dimensions based on your data
    image = np.ones(image_size, dtype=np.uint8) * 255

    # Draw each shelf as a filled rectangle

    for shelf in shelf_points:
        x = int(shelf['x'])
        y = int(shelf['y'])
        rotation = shelf['rot']

        # Create a rotation matrix around the top-left corner
        rotation_matrix = cv2.getRotationMatrix2D((0, 0), -rotation, 1)
        # print("shelf rotation",x,y,rotation)
        # Create a rectangle
        rect_points = np.array([[0, 0],
                                [shelf_size[0], 0],
                                [shelf_size[0], shelf_size[1]],
                                [0, shelf_size[1]]])

        # Rotate the rectangle points
        rect_points_rotated = cv2.transform(np.array([rect_points]), rotation_matrix)
        final_point =[]
        for point in rect_points_rotated[0]:
            final_point.append(point+[x,y])
        # print("out",final_point[0])
        # Draw the filled rectangle on the image
        cv2.fillPoly(image, [np.int32(final_point)], color=(0, 0, 0))
    wall_no_door = []
    for wall in walls:
        if wall[1] == "door":
            if distance.euclidean(wall[0][0],door[0])<distance.euclidean(wall[0][0],door[1]):
                wall_no_door.append((wall[0][0].tolist(),door[0]))
                wall_no_door.append((door[1],wall[0][1].tolist()))
            else:
                wall_no_door.append((wall[0][0].tolist(),door[1]))
                wall_no_door.append((door[0],wall[0][1].tolist()))

        else:
            wall_no_door.append(wall[0].tolist())
    for wall in wall_no_door:
        cv2.line(image, tuple(wall[0]), tuple(wall[1]), (0, 0, 0), 15)
    # Save the image as a PNG file
    # Resize the image by a factor of 5
    resized_image = cv2.resize(image, (0, 0), fx=0.2, fy=0.2)
    # Flip the resized image upside down
    resized_image = cv2.flip(resized_image, 0)
    # Convert the resized image to grayscale if it's not already
    cv2.imwrite(abs_path+"shelf_rectangles.jpg", resized_image)    
    if len(resized_image.shape) == 3:
        resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Save the resized image as a PGM file
    cv2.imwrite(abs_path+"resized_shelf_rectangles.pgm", resized_image)
    return wall_no_door

def floor_generation(dataDict,abs_path_var):
    #transfer data
    global abs_path
    abs_path = abs_path_var
    global aisle_size,base_width,base_height
    aisle_size = dataDict["aisleSize"]
    base_width = dataDict["storeWidth"]
    base_height = dataDict["storeHeight"]
    print("innerReceived MapData:")
    print(dataDict)
    #modules generate
    house, room_size = walls_generation() 
    # print("house ", house)
    #door
    door, walls = door_generation(house)
    
    #shelf along wall
    all_module1,bounding_points = generate_shelf_along_wall(walls)

    #內切
    bounding_points_shape = np.array([bounding_points], np.int32)
    
    inscribe = lir.lir(bounding_points_shape)
    
    all_inner_modules = generate_inside_modules(inscribe)

    all_modules = all_module1 + all_inner_modules
    all_shelves =[]
    for mod in all_modules:
        all_shelves = all_shelves + mod.get_shelves()
        # print(mod)
    wall_no_door = transfer_to_floor_map(room_size,all_shelves,door, walls)
    # print("all_shelves", all_shelves)    
    # print("walls",wall_no_door)
    
    # all_shelves,wall_no_door
    all_shelves_str = json.dumps(all_shelves)
    converted_walls = [{"point1": wall[0],"point2": wall[1]} for wall in wall_no_door]
    # print(wall_no_door)
    walls_str = json.dumps(converted_walls)
    # returnstring = "shelf = "+all_shelves_str+"wall = " + walls_str
    # print(returnstring)
        
    #=================================
    # 創建一個空的黑色圖像
    img = np.zeros((room_size[1], room_size[0], 3), dtype=np.uint8)
    # # 使用cv2.line()繪製線段
    cv2.polylines(img, [house], True, (255, 255, 255), 2)

    for mod in all_module1:
        # print(tuple(mod.get_position()))
        cv2.circle(img, mod.get_pos(), radius=2, color=(0, 255, 255), thickness=10)
    for mod in all_inner_modules:
        # print(tuple(mod.get_position()))
        cv2.circle(img, mod.get_pos(), radius=2, color=(255, 255, 0), thickness=10)
    for point in bounding_points:
        #print(tuple(point))
        cv2.circle(img, point, radius=2, color=(55, 155, 255), thickness=10)
        
    cv2.rectangle(img, lir.pt1(inscribe), lir.pt2(inscribe), (0, 255, 0), 2)
    cv2.line(img, tuple(door[0]), tuple(door[1]), (0, 0, 255), 2)
    # 保存圖像為jpg文件
    cv2.imwrite(abs_path+'square_with_offsets.jpg', img)
    #=====================================
    return all_shelves_str, walls_str
        

if __name__ == "__main__":
    dataDict = {"aisleSize": 40,"storeWidth":700,"storeHeight":800}
    floor_generation(dataDict)
