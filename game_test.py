import unittest
import game

class PlayerTest(unittest.TestCase):
  def testNumberOfPlayers(self):
    self.assertEqual(2, len(list(game.Player)))

class DirectionTest(unittest.TestCase):
  def testNumberDirections(self):
    self.assertEqual(4, len(list(game.Direction)))

class PositionTest(unittest.TestCase):
  def testPositionCreation(self):
    pos: game.Position = game.Position(1,2)

    self.assertEqual(1, pos.row)
    self.assertEqual(2, pos.column)

    row, col = pos

    self.assertEqual(1, row)
    self.assertEqual(2, col)

class GameTest(unittest.TestCase):
  def setUp(self):
    self.game: game.Game = game.Game(6, 7)
  
  def testNumberOfRows(self):
    self.assertEqual(6, self.game.nRows)
    self.assertEqual(7, self.game.nColumns)

  def testPiecesDrop(self):
    # Add in column one should drop to the bottom
    self.game.addPiece(game.Player.RED, 1)

    self.assertIsNone(self.game.getPlayer(game.Position(5, 1)))
    self.assertIsNone(self.game.getPlayer(game.Position(4, 1)))
    self.assertIsNone(self.game.getPlayer(game.Position(3, 1)))
    self.assertIsNone(self.game.getPlayer(game.Position(2, 1)))
    self.assertIsNone(self.game.getPlayer(game.Position(1, 1)))

    self.assertEqual(game.Player.RED, self.game.getPlayer(game.Position(0, 1)))

  def testAddMultiplePiecesSameColumn(self):
    '''
    0 0 0 0 0 0 0
    0 0 0 0 0 0 0
    0 0 0 0 0 0 0
    0 0 0 x 0 0 0
    0 0 0 x 0 0 0
    0 0 0 x 0 0 0
    '''
    self.game.addPiece(game.Player.RED, 4)
    self.game.addPiece(game.Player.RED, 4)
    self.game.addPiece(game.Player.RED, 4)

    self.assertIsNone(self.game.getPlayer(game.Position(5, 4)))
    self.assertIsNone(self.game.getPlayer(game.Position(4, 4)))
    self.assertIsNone(self.game.getPlayer(game.Position(3, 4)))
    
    self.assertEqual(game.Player.RED, self.game.getPlayer(game.Position(2, 4)))
    self.assertEqual(game.Player.RED, self.game.getPlayer(game.Position(1, 4)))
    self.assertEqual(game.Player.RED, self.game.getPlayer(game.Position(0, 4)))

  def testVerticalWinCondition(self):
    '''
    0 0 0 0 0 0 0
    0 0 0 0 0 0 0
    0 0 0 x 0 0 0
    0 0 0 x 0 0 0
    0 0 0 x 0 0 0
    0 0 0 x 0 0 0
    '''
    self.assertFalse(self.game.addPiece(game.Player.RED, 4))
    self.assertFalse(self.game.addPiece(game.Player.RED, 4))
    self.assertFalse(self.game.addPiece(game.Player.RED, 4))
    # Winning move.
    self.assertTrue(self.game.addPiece(game.Player.RED, 4))

  def testHorizontalWinCondition(self):
    '''
    0 0 0 0 0 0 0
    0 0 0 0 0 0 0
    0 0 0 0 0 0 0
    0 0 0 0 0 0 0
    0 0 0 0 0 0 0
    0 x x x x 0 0
    '''
    self.assertFalse(self.game.addPiece(game.Player.RED, 1))
    self.assertFalse(self.game.addPiece(game.Player.RED, 2))
    self.assertFalse(self.game.addPiece(game.Player.RED, 3))
    # Winning move.
    self.assertTrue(self.game.addPiece(game.Player.RED, 4))

  def testDiagonalUpRightWinCondition(self):
    '''
    0 0 0 0 0 0 0
    0 0 0 0 0 0 0
    0 0 0 0 x 0 0
    0 0 0 x o 0 0
    0 0 x o o 0 0
    0 x o o o 0 0
    '''
    self.assertFalse(self.game.addPiece(game.Player.RED, 1))

    self.assertFalse(self.game.addPiece(game.Player.YELLOW, 2))
    self.assertFalse(self.game.addPiece(game.Player.RED, 2))

    self.assertFalse(self.game.addPiece(game.Player.YELLOW, 3))
    self.assertFalse(self.game.addPiece(game.Player.YELLOW, 3))
    self.assertFalse(self.game.addPiece(game.Player.RED, 3))

    self.assertFalse(self.game.addPiece(game.Player.YELLOW, 4))
    self.assertFalse(self.game.addPiece(game.Player.YELLOW, 4))
    self.assertFalse(self.game.addPiece(game.Player.YELLOW, 4))
    # Winning move.
    self.assertTrue(self.game.addPiece(game.Player.RED, 4))

  def testDiagonalUpLeftWinCondition(self):
    '''
    0 0 0 0 0 0 0
    0 0 0 0 0 0 0
    0 x 0 0 0 0 0
    0 o x 0 0 0 0
    0 o o x 0 0 0
    0 o o o x 0 0
    '''
    self.assertFalse(self.game.addPiece(game.Player.YELLOW, 1))
    self.assertFalse(self.game.addPiece(game.Player.YELLOW, 1))
    self.assertFalse(self.game.addPiece(game.Player.YELLOW, 1))
    self.assertFalse(self.game.addPiece(game.Player.RED, 1))

    self.assertFalse(self.game.addPiece(game.Player.YELLOW, 2))
    self.assertFalse(self.game.addPiece(game.Player.YELLOW, 2))
    self.assertFalse(self.game.addPiece(game.Player.RED, 2))

    self.assertFalse(self.game.addPiece(game.Player.YELLOW, 3))
    self.assertFalse(self.game.addPiece(game.Player.RED, 3))
    # Winning move.
    self.assertTrue(self.game.addPiece(game.Player.RED, 4))

if __name__ == '__main__':
  unittest.main()