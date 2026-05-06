import tensorflow as tf
import numpy as np
from nhl_stats import mcdavid

class TextColor:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

def predict_points(name, input, output, current):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units=1, input_shape=[6]),
        tf.keras.layers.Dense(units=3),
        tf.keras.layers.Dense(units=6),
        tf.keras.layers.Dense(units=6),
        tf.keras.layers.Dense(units=1)
    ])

    model.compile(loss="mean_squared_error", optimizer=tf.keras.optimizers.Adam(0.1))
    model.fit(input, output, epochs=600, verbose=False)

    input_data = np.expand_dims(current, axis=0)
    print("Next season, " + name + " will get " + TextColor.YELLOW + str(model.predict(input_data)) + TextColor.RESET + ' points')

# example
predict_points(mcdavid.name, mcdavid.input, mcdavid.output, mcdavid.current)