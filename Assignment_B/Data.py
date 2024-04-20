# The goal of this file is to input the main data of the problem
# Those variables will be imported by the others files 
# Most of the values are stored in dataframes

########################
""" Relevant modules """
########################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy
import random

###################################
""" Variables used in this file """
###################################

# Informations on wind power forecasts are in the list 'DA_forecast'
# Informations on day ahead prices are in the list 'DA_price'
# Informations on balancing stage of system are in the dataframe 'PS_need'
    
  
#20 hourly DA sets of wind, taken by the Belgian TSO, and normalized for a 200MW farm (01/03/2024 - 20/03/2024)
DA_forecast = [
    [83.9194, 75.2209, 63.626, 55.3113, 54.079, 59.4174, 72.0527, 88.5993, 103.6926, 120.4443, 132.8181, 140.0877, 145.7675, 148.7702, 146.3272, 137.4594, 120.1837, 101.4218, 88.7997, 85.9974, 90.9219, 97.7776, 103.1724, 103.7048],
    [102.9005, 102.1856, 101.973, 103.6804, 105.0284, 104.6276, 104.3586, 105.8627, 107.3058, 107.8626, 114.6779, 119.9015, 118.26, 108.5729, 95.0016, 81.705, 68.3821, 59.5227, 55.6631, 53.0659, 48.449, 43.5706, 36.6942, 29.7849],
    [37.4261, 33.7997, 29.0465, 25.0532, 21.7411, 18.4553, 15.8195, 13.4113, 10.8489, 7.9102, 7.2668, 8.3062, 10.1707, 11.7539, 13.8187, 16.6068, 18.4111, 19.2031, 19.5361, 18.5033, 17.0744, 15.9916, 14.9541, 14.7904],
    [16.621, 15.1196, 13.2401, 11.7134, 9.0165, 6.7325, 5.2829, 4.5745, 4.0826, 3.521, 3.1673, 3.5972, 3.3883, 2.855, 2.2417, 1.9303, 2.4176, 3.949, 7.3242, 12.878, 18.507, 22.7279, 23.7532, 23.3421],
    [25.2367, 25.6948, 24.7635, 23.1869, 22.028, 21.5501, 21.0074, 19.4872, 17.8523, 15.907, 14.2645, 13.1771, 12.3051, 11.419, 10.2798, 8.7117, 7.2875, 5.8727, 4.4645, 3.6348, 3.1776, 2.9406, 2.569, 2.0629],
    [6.8933, 7.4483, 8.2931, 8.7098, 8.3514, 7.9789, 7.9017, 8.2159, 8.1849, 7.6449, 6.8275, 6.4296, 6.82, 7.7795, 8.817, 9.5066, 9.5301, 8.8349, 8.2714, 8.8029, 10.0644, 11.6965, 13.1084, 14.653],
    [18.5578, 20.9189, 23.9884, 26.3457, 27.6025, 27.2695, 27.6956, 29.1923, 31.2834, 29.8902, 28.0343, 28.6006, 31.2618, 35.3321, 39.6583, 44.928, 49.8309, 53.6679, 59.329, 65.2769, 73.554, 80.1124, 82.6796, 83.5168],
    [87.3811, 89.0631, 88.9963, 87.5429, 86.5035, 89.1515, 94.3422, 99.213, 102.8196, 98.0513, 90.0846, 86.0406, 82.594, 80.6722, 82.3409, 89.0659, 95.1728, 99.6392, 106.3585, 112.409, 112.0054, 106.6529, 99.3607, 93.4692],
    [82.2036, 77.8755, 75.5191, 73.189, 71.7733, 70.2607, 68.4179, 66.56, 63.6006, 55.4091, 47.8357, 45.7144, 46.1613, 49.1385, 54.5954, 60.2781, 65.7416, 76.5059, 87.5006, 91.5869, 88.5447, 82.7473, 73.5756, 64.0126],
    [57.6, 54.3537, 54.1486, 53.3979, 48.6437, 42.5011, 35.6435, 25.9121, 19.2972, 16.8684, 13.527, 11.2986, 8.0598, 5.4597, 5.6196, 6.5095, 4.8916, 3.9208, 4.6329, 5.725, 6.5189, 7.2254, 7.7701, 8.3326],
    [12.068, 12.6212, 13.7829, 16.2428, 19.9736, 24.0665, 27.9694, 30.829, 31.8375, 32.9334, 34.7696, 35.4807, 35.9247, 35.8485, 36.5823, 37.7779, 40.3318, 43.8923, 47.3889, 50.8891, 53.3829, 53.4111, 52.0415, 51.8938],
    [36.2549, 36.1872, 37.9218, 39.4363, 40.583, 40.1371, 36.2954, 29.3089, 22.8718, 20.9641, 22.1907, 25.0203, 30.8065, 36.5795, 41.1662, 44.5348, 46.1895, 44.9854, 42.3411, 40.7984, 42.1126, 46.3353, 50.4094, 53.7215],
    [89.5249, 89.7413, 89.2719, 86.8242, 81.2845, 75.3112, 73.9472, 74.8352, 77.423, 83.1208, 89.9859, 94.9743, 98.881, 100.8273, 100.8997, 100.0352, 96.4032, 91.1307, 87.6755, 85.718, 80.9083, 74.3216, 70.208, 70.3406],
    [83.8065, 85.5487, 84.5882, 79.8227, 73.7459, 70.0537, 69.1911, 70.1487, 73.475, 69.9719, 64.3231, 63.5667, 60.8096, 57.2011, 54.6143, 54.3057, 55.7393, 60.7776, 69.6342, 80.1162, 89.3095, 96.0966, 101.7585, 105.8364],
    [111.8737, 113.6949, 114.9375, 115.961, 115.0608, 113.0524, 112.5708, 112.9207, 115.4502, 121.1903, 126.919, 129.6329, 129.8888, 130.2537, 130.6601, 128.6, 124.366, 119.2788, 114.994, 113.1483, 112.7006, 111.488, 109.1683, 105.1666],
    [86.6935, 77.3431, 68.7217, 60.6017, 52.1976, 45.3542, 39.3535, 31.115, 22.7448, 16.7752, 12.5892, 9.3843, 7.3778, 5.8981, 4.9217, 4.0863, 3.2924, 2.0958, 1.2568, 1.5446, 3.0403, 6.4202, 11.8423, 21.2247],
    [28.2854, 32.7819, 36.7582, 39.8417, 41.2913, 42.7456, 44.7794, 45.1529, 46.054, 46.9599, 47.9335, 51.146, 54.7281, 57.0224, 58.7947, 62.0334, 64.9684, 65.4199, 66.2035, 67.3267, 66.9382, 65.0747, 61.1106, 57.6019],
    [51.1967, 42.0326, 32.5101, 26.2724, 22.202, 19.126, 17.2644, 15.9333, 15.5166, 15.0312, 14.6117, 14.6126, 14.8957, 15.7903, 16.9201, 18.7384, 22.5887, 28.2995, 33.4141, 35.8881, 32.8327, 27.7859, 24.7682, 24.6412],
    [30.0248, 30.1113, 30.5055, 33.0246, 36.3001, 38.9885, 41.4371, 42.2508, 41.7335, 38.6744, 36.9284, 39.0986, 43.4436, 46.642, 46.9035, 44.8829, 40.9668, 36.2653, 32.4677, 29.1161, 24.9535, 20.4843, 16.7263, 13.8149]
    ]

#20 hourly DA prices of Belgian DA market clearing, taken by Nord Pool 
DA_price = [
    [62.04 , 61.42 , 58.14 , 57.83 , 58.3 , 62.49 , 71.58 , 79.36 , 87.8 , 79.83 , 66.53 , 64.76 , 63.16 , 68.2 , 66.89 , 67.2 , 72.49 , 89.4 , 91.88 , 87.19 , 77.49 , 71.62 , 70.06 , 66.39],
    [59.95 , 56.03 , 56.02 , 55.48 , 54.88 , 55.99 , 56.58 , 60.67 , 63.76 , 65.75 , 60.44 , 61.1 , 57.85 , 54.9 , 59.86 , 66.08 , 73 , 81.61 , 93.6 , 89.9 , 76.98 , 72.8 , 84.9 , 79.4],
    [63.7 , 68.8 , 66.74 , 57.91 , 55.48 , 58.88 , 65.05 , 68.97 , 69.9 , 70.36 , 71.24 , 70.51 , 54.02 , 42.51 , 46.84 , 55.58 , 60.28 , 80 , 92.01 , 86.96 , 81.8 , 75 , 72.18 , 72.42],
    [69.13 , 67.9 , 67.41 , 66.22 , 65.59 , 70.83 , 81.18 , 96.67 , 102.97 , 85.02 , 72.16 , 65.07 , 63.93 , 61.14 , 62.5 , 69.86 , 79.18 , 99.4 , 105.18 , 99.13 , 80.52 , 71.39 , 67.49 , 63.93],
    [61.96 , 61.67 , 61.33 , 59.86 , 60.56 , 61.67 , 71.53 , 79.28 , 83.02 , 77 , 71.15 , 69.72 , 66.06 , 65.91 , 69.71 , 70.85 , 76.33 , 82.41 , 104.49 , 126.68 , 105.2 , 90.68 , 86.1 , 72.98],
    [71 , 70.7 , 70.46 , 69.74 , 70.46 , 73.91 , 83.98 , 106.64 , 108.7 , 87.21 , 76.1 , 72.17 , 69.35 , 69.29 , 70.64 , 72.3 , 77.01 , 87.09 , 117.8 , 119.26 , 93.44 , 80.15 , 77.98 , 74.34],
    [73.33 , 72.32 , 70.34 , 68.71 , 69.89 , 73.13 , 84.27 , 103.2 , 96.7 , 79.09 , 71.31 , 66.16 , 61.58 , 59.99 , 63.25 , 65.3 , 69.4 , 87.6 , 104.1 , 90.59 , 83.29 , 73.37 , 73.38 , 67.79],
    [68.49 , 66.96 , 67.01 , 65.99 , 65 , 67.1 , 78.79 , 94.81 , 88.89 , 74.36 , 59.66 , 52.25 , 42.94 , 25 , 44.06 , 48.91 , 56.46 , 72.8 , 84.51 , 80.81 , 71.95 , 65.29 , 65.17 , 60.04],
    [56.71 , 55.05 , 53.87 , 52.69 , 48.76 , 47.96 , 50.66 , 53.06 , 53.06 , 48.12 , 38.69 , 26.44 , 15.85 , 15.67 , 28.16 , 28.57 , 52.65 , 69.66 , 78.17 , 79.03 , 70 , 60.47 , 67.64 , 68.3],
    [48.65 , 46.06 , 40.98 , 35.55 , 32.39 , 32.28 , 33.91 , 39.49 , 55.58 , 69.69 , 60.1 , 80.97 , 90.9 , 80.8 , 65.17 , 65.85 , 70.2 , 84.92 , 87.3 , 106.4 , 95.6 , 87.3 , 86.83 , 82.27],
    [64.8 , 63 , 56.61 , 54.81 , 53.51 , 57 , 76.69 , 82.76 , 85.71 , 82.57 , 76.61 , 68.52 , 68.8 , 66.96 , 67 , 73.43 , 75.76 , 85.58 , 98.71 , 107.98 , 87.99 , 76.68 , 75.02 , 67.08],
    [69.18 , 65.56 , 66.51 , 65.2 , 64.23 , 69.39 , 78.88 , 92.36 , 100.3 , 93.8 , 84.07 , 74.93 , 73.89 , 71.31 , 71.84 , 77.38 , 80 , 76.24 , 87 , 105.01 , 87.93 , 77.16 , 74.94 , 64.91],
    [58.14 , 54.54 , 52.79 , 51.29 , 51.25 , 56.66 , 69.64 , 89.29 , 89.31 , 75 , 64.99 , 59.21 , 55.14 , 48.55 , 50 , 53.94 , 58.14 , 77.4 , 91.97 , 100.2 , 85.18 , 66.87 , 68.18 , 63.88],
    [63.29 , 56.9 , 57.52 , 57 , 51.1 , 57.92 , 70 , 87.05 , 81.99 , 65.71 , 54.32 , 42.23 , 19.8 , 29.61 , 42.82 , 47.24 , 51.03 , 71.14 , 85.43 , 87.45 , 74.11 , 62.83 , 59.61 , 50],
    [46.87 , 42.21 , 41.22 , 37.63 , 31.23 , 36.45 , 48.25 , 58.4 , 64.73 , 53.8 , 44.54 , 37.92 , 33.48 , 30.36 , 26.74 , 25.51 , 40.42 , 53.79 , 64.11 , 88 , 64.29 , 55.5 , 56.38 , 49.45],
    [44.31 , 42.15 , 40.69 , 38.93 , 38.76 , 40.55 , 47.68 , 54.13 , 53.11 , 47.01 , 44.88 , 41.66 , 36.87 , 21.56 , 13.74 , 32.47 , 50.27 , 74.04 , 85.35 , 94.48 , 84.12 , 73.5 , 72.84 , 67.1],
    [64.99 , 60 , 55.14 , 50.51 , 47.59 , 52.07 , 47.92 , 51.43 , 44.85 , 47.06 , 45.28 , 45.87 , 41.76 , 40 , 47.79 , 55.78 , 47.59 , 71.12 , 69.67 , 82.69 , 77.89 , 72.33 , 72.1 , 65.91],
    [64.12 , 57.14 , 58.31 , 52.83 , 51.63 , 52.36 , 69.93 , 96.5 , 94.45 , 82.8 , 72.83 , 66.64 , 64.45 , 56.54 , 47.15 , 49.28 , 54.75 , 67.32 , 109 , 125.6 , 102.86 , 79.4 , 77.62 , 71.64],
    [70 , 66.92 , 63.28 , 60.81 , 58.43 , 62.41 , 79.87 , 104.89 , 95.87 , 72.06 , 59.66 , 53.44 , 50.11 , 44.81 , 45.13 , 49.26 , 54.37 , 77.23 , 98.6 , 128.96 , 110 , 89.06 , 81.73 , 76.1],
    [76.01 , 70.44 , 65.76 , 58.81 , 60 , 66.77 , 93.3 , 103.15 , 98.92 , 70.84 , 61.75 , 57.18 , 62.48 , 65.49 , 59.09 , 64.08 , 71.27 , 97.86 , 144.85 , 141.56 , 115.15 , 99.38 , 82.9 , 78.92]
    ]

#24 random binary variables which will be used to represent the status of power system (excess or deficit)
PS_need = np.random.binomial(n=1, p=0.5, size=24)

#Arbitrarily selecting the in sample scenarios and creating a dataframe with them 
no_sample = 250
no_lists = []

for t in range(no_sample):
    no_lists.append([random.choice(DA_forecast), random.choice(DA_price), random.choice(PS_need)])

in_sample = pd.DataFrame (no_lists, columns=['DA_forecast','DA_price','Binary_var'])







