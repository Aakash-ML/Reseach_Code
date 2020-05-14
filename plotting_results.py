from agent import Agent
import pickle
import matplotlib as plt


with open('agent_data.pkl', 'rb') as f:
    agent_list = pickle.load(f)
print(len(agent_list))
print(agent_list[0].ROI)
for i in agent_list:
    print(i.transaction)
    print(i.ROI)
    print('\n')

