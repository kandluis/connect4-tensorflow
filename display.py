from game import Player
from enum import Enum, unique

from typing import List

@unique
class GameMode(Enum):
  EASY = 1
  MEDIUM = 2
  TWO_PLAYER = 3

  def __str__(self) -> str:
    return self.name

class Action(int):
  @staticmethod
  def isValid(value: int) -> bool:
    return 0 <= value and value < 7

  def __new__(cls, value):
    value = int.__new__(cls, int(value))
    # TOOD(nautilik): Share the 7 value for nColumns.
    assert Action.isValid(value)
    return value

def allActions() -> List[Action]:
  return [Action(i) for i in range(7)]

class Display(object):
  def __init__(self, game):
    self.game = game

  def show(self) -> None:
    print(" ".join(["{}".format(i + 1) for i in range(self.game.nColumns)]))
    print("-".join(["-" for i in range(self.game.nColumns)]))
    print(self.game)
    print("-".join(["-" for i in range(self.game.nColumns)]))

  def promptContinuePlay(self) -> bool:
    while True:
      selection = input("Would you like to play again? [y/n]: ").lower()
      if selection not in ["n", "y"]: continue
      return selection == "y"

  def getAction(self, player: Player) -> Action:
    if player.isAI():
      return player.getAction(self.game)
    # Ask the user fo the action.
    while True:
      try:
        col = int(input(" ".join([
          self._playerCallout(player),
          "Select a column on which to drop the token: "]))) - 1
        if (Action.isValid(col) and self.game.isValid(col)):
          return Action(col)
      except ValueError:
        pass
      print(" ".join([self._playerCallout(player), "Invalid action."]))

  def endGameWith(self, winner: Player) -> None:
    self.show()
    print("{} is the winner!".format(winner.token.name))

  def displayWelcomeMessage(self) -> None:
    print("Welcome to Connect4-RL!")

  def getGameMode(self) -> GameMode: 
    while True:
      selection = input("What game mode would you like to play: {}: ".format(" or ".join(map(str, list(GameMode))))).upper()
      candidateModes = [mode for mode in list(GameMode) if mode.name == selection]
      if len(candidateModes) == 1:
        return candidateModes[0]
      print("Invalid mode selected!")


  def _playerCallout(self, player: Player) -> str:
    return "[{}]".format(player.token.name)