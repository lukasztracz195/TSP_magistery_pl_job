import pandas as pd
import numpy as np

dictionary = {
    "full_cost": 1000,
    "N": 3,
    "way": [[0, 1, 2, 0]],
    "name": "name"
}

df = pd.DataFrame(dictionary)
print(df)
