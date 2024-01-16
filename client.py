# store_config = {
#     'base_width': 700,
#     'base_height': 800,
#     'random_adj': 0.1,
#     'door_size': 300,
#     'aisle_size': 70,
#     'shelf_size': [80, 40],
# }
from generate_house import floor_generation
import socket
import pickle
import json

# 建立 socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Receive the serialized MapData as a JSON string
mapflg = False
pathflg = False
while(not mapflg or not pathflg):
    received_data = client_socket.recv(1024).decode()
    print(received_data)
    if received_data.startswith("/"):
        abs_path = received_data
        pathflg = True
    else:
        map_data_json = received_data
        mapflg = True

# Deserialize the JSON string into a Python dictionary
map_data_dict = json.loads(map_data_json)

# Print the received MapData
print("Received MapData:")
print(map_data_dict)

# 在這裡進行你想做的事情，然後將結果字串發送回 server
all_shelves_str, walls_str = floor_generation(map_data_dict,abs_path)
# error_count = 0
# while(error_count<3):
#     try:
#         all_shelves_str, walls_str = floor_generation(map_data_dict,abs_path)
#         break
#     except Exception as e:
#         error_count+=1
#         print("cannot found resolution.")
# if(error_count==3):
#     print("cannot found resolution more then 3 times.")    
#     message = "cannot found resolution more then 3 times."
#     client_socket.send(message.encode('utf-8'))
#     client_socket.close()
#     exit(1)

# Combine data into a dictionary
# print(all_shelves_str)
data_dict = f'{{"shelf": {all_shelves_str}, "wall": {walls_str}}}'
print("datadict",data_dict)
# Convert the dictionary to a JSON string
json_data = json.dumps(data_dict)

client_socket.send(data_dict.encode())
print("sent")
client_socket.close()
