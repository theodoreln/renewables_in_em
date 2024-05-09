########################
""" Relevant modules """
########################


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy
import random
import gurobipy as gp
import os
GRB = gp.GRB
from Data import in_sample


##################################################
""" Offering strategy under a one-price scheme """
##################################################

def Offering_one_price(in_sample) :
    #Number of units to take into account (based on data)
    # Number of scenarios
    n_scen = len(in_sample)
    # Number of hour
    n_hour = 24
    
    #Optimization part
    # Create the model
    model = gp.Model()
    #Initialize the decision variables
    # Quantity offered by the wind farm in hour t
    var_qu_off = model.addVars(n_hour, lb=-gp.GRB.INFINITY, ub=gp.GRB.INFINITY, vtype=GRB.CONTINUOUS, name='quantity_offered')
    # Difference between the forecast value and the offered value in hour t for scenario w
    var_qu_diff = model.addVars(n_hour, n_scen, lb=-gp.GRB.INFINITY, ub=gp.GRB.INFINITY, vtype=GRB.CONTINUOUS, name='quantity_difference')
    
    # Add the objective function to the model, sum on every t, separation of the conventional generation units and the wind farms
    model.setObjective(gp.quicksum(gp.quicksum((1/n_scen)*(in_sample['DA_price'][w][t]*var_qu_off[t] + in_sample['Binary_var'][w][t]*0.9*in_sample['DA_price'][w][t]*var_qu_diff[t,w]
                                                           + (1-in_sample['Binary_var'][w][t])*1.2*in_sample['DA_price'][w][t]*var_qu_diff[t,w]) for w in range(n_scen)) for t in range(n_hour)), GRB.MAXIMIZE)
    
    #Add constraints to the model
    for t in range(n_hour):
        # Quantity offered limited to the maximum power of the wind turbine
        model.addConstr(var_qu_off[t] <= 200)
        model.addConstr(var_qu_off[t] >= 0)
        # Definition of the difference quantity variable
        for w in range(n_scen):
            model.addConstr(var_qu_diff[t,w] == in_sample['DA_forecast'][w][t] - var_qu_off[t])
    
    #Solve the problem
    model.optimize()
    
    #Get the optimal values
    if model.status == GRB.OPTIMAL:
        
        # Create a list to store the optimal values of the variables
        optimal_qu_off = [round(var_qu_off[t].X,2) for t in range(n_hour)]
        # Value of the optimal objective
        optimal_obj = model.ObjVal
    
    else:
        print("Optimization did not converge to an optimal solution.")
    
    return(optimal_qu_off, optimal_obj)

optimal_qu_off_one, optimal_obj_one = Offering_one_price(in_sample)

##################################################
""" Offering strategy under a two-price scheme """
##################################################

def Offering_two_price(in_sample, coeff_up, coeff_down) :
    #Number of units to take into account (based on data)
    # Number of scenarios
    n_scen = len(in_sample)
    # Number of hour
    n_hour = 24
    
    #Optimization part
    # Create the model
    model = gp.Model()
    #Initialize the decision variables
    # Quantity offered by the wind farm in hour t
    var_qu_off = model.addVars(n_hour, lb=-gp.GRB.INFINITY, ub=gp.GRB.INFINITY, vtype=GRB.CONTINUOUS, name='quantity_offered')
    # Difference between the forecast value and the offered value in hour t for scenario w
    var_qu_diff = model.addVars(n_hour, n_scen, lb=-gp.GRB.INFINITY, ub=gp.GRB.INFINITY, vtype=GRB.CONTINUOUS, name='quantity_difference')
    # Auxillary variable for power excess
    var_aux_exc = model.addVars(n_hour, n_scen, lb=-gp.GRB.INFINITY, ub=gp.GRB.INFINITY, vtype=GRB.CONTINUOUS, name='auxillary_excess')
    # Auxillary variable for power deficit
    var_aux_def = model.addVars(n_hour, n_scen, lb=-gp.GRB.INFINITY, ub=gp.GRB.INFINITY, vtype=GRB.CONTINUOUS, name='auxillary_deficit')
    
    # Add the objective function to the model, sum on every t, separation of the conventional generation units and the wind farms
    model.setObjective(gp.quicksum(gp.quicksum((1/n_scen)*(in_sample['DA_price'][w][t]*var_qu_off[t] 
                                                           + in_sample['Binary_var'][w][t]*(coeff_up*in_sample['DA_price'][w][t]*var_aux_exc[t,w] - in_sample['DA_price'][w][t]*var_aux_def[t,w])
                                                           + (1-in_sample['Binary_var'][w][t])*(in_sample['DA_price'][w][t]*var_aux_exc[t,w] -coeff_down*in_sample['DA_price'][w][t]*var_aux_def[t,w])) 
                                               for w in range(n_scen)) for t in range(n_hour)), GRB.MAXIMIZE)
    
    #Add constraints to the model
    for t in range(n_hour):
        # Quantity offered limited to the maximum power of the wind turbine
        model.addConstr(var_qu_off[t] <= 200)
        model.addConstr(var_qu_off[t] >= 0)
        # Definition of the difference quantity variable
        for w in range(n_scen):
            model.addConstr(var_qu_diff[t,w] == in_sample['DA_forecast'][w][t] - var_qu_off[t])
            model.addConstr(var_qu_diff[t,w] == var_aux_exc[t,w] - var_aux_def[t,w])
            model.addConstr(var_aux_exc[t,w] >= 0)
            model.addConstr(var_aux_def[t,w] >= 0)
    
    #Solve the problem
    model.optimize()
    
    #Get the optimal values
    if model.status == GRB.OPTIMAL:
        
        # Create a list to store the optimal values of the variables
        optimal_qu_off = [round(var_qu_off[t].X,2) for t in range(n_hour)]
        # Value of the optimal objective
        optimal_obj = model.ObjVal
    
    else:
        print("Optimization did not converge to an optimal solution.")
    
    return(optimal_qu_off, optimal_obj)

optimal_qu_off_two, optimal_obj_two = Offering_two_price(in_sample, 0.9, 1.2)


##############################################
""" Compute the profits for each scenarios """
##############################################

def Profits_scenarios(in_sample, optimal_qu_off, price_scheme, n_scen) :
    #Number of units to take into account (based on data)
    # Number of hour
    n_hour = 24
    
    # Creating the list of profits
    profit = [0]*n_scen
    
    # Compute the profit for each scenarios
    for w in range(n_scen) :
        profit_w = 0
        for t in range(n_hour) :
            optimal_qu_diff = in_sample['DA_forecast'][w][t] - optimal_qu_off[t]
            # Profit depends on the price scheme
            if price_scheme == 1 :
                profit_w += in_sample['DA_price'][w][t]*optimal_qu_off[t] + in_sample['Binary_var'][w][t]*0.9*in_sample['DA_price'][w][t]*optimal_qu_diff + (1-in_sample['Binary_var'][w][t])*1.2*in_sample['DA_price'][w][t]*optimal_qu_diff
            elif price_scheme == 2 :
                profit_w +=in_sample['DA_price'][w][t]*optimal_qu_off[t] 
                if in_sample['Binary_var'][w][t] == 1 :
                    if optimal_qu_diff >= 0 :
                        profit_w += 0.9*in_sample['DA_price'][w][t]*optimal_qu_diff
                    else :
                        profit_w += in_sample['DA_price'][w][t]*optimal_qu_diff
                else :
                    if optimal_qu_diff >= 0 :
                        profit_w += in_sample['DA_price'][w][t]*optimal_qu_diff
                    else :
                        profit_w += 1.2*in_sample['DA_price'][w][t]*optimal_qu_diff
                    
        # Save the profit for scenario w
        profit[w] = profit_w
    
    return(profit)


def Show_distribution(profit, nb_bins) :
    
    # Create histogram
    plt.hist(profit, bins=nb_bins, color='blue', edgecolor='black')
    
    # Add labels and title
    plt.xlabel('Profit [$]')
    plt.ylabel('Number of occurence')
    #plt.title('Histogram of profits')
    
    # Display the plot
    plt.show()
    
if __name__ == "__main__":
    # Number of scenarios
    n_scen = len(in_sample)
    profit_one = Profits_scenarios(in_sample, optimal_qu_off_one, 1, n_scen)
    profit_two = Profits_scenarios(in_sample, optimal_qu_off_two, 2, n_scen)
    Show_distribution(profit_one, 80)
    Show_distribution(profit_two, 80)
    range_one = np.max(profit_one) - np.min(profit_one)
    range_two = np.max(profit_two) - np.min(profit_two)
    avg_one = np.mean(profit_one)
    avg_two = np.mean(profit_two)
    std_one = np.std(profit_one)
    std_two = np.std(profit_two)


##################################################
""" Variant to understand the two-price scheme """
##################################################

optimal_qu_off_two_var, optimal_obj_two = Offering_two_price(in_sample, 0.9, 1.1)

power_avg = [0]*24
binary = [0]*24
for i in range(250) :
    for j in range(24) :
        power_avg[j] += in_sample['DA_forecast'][i][j]
        binary[j] += in_sample['Binary_var'][i][j]
for j in range(24) :
    power_avg[j] = power_avg[j]/250
    binary[j] = binary[j]/250
    if binary[j] > 0.5 :
        binary[j] = 1 
    else :
        binary[j] = 0
    
Hours = [x for x in range(1,25)]

binary=np.array(binary)

# Create custom colormap based on background_colors
cmap = plt.cm.gray  # Use grayscale colormap
norm = plt.Normalize(binary.min(), binary.max())
colors = cmap(norm(binary))

# Create figure and axes
fig, ax = plt.subplots(figsize = (10, 7))

# Plot data with colored background
for i in range(1,25) :
    if binary[i-1] == 0:
        color = 'white'
    elif binary[i-1] == 1:
        color = '#D3D3D3'  # Light grey color
    ax.axvspan(i, i+1, color=color)
    
ax.step(Hours, optimal_qu_off_two, 'b', label='1.2 lambda', where='post')
ax.step(Hours, optimal_qu_off_two_var, 'g', label='1.1 lambda', where='post')
ax.step(Hours, power_avg, 'r--', label='Average power forecast', alpha=0.8, where='post')

# Customize plot
ax.legend()
# Set x-axis limits
ax.set_xlim(1, 24)
ax.set_xlabel('Hours')
ax.set_ylabel('Power [MW]')
# ax.grid(True)  # Optionally, add gridlines

# Show plot
plt.show()















