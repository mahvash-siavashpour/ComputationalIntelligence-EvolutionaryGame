from matplotlib import pyplot as plt
import csv
import  numpy as np
max_list = []
min_list =[]
average_list = []

mode = input("Enter Mode: ")
with open(f'{mode}-max.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        max_list.append(float(row[0]))

with open(f'{mode}-min.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        min_list.append(float(row[0]))

with open(f'{mode}-average.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        average_list.append(float(row[0]))


plt.plot(max_list, 'purple')
plt.plot(average_list, 'red')
plt.plot(min_list, 'blue')
plt.legend(["max", "average", "min"])
plt.show()

