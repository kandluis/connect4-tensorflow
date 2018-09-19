from enum import Enum, unique
from collections import defaultdict
from typing import Dict, Tuple, Optional
from util import *
import numpy as np

WIN_SEQUENCE_REQUIREMENT = 4

@unique
class Token(Enum):
  RED = 1
  YELLOW = 2

  def describe(self) -> str:
    return "x" if self == Token.RED else "o"

  def __str__(self) -> str:
    return self.describe()

class Player(object):
  '''
  A player can be either play with RED or YELLOW objects.
  '''
  def __init__(self, token: Token) -> None:
    self.token = token

  def describe(self) -> str:
    return self.token.describe()

  def isAI(self) -> bool:
    return False

  def getAction(self, game):
    raise InternalError("A real player cannot generate actions.")

class Direction(Enum):
  VERTICAL = 1
  HORIZONTAL = 2
  LEFTUP_DIAGONAL = 3
  RIGHTUP_DIAGONAL = 4

def _getRowDiff(direction: Direction) -> int:
  if (direction == Direction.VERTICAL or
     direction == Direction.LEFTUP_DIAGONAL or
     direction == Direction.RIGHTUP_DIAGONAL):
    return 1
  if direction == Direction.HORIZONTAL:
    return 0
  raise InternalError("{} is an invalid direction".format(direction.name))

def _getColumnDiff(direction: Direction) -> int:
  if (direction == Direction.HORIZONTAL or
     direction == Direction.LEFTUP_DIAGONAL):
    return 1
  if direction == Direction.RIGHTUP_DIAGONAL:
    return -1
  if direction == Direction.VERTICAL:
    return 0
  raise InternalError("{} is an invalid direction".format(direction.name))

class Position(tuple):
  def __new__(cls, row: int, column: int):
    return super(Position, cls).__new__(cls, tuple([row, column]))

  def __init__(self, row: int, column: int) -> None:
    assert 0 <= row and 0 <= column
    super(Position, self).__init__()
    self.row: int = row
    self.column: int = column

class Game(object):
  '''
  A game object tracks the state of the board and allows players to execute particular actions.
  '''
  def __init__(self, nRows: int = 6, nColumns: int = 7) -> None:
    # Rows are indexed from the bottom left corner to the top right corder.
    self.nRows: int = nRows
    self.nColumns: int = nColumns
    self._player_at: Dict[Position, Optional[Player]] = defaultdict(lambda: None)

    # A list from columns to available row.
    self._available_row_index_for_column: Dict[int, int] = defaultdict(int)

  def addPiece(self, player: Player, column: int) -> bool:
    '''
    Adds a piece to the board on the indicated column as if played by the player.

    returns whether or not the piece was a winning move.
    '''
    row: int = self._available_row_index_for_column[column]
    assert row < self.nRows 
    assert column < self.nColumns
    pos = Position(row, column)

    self._player_at[pos] = player
    
    self._available_row_index_for_column[column] += 1

    return self._checkIfWin(pos)

  def isValid(self, action: int) -> bool:
    return self._available_row_index_for_column[action] < self.nRows

  def getPlayer(self, at: Position) -> Optional[Player]:
    '''
    Returns the player at the specified position if one exists.
    '''
    return self._player_at[at]

  def reset(self) -> None:
    self._player_at: Dict[Position, Optional[Player]] = defaultdict(lambda: None)
    self._available_row_index_for_column: Dict[int, int] = defaultdict(int)

  def asNumpyArray(self, forPlayer: Player) -> np.array:
    '''
    Returns the player's numpy representation. A 6x7x2 array.
    '''
    res = np.zeros((self.nRows, self.nColumns, 2))
    for row in range(self.nRows):
      for col in range(self.nColumns):
        player: Optional[Player] = self._player_at[Position(row, col)]
        if player is None:
          res[self.nRows - 1 - row][col] = np.zeros(2)
        else:
          res[self.nRows - 1 - row][col][0] = int(forPlayer.token == player.token)
          res[self.nRows - 1 - row][col][1] = 1 - res[self.nRows - 1 - row][col][0] 
    return res


  def _isValidBoardPosition(self, row: int, col: int) -> bool:
    return (0 <= row and row < self.nRows and
            0 <= col and col < self.nColumns)

  def _getLengthContiguous(self, at: Position, player: Player, along: Direction) -> int:
    '''
    Returns the length of the longest contiguous section belong to player along the specified
    along.
    '''
    row, column = at
    rowDiff: int = _getRowDiff(along)
    colDiff: int = _getColumnDiff(along)
    # Find max
    maxIndex: int = 0
    for i in range(1, WIN_SEQUENCE_REQUIREMENT):
      rowP = row + rowDiff * i
      colP = column + colDiff * i
      if (not self._isValidBoardPosition(rowP, colP) or self._player_at[Position(rowP, colP)] != player):
        break
      maxIndex += 1
    # Find min in reverse direction.
    minIndex: int = 0
    for i in range(1, WIN_SEQUENCE_REQUIREMENT):
      rowP = row - rowDiff * i
      colP = column - colDiff * i
      if (not self._isValidBoardPosition(rowP, colP) or self._player_at[Position(rowP, colP)] != player):
        break
      minIndex += 1

    return maxIndex + minIndex + 1

  def _checkIfWin(self, at: Position) -> bool:
    row, col = at
    player: Optional[Player] = self._player_at[at]
    if player is None:
      return False

    # Check along all directions.
    maxContiguous: int = max([self._getLengthContiguous(at, player, d) for d in list(Direction)])
    return maxContiguous >= WIN_SEQUENCE_REQUIREMENT

  def __str__(self) -> str:
    res = ""
    for row in reversed(range(self.nRows)):
      for col in range(self.nColumns):
        player: Optional[Player] = self._player_at[Position(row, col)]
        if player is None:
          res += " "
        else:
          res += player.describe()
        res += " "
      if row != 0:
        res += "\n"
    return res