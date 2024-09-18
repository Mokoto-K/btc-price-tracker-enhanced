import csv

with open("BTCUSDT-D.csv", "r") as data:
    reader = data.readlines()
    # reader.pop(0)

    print(reader)
