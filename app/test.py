# graph = {
#     '1': ['2', '3', '5'],
#     '2': ['4'],
#     '3': ['6', '7', '9'],
#     '4': ['2'],
#     '5': ['8'],
#     '6': ['3'],
#     '7': ['3'],
#     '8': ['9'],
#     '9': ['3', '8']
# }
#
# visited = {}

# def dfs(node):
#     if node not in visited:
#         visited[node] = True
#         print(node)
#         print(visited)
#         print("=============")
#         for neighbor in graph[node]:
#             dfs(neighbor)
#
#
# start_node = '1'
# dfs(start_node)
# ================================

# def bfs(graph, start):
#     visited = []
#     queue = [start]
#
#     while queue:
#         node = queue.pop(0)
#         if node not in visited:
#             visited.append(node)
#             print(node)
#             for neighbor in graph[node]:
#                 if neighbor not in visited:
#                     queue.append(neighbor)
#
# bfs(graph, '1')


# def dijkstra(graph, start):
#     distances = {node: float('infinity') for node in graph}
#     distances[start] = 0
#
#     unvisited_node = list(graph)
#
#     while unvisited_node:
#         current_node = None
#         for node in unvisited_node:
#             if current_node is None or distances[node] < distances[current_node]:
#                 current_node = node
#
#         unvisited_node.remove(current_node)
#
#         for neighbor, weight in graph[current_node].items():
#             tentative_distance = distances[current_node] + weight
#             if tentative_distance < distances[neighbor]:
#                 distances[neighbor] = tentative_distance
#
#     return distances
#
#
# # Ví dụ sử dụng:
# graph = {
#     'A': {'B': 1, 'C': 4},
#     'B': {'A': 1, 'C': 2, 'D': 5},
#     'C': {'A': 4, 'B': 2, 'D': 1},
#     'D': {'B': 5, 'C': 1}
# }
#
# start_node = 'A'
# shortest_distances = dijkstra(graph, start_node)
#
# for node, distance in shortest_distances.items():
#     print(f'Khoảng cách ngắn nhất từ {start_node} đến {node} là {distance}')


import random

# import string
#
# def generate_transaction_code():
#     characters = string.ascii_letters
#     transaction_code = ''.join(random.choice(characters) for _ in range(4))
#     return transaction_code
#
# code = generate_transaction_code()
# print(code)


# import asyncio
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# scheduler = AsyncIOScheduler()
#
#
# async def a(arg):
#     print("Running job 'a' with arguments:", arg)
#     await asyncio.sleep(1)
#
#
# scheduler.add_job(a, 'date', args=['argument1'])
# scheduler.start()
#
# try:
#     asyncio.get_event_loop().run_forever()
# except (KeyboardInterrupt, SystemExit):
#     pass

# class Student:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#         self.department = None
#         self.address = None
#
#     def display_info(self):
#         infor = dict(name=self.name, age=self.age, department=self.department, address=self.address)
#         print(infor)
#
#     def update_age(self, new_age):
#         self.age = new_age
#
#     def add_department(self, department):
#         self.department = department
#
#
# def run_demo():
#     student = Student("Dat", 20)
#     student.add_department("IT")
#     student.display_info()
#
#
# run_demo()

# a = {
#     "2": {
#         "quantity": 20,
#         "price": 5
#     },
#     "3": {
#         "quantity": 40,
#         "price": 7
#     },
#     "4": {
#         "quantity": 40,
#         "price": 10
#     }
# }

# current_quantity = a["2"]["quantity"]
# a["2"]["quantity"] = current_quantity - 1
# print(a)

# quantity_value = 0
# for k, v in a.items():
#     quantity_value += v["quantity"]
# total_amount = 0
# for k, v in a.items():
#     total_amount_tmp = (v["quantity"] * v["price"])
#     total_amount += total_amount_tmp
# print(total_amount)


def dis(data):
    for key, value in data.items():
        print(f'Key: {key}, Value: {value}')



def find(data):
    tmp = data["result"]
    value_result = data["index_result"]
    for key, value in tmp.items():
        if key <= value_result:
            continue
        if value:
            a = key
            data["index_result"] = a
            break
    return data

data1 = {
    "result": {
        "1":  876,
        "2": None,
        "3": None,
        "4": 234,
        "5": 345,
        "6": 456,
        "7": 789,
        "8": None,
        "9": 234,
        "10": None
    },
    "index_result": "2"
}
dis(find(data1))

