import json
import requests
import random
import time
from graph import graph
from api import Queue

token = "8f8f7f8962c63020496c4d1833059b8555b20305"

# def movement(direction, next_room_id=None):
#   url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
#   if next_room_id is not None:
#     time.sleep(current['cooldown'])
#     data = f'{{"direction":"{direction}","next_room_id": "{next_room_id}"}}'
#   else:
#     time.sleep(current['cooldown'])
#     data = f'{{"direction":"{direction}"}}'
#   result = requests.post(url, data=data,
#                          headers={'Content-Type':'application/json',
#                                   'Authorization': f'Token {token}'}).json()

url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
current = requests.get(url, headers={'Authorization': f'Token {token}'}).json()
if current['room_id'] not in graph:
  new_room = {}
  for direction in current['exits']:
      new_room[direction] = "?"
  graph[current['room_id']] = [new_room, current]
print("current",graph[current['room_id']])

# Movement
def movement(direction, next_room_id=None):
  if graph[current['room_id']][1]['terrain'] == 'CAVE':
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
  else:
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/fly/'
  if next_room_id is not None:
    data = f'{{"direction":"{direction}","next_room_id": "{next_room_id}"}}'
    if graph[next_room_id][1]['terrain'] == 'CAVE':
      url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
  else:
    data = f'{{"direction":"{direction}"}}'
  
  result = requests.post(url, data=data,
                         headers={'Content-Type':'application/json',
                                  'Authorization': f'Token {token}'}).json()
  # Update room_id in graph
  inverse_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
  if result['room_id'] not in graph:
    graph[result['room_id']] = {}
    for road in result['exits']:
      graph[result['room_id']][road] = "?"
    new_room = {}
    for road in result['exits']:
      new_room[road] = "?"
    graph[result['room_id']] = [new_room, result]
  graph[current['room_id']][0][direction] = result['room_id']
  graph[result['room_id']][0][inverse_directions[direction]] = current['room_id']
  print(result)
  return result

def bfs(starting_room, destination):
  queue = Queue()
  queue.enqueue([starting_room])
  visited = set()
  while queue.size() > 0:
    path = queue.dequeue()
    room_id = path[-1]
    if room_id not in visited:
      if room_id == destination:
        return path
      else:
        for direction in graph[room_id][0]:
          # if graph[room_id][0][direction] not in traps:
          new_path = path.copy()
          new_path.append(graph[room_id][0][direction])
          queue.enqueue(new_path)
      visited.add(room_id)
  return []
bfs(current['room_id'], 461)

inverse_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
# prev_move = None
while True:
  current_exits = graph[current['room_id']][0]
  print(current_exits)
  # directions = []
  # for direction, room_id in current_exits.items():
  #   # If adjacent room_id not visited yet, add that direction
  #   if room_id == "?":
  #     directions.append(direction)
  # if len(directions) == 0:
    # print('All adjacent rooms visited..')
  targets = bfs(current['room_id'], 202)[1:]
  print("targets*************************************", targets)
  # print("current exits",current_exits.items())
  for direction, room_id in current_exits.items():
    if room_id == targets[0]:
      # Figure out the direction of next room
      # next_move = direction
      print("You've arrived at a Shrine")
      break
  print(f'********************, Room[{current["room_id"]}] to Room[{current_exits[next_move]}]')
  if current_exits[next_move] == "?":
    print(f"Traveling to the unknown.. ({len(graph)}/500)")
    end_room = movement(next_move)
  else:
    # Use "Wise Explorer" buff
    end_room = movement(next_move, current_exits[next_move])
  print(f"CD: {end_room['cooldown']},**********************, {end_room['messages']}")
  # if len(end_room['items']) > 0:
  #   for item in end_room['items']:
  #     if 'treasure' not in item:
  #       print(f'{item} found in {end_room["room_id"]}')
  #       time.sleep(end_room['cooldown'])
  #       end_room = take_item(item)
  # if end_room['title'] == 'Shop':
  #   time.sleep(end_room['cooldown'])
  #   items = status_check()['inventory']
  #   for item in items:
  #     if 'treasure' in item:
  #       time.sleep(end_room['cooldown'])
  #       end_room = sell_item(item)
  # prev_move = next_move
  current = end_room
  time.sleep(current['cooldown'])