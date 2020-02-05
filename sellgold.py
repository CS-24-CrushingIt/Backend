import json
import requests
import random
import time
from graph import graph
from api import Queue

def movement(direction, next_room_id=None):
  url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
  if next_room_id is not None:
    time.sleep(current['cooldown'])
    data = f'{{"direction":"{direction}","next_room_id": "{next_room_id}"}}'
  else:
    time.sleep(current['cooldown'])
    data = f'{{"direction":"{direction}"}}'
  result = requests.post(url, data=data,
                         headers={'Content-Type':'application/json',
                                  'Authorization': f'Token {token}'}).json()
      # Update room_id in graph
  inverse_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
#   print("graph",graph)
#   time.sleep(25)
# time.sleep(15)
  if result['room_id'] not in graph:
    graph[current['room_id']][0][next_move] = result['room_id']
    graph[result['room_id']] = {}
    for direction in result['exits']:
      graph[result['room_id']][direction] = "?"
    new_room = {}
    for direction in result['exits']:
      new_room[direction] = "?"
    new_room[inverse_directions[next_move]] = current['room_id']
    graph[result['room_id']] = [new_room, result]
  print(result)
  with open("data.json", "w") as write_file:
    json.dump(graph, write_file)
  return result

# bfs(current['room_id'], "?")

inverse_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
# prev_move = None
while True:
    current_exits = graph[current['room_id']][0]
    # if status_check()['encumbrance'] > 0:
    #   # If inventory getting too full, go sell at shop
    target = bfs(current['room_id'], 1)[1]
    print('Heading to shop..')
    for direction, room_id in current_exits.items():
        if room_id == target:
            next_move = direction
            print("At the shop")
            break
    # if status_check()['gold'] >= 1000:
    #   # Change name to get clue for Lambda coin
    #   target = bfs(current['room_id'], 55)[1]
    #   print('Heading to the Wishing well..')
    #   for direction, room_id in current_exits.items():
    #     if room_id == target:
    #       next_move = direction
    #       break