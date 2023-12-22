import numpy as np

house = np.array([[[1,2], [1,2], [1,2], [1,2]]], np.int32)
# return np.array([[top_left, top_right, bottom_right, bottom_left]], np.int32)

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

for wall in ret_walls:
    print(wall)
    if wall[1] == "no_door":
        print(wall[0][1] - wall[0][0])
# 打印 ret_walls 以確認結果
# print(ret_walls)
