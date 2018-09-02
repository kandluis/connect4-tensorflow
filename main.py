from game import Game, Player, Token
from ai import RandomAI
from display import Display, Action, GameMode

from typing import List

def main() -> None:
  players: List[Player] = []
  game = Game()
  display = Display(game)

  gameMode: GameMode = display.getGameMode()
  if gameMode == GameMode.TWO_PLAYER:
    players = [Player(Token.RED), Player(Token.YELLOW)]
  elif gameMode == GameMode.SINGLE_PLAYER:
    players = [Player(Token.RED), RandomAI(Token.YELLOW)]
  play = True
  while play:
    for player in players:
      display.show()
      action: Action = display.getAction(player)
      if game.addPiece(player, action):
        display.endGameWith(player)
        play = display.promptContinuePlay()
        game.reset()

if __name__ == '__main__':
	main()