from game import Player, Game, Token
import display

from typing import List

import random

class RandomAI(Player):
  def __init__(self, token: Token) -> None:
    super(RandomAI, self).__init__(token)

  def isAI(self) -> bool:
    return True

  def getAction(self, game: Game) -> display.Action:
    return random.choice(display.allActions())