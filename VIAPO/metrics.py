import json
import random

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

day_quantity = 30
estimation = []


def generate_data(quality_model):
    for characteristic in quality_model["quality_model"]["characteristics"]:
        for sub_characteristic in characteristic["sub_characteristics"]:
            for metric in sub_characteristic["metrics"]:
                metric["values"] = [random.random() for i in range(day_quantity)]


def calculate_integral_estimation(quality_model, day):
    characteristic_estimation = 0
    for characteristic in quality_model["quality_model"]["characteristics"]:
        sub_characteristic_estimation = 0
        for sub_characteristic in characteristic["sub_characteristics"]:
            metric_estimation = 0
            for metric in sub_characteristic["metrics"]:
                metric_estimation += metric["importance-factor"] * metric["values"][day]
            sub_characteristic_estimation += sub_characteristic["importance-factor"] * metric_estimation
        characteristic_estimation += sub_characteristic_estimation * characteristic["importance-factor"]
    return characteristic_estimation


with open("metrics.json", encoding="utf-8") as metrics_f:
    quality_model = json.load(metrics_f)

for day in range(day_quantity):
    estimation.append(calculate_integral_estimation(quality_model, day))

y_pos = np.arange(len(estimation))

plt.bar(y_pos, estimation, align='center')
plt.xticks(y_pos, list(range(day_quantity)))
plt.ylabel('Integral estimation value')
plt.xlabel('Day')
plt.title('Integral estimation plot')
df = pd.DataFrame(estimation)
ewma = df.ewm(span=7).mean()
plt.figure()
plt.plot(list(range(day_quantity)), estimation, label="original")
plt.plot(list(range(day_quantity)), ewma, label="EWMA")
plt.ylabel('Integral estimation value')
plt.xlabel('Day')
plt.title('Integral estimation plot')
plt.legend()
plt.show()
