"""
This is the main evalutaion algorithm for research.
"""

__author__ = "Aakash Patel"
__version__ = "0.1.0"
__license__ = "MIT"
import math
import os
import neat
import random
random.seed(1234)
from agent import Agent
import configparser
from pprint import pprint
import pandas as pd
import pickle


# config
# global variables
No_of_Agents = 50
Shift_data_by = 5
Maximum_Generations = 250
# Number of days used for training
num_to_train = 15
# 
Today = 20
# trade for days
days = 21
tecnical_indicator_score = {i : 0 for i in range(1,15)}
df = pd.read_csv("GA_Data_with_TI_Normalized.csv")
print("Data loaded !!")
pprint(df.head())
pprint(df.columns)


def create_config(inputs):
    """
    this function takes inputs = list of input to ANN
    creates a temp file for this inputs.
    """
    try:
        os.remove('temp.conf')
    except OSError:
        pass
    config = configparser.ConfigParser()
    config.read('./NEAT-Try/XOR-conf')
    print("Loading config!")
    config['DefaultGenome']['num_inputs'] = str(len(inputs))
    config.add_section('Inputs')
    config.set('Inputs','Indicators', str(inputs)[1:-1])
    with open('temp.conf','w') as f:
        config.write(f)
    print("Temp config created!")

def input_for_training(indicators):
    """Return list contating the tuple of required inputs"""
    # indicators = [i+Shift_data_by for i in indicators]
    sub_data = df.iloc[Today-num_to_train:Today,indicators]
    return list(sub_data.itertuples(index=False, name=None))

def input_for_test(indicators):
    """Return list contating the tuple of required inputs"""
    # indicators = [i+Shift_data_by for i in indicators]
    sub_data = df.iloc[Today:Today+days,indicators]
    return list(sub_data.itertuples(index=False, name=None))

def output_for_training():
    """Return list contating the tuple of required inputs"""
    # indicators = [i+Shift_data_by for i in indicators]
    sub_data = df.iloc[Today-num_to_train+1:Today+1,20]
    #pprint(sub_data.values)
    return sub_data.values

def output_for_test():
    """Return list contating the tuple of required inputs"""
    # indicators = [i+Shift_data_by for i in indicators]
    sub_data = df.iloc[Today+1:Today+1+days,20]
    #pprint(sub_data.values)
    return sub_data.values

def eval_genomes(genomes, config):
    """
    To evaluate each model on the baises on ROI
    """
    tempConfig = configparser.ConfigParser()
    tempConfig.read('temp.conf')
    print("Loading temp config!")
    indi = tempConfig.get('Inputs','Indicators')
    indi = [int(i) for i in indi.split(',')]
    #print(type(indi))
    inputs = input_for_training(indi) # take it from inputs_file
    outputs = output_for_training() # same for it.
    for genome_id, genome in genomes:
        money = 1000
        stocks = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for xi, xo in zip(inputs, outputs):
            output = net.activate(xi)
            output = output[0]
            if output > 0.75:
                buy = int(money/xo)
                if buy> 1:
                    stocks += buy
                    money = money - buy*xo
            elif output < 0.25:
                if stocks > 1:
                    money = money + stocks*xo
                    stocks = 0
        genome.fitness = ((money+stocks*outputs[-1])-1000)/1000

def create_Model(Maximum_Generations):
    """
    takes Maximum_Generations as input, returns-> winner , config
    Uses NEAT to evolve model params.
    """
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        './temp.conf')

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(False))
    # Run until a solution is found.
    winner = p.run(eval_genomes, n=Maximum_Generations)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    return winner , config

#Step 1> 50 agents are created and each agent selects a 
# list of technical indicators(based on there score)to trade.
def select_indicators(agent_list):
    for agent in agent_list:
        agent.indicators = random.sample(range(1,15),random.randint(0,len(tecnical_indicator_score)))
        agent.indicators = [i+Shift_data_by for i in agent.indicators]
        agent.indicators.extend([1,2,3,4])
    return agent_list

#step2> each agent then uses NEAT to get the perfect neural network model 
# to trade with the selected technical indicators from step 1. [To get the model from neat we use 
# past 15 days data and we try to predict the Buy or Sell action rather than the price of the stock,
#  fitness will be calculated based on the ROI for each gene, also the termination will be 150 generations,
#  i.e after 150 generations we take the best-performing individual as winner model for the agent]
def indv_lear(agent_list):
    for agent in agent_list:
        create_config(agent.indicators)
        # Use the created config to get 
        agent.pridiction_model,agent.model_Config = create_Model(Maximum_Generations)
        print(f"agent {agent.ID} learned the best model!! ")  

    return agent_list


#step 3> The agent then trades using the winner model obtained in step 2, for 1 month or 21 trading days, 
def trade_with_model(agent):
    inputs = input_for_training(agent.indicators) # take it from inputs_file
    outputs = output_for_training()
    winner_net = neat.nn.FeedForwardNetwork.create(agent.pridiction_model, agent.model_Config)
    money = agent.cash
    stocks = agent.stocks
    pvalue = (money+stocks*outputs[0])
    for xi, xo in zip(inputs, outputs):
            output = winner_net.activate(xi)
            output = output[0]
            if output > 0.75:
                buy = int(agent.cash/xo)
                if buy> 1:
                    agent.buy_All(xo)
            elif output < 0.25:
                if agent.stocks > 1:
                    agent.sell_All
    ROI = ((agent.cash+agent.stocks*outputs[-1])-pvalue)/pvalue
    agent.ROI.append(ROI)
    print(f"agent {agent.ID} Traded for {days} with best Model ROI {ROI}")
    print(f"Tranictions for {agent.ID}")
    pprint(agent.transaction)
    print('*'*20)
    return agent  

def norm_dic(dic_data):
    max_val = max(dic_data.values())
    min_val = min(dic_data.values())
    for k in dic_data:
        dic_data[k] = (dic_data[k] - min_val) / (max_val - min_val)
    return dic_data
#Step 4> now after 21 trading days the ROI is calculated for each agent and ranked accordingly,
#  and the technical indicators used by them have also scored accordingly.
def score_TI(agent_list):
    agent_score = {}
    # get roi per agent
    for i,agent in enumerate(agent_list):
        agent_score[i] = agent.ROI[-1]
    # normalize the roi
    agent_score = norm_dic(agent_score)
    # factor=1.0/sum(agent_score.values())
    # for k in agent_score:
    #     agent_score[k] = agent_score[k]*factor
    # adding the values to the ti score
    global tecnical_indicator_score
    for i in agent_score:
        ind = [a-Shift_data_by for a in agent_list[i].indicators if a not in [1,2,3,4]]
        for b in ind:
            tecnical_indicator_score[b] += agent_score[i]
    # fac = 1.0/sum(tecnical_indicator_score.values())
    # for key in tecnical_indicator_score:
    #     tecnical_indicator_score[key] = tecnical_indicator_score[key]*fac
    tecnical_indicator_score = norm_dic(tecnical_indicator_score) 

#step5> again the process from step 1 to step 4 is repeated for 6 months.

#!/usr/bin/env python3

def main():
    """ Main entry point of the app """
    print("hello world")
    pprint(tecnical_indicator_score)
    agent_list = []
    for _ in range(No_of_Agents):
        inv = Agent()
        agent_list.append(inv)
    
    for _ in range(5):
        # step 1:- get technical indicators
        agent_list = select_indicators(agent_list)
        #step 2:- get the perfect neural network model
        agent_list = indv_lear(agent_list)
        # step 3:- Use best model for each agent to trade for 21 days
        for agent in agent_list:
            agent = trade_with_model(agent)
        # step 4:- Update the Technical indicator based on the roi of last 21 days
        # This steps helps to collectively learn the best TI
        score_TI(agent_list)
        #step5> again the process from step 1 to step 4 is repeated for 6 months.
        global Today 
        Today = Today + days
    
    pprint(tecnical_indicator_score)
    # saving the agentdata for further analysis
    with open('agent_data.pkl','wb') as f:
        pickle.dump(agent_list,f)



    


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()