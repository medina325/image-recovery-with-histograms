import numpy as np
from enum import Enum

class DistanceHeuristic(Enum):
  """Collection of Heuristics"""

  ED = 'Euclidian Distance'
  SC = 'Square Chi'
  
  def euclidian_distance(pe, pi) -> dict:
    """Returns the Euclidian Distance for every given channel"""

    return {
      'gray':  np.sum(np.square(pe['gray']  - pi['gray'])),
      'red':   np.sum(np.square(pe['red']   - pi['red'])),
      'green': np.sum(np.square(pe['green'] - pi['green'])),
      'blue':  np.sum(np.square(pe['blue']  - pi['blue']))
    }

  def square_chi(pe, pi) -> dict:
    """Returns the Square Chi Distance for every given channel"""

    fix = 0.00000001

    return {
      'gray':  np.sum(np.square(pe['gray'] - pi['gray']) / (pe['gray'] + pi['gray'] + fix)),
      'red':   np.sum(np.square(pe['red'] - pi['red']) / (pe['red'] + pi['red'] + fix)),
      'green': np.sum(np.square(pe['green'] - pi['green']) / (pe['green'] + pi['green'] + fix)),
      'blue':  np.sum(np.square(pe['blue'] - pi['blue']) / (pe['blue'] + pi['blue'] + fix))
    }

class ChannelHeuristic(Enum):
  """Collection of Channel Heuristics
  Each channel heuristic is a different combination of the channels"""
  
  GRAY = 0
  RGBAVG = 6

def selector(channel_heuristic: int, distances: dict) -> float:
  if channel_heuristic == ChannelHeuristic.GRAY:
    return distances['gray']
  elif channel_heuristic == ChannelHeuristic.RGBAVG:
    return (distances['red'] + distances['green'] + distances['blue']) / 3
