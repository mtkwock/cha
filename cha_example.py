'''Just a quick script to start some examples for the converter.
Should be translated to example.cha
'''

from math import pi
import time
import numpy as np

class Directions:
  NORTH = 'north'
  SOUTH = 'south'
  EAST = 'east'
  WEST = 'west'

class Person:
  def __init__(self):
    self.speed = 2
    self.x = 0
    self.y = 0
    self.past_positions = []
    self.map = {}
  
  def walk(self, distance, direction=Directions.NORTH):
    """Changes x, y depending on distance and direction, defaults to north."""
    self.past_positions.append([self.x, self.y, time.time()])
    self.map[(self.x, self.y)] = 1
    if direction == Directions.NORTH:
      self.y += distance
    elif direction == Directions.SOUTH:
      self.y -= distance
    elif direction == Directions.EAST:
      self.x += distance
    elif direction == Directions.WEST:
      self.x -= distance
    else:
      assert False, 'Invalid direction %s' % direction

  def AddPastPositions(self, pp):
    """pp is a string of format '[3,7],[2,9],...'"""
    almost_xys = [xyt.split(',') for xyt in pp.split('],[')]
    for x, y, t in almost_xys:
      self.past_positions.append(
          [int(x.replace('[', '')), int(y), float(t.replace(']', ''))])

  def LoadPastPositions(self, filename):
    """Loads past positions from file"""
    self.past_positions = []
    with open(filename) as f:
      for l in f.readlines():
        try:
          self.AddPastPositions(l.replace('\n', ''))
        except:
          raise Exception('AddPastPositions failed with %s' % direction)
        finally:
          self.past_positions = []

  def CalculateDistanceTraveled(self):
    """Returns a float defining total distance traveled."""
    if not self.past_positions:
      return 0
    total_distance = 0
    x0, y0, _ = self.past_positions[0]
    for x, y, _ in self.past_positions[1:]:
      distance = ((y - y0) ** 2 + (x - x0) * (x - x0)) ** 0.5
      total_distance += distance
      x0, y0 = x, y
    return total_distance

  def CalculateAverageSpeed(self):
    distance = self.CalculateDistanceTraveled()
    time = self.past_positions[-1][2] - self.past_positions[0][2]
    return distance / time


if __name__ == '__main__':
  daming = Person()

  try:
    daming.walk(0, 'not a direction')
    raise Exception('Should fail')
  except:
    pass

  movements = [
      [5, Directions.NORTH],
      [10, Directions.EAST],
      [15, Directions.SOUTH],
      [20, Directions.WEST],
      [25, Directions.NORTH],
      [15, Directions.WEST],
      [10, Directions.EAST],
      [10, Directions.EAST],
      [10, Directions.EAST],
  ]

  for distance, direction in movements:
    total = daming.CalculateDistanceTraveled()
    if total >= 50:
      print('daming is too tired to walk any more! Walked %f' % total)
      break

    if distance >= 20:
      print('daming refuses to walk %i' % distance)
      continue
    daming.walk(distance, direction)
