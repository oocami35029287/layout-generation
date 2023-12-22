# store_config = {
#     'base_width': 700,
#     'base_height': 800,
#     'random_adj': 0.1,
#     'door_size': 300,
#     'aisle_size': 70,
#     'shelf_size': [80, 40],
# }
import generate_house
import socket
import pickle

# 建立 socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9487))

# 接收配置字典字串
config_str = client_socket.recv(1024)
config = pickle.loads(config_str)

print("Received configuration:")
print(config)

# 在這裡進行你想做的事情，然後將結果字串發送回 server
result_str = floor_generation()
client_socket.send(result_str.encode())

client_socket.close()