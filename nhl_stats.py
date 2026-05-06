import numpy as np
import tensorflow as tf

def predict_gp(name, input, output, current):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units=1, input_shape=[3]),
        tf.keras.layers.Dense(units=3),
        tf.keras.layers.Dense(units=6),
        tf.keras.layers.Dense(units=1)
    ])

class Player:
    def __init__(self, name, input, output, current):
        self.name = name
        # array organized as [games played that season, goals last season, assists last season, points last season, age, oilers team rank last season]
        self.input = input
        # points that season
        self.output = output
        # games played is assumed for current prediction
        self.current = current
mcdavid = Player("Connor McDavid",
                 np.array([[82, 19, 32, 48, 20, 29], [82, 30, 70, 100, 21, 8], [78, 41, 67, 108, 22, 23], [64, 41, 75, 116, 23, 25], [56, 34, 63, 97, 24, 12], [80, 33, 72, 105, 25, 11], [82, 44, 79, 123, 26, 11], [76, 64, 89, 153, 27, 6], [67, 32, 100, 132, 28, 9]]),
                 np.array([100, 108, 116, 97, 105, 123, 153, 132, 100]),
                 np.array([78, 26, 74, 100, 29, 9])
                  )

crosby = Player("Sydney Crosby",
                np.array([]),
                np.array([]),
                np.array([])
                )