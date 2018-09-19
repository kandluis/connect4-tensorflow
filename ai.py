from game import Player, Game, Token
import display
import tensorflow as tf
import numpy as np

from typing import List

import random

class RandomAI(Player):
  def __init__(self, token: Token) -> None:
    super(RandomAI, self).__init__(token)

  def isAI(self) -> bool:
    return True

  def getAction(self, game: Game) -> display.Action:
    return random.choice(display.allActions())

class RLAgent(Player):
  def __init__(self, token: Token) -> None:
    super(RLAgent, self).__init__(token)

    self.model = tf.keras.Sequential([
      # First layer will go from (6,7,2) to (6,7,32).
      # It does this with a convolution of filter size (3,3) over
      tf.keras.layers.Conv2D(
        filters=32, kernel_size=3, padding='same', activation='relu',
        use_bias=True, data_format='channels_last'),
      tf.keras.layers.BatchNormalization(axis=1, fused=False),
      # We now output (4,5,64)
      tf.keras.layers.Conv2D(
        filters=64, kernel_size=3, padding='valid', activation='relu',
        use_bias=True, data_format='channels_last'),
      tf.keras.layers.BatchNormalization(axis=1, fused=False),
      # We keep squeezing to output (2,3,128)
      tf.keras.layers.Conv2D(
        filters=128, kernel_size=3, padding='valid', activation='relu',
        use_bias=True, data_format='channels_last'),
      tf.keras.layers.BatchNormalization(axis=1, fused=False),
      # We flatten the output for the final layer. We now have:
      # (768,)
      tf.keras.layers.Flatten(),
      # We output in space (7,) which we'll interpret as probabilities.
      tf.keras.layers.Dense(units=7, activation='relu'),
      tf.keras.layers.BatchNormalization(fused=False),
      tf.keras.layers.Softmax(),
  ])

  def isAI(self) -> bool:
    return True

  def getAction(self, game: Game) -> display.Action:
    probs = self.model.predict(self._getBatchFromGame(game), steps=1)[0]
    return np.random.choice(display.allActions(), p=probs)

  def _getBatchFromGame(self, game: Game) -> tf.Tensor:
    board = game.asNumpyArray(self)
    x, y, p = board.shape
    board = board.reshape((1, x, y, p))
    return tf.cast(tf.convert_to_tensor(board), tf.float32)
