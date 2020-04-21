"""
try using the Neat as pridicting model for the project.
"""
import numpy as np

class NeuralNetwork():
    '''
    The Neural Network to predict the buy or sell signal based on 
    the given technical indicators. 
    for 
    sigmoid = if output < 0.25, sell(0), elif output > 0.75, buy(1)
    tanh = if output < -0.5, sell(0), elif output > 0.5, buy(1)

    '''
    
    def __init__(self, hidden, activation_fun,weights):
        # seeding for random number generation
        np.random.seed(1)
        # hidden layer is present (True) or not (False)
        self.hidden = hidden
        # which activation funtion to use sigmoid,tanh
        self.activation_fun = activation_fun        
        #converting weights to a 3 by 1 matrix with values from -1 to 1 and mean of 0
        self.weights = weights

    def sigmoid(self, x):
        #applying the sigmoid function
        return 1 / (1 + np.exp(-x))
    
    def tanh(self,x):
        return np.tanh(x)

    def sigmoid_derivative(self, x):
        #computing derivative to the Sigmoid function
        return x * (1 - x)

    def Output(self, inputs):
        #passing the inputs via the neuron to get output   
        #converting values to floats
        
        inputs = inputs.astype(float)
        output = self.sigmoid(np.dot(inputs, self.synaptic_weights))
        return output


if __name__ == "__main__":

    #initializing the neuron class
    neural_network = NeuralNetwork()

    print("Beginning Randomly Generated Weights: ")
    print(neural_network.synaptic_weights)

    #training data consisting of 4 examples--3 input values and 1 output
    training_inputs = np.array([[0,0,1],
                                [1,1,1],
                                [1,0,1],
                                [0,1,1]])

    training_outputs = np.array([[0,1,1,0]]).T

    #training taking place
    neural_network.train(training_inputs, training_outputs, 15000)

    print("Ending Weights After Training: ")
    print(neural_network.synaptic_weights)

    user_input_one = str(input("User Input One: "))
    user_input_two = str(input("User Input Two: "))
    user_input_three = str(input("User Input Three: "))
    
    print("Considering New Situation: ", user_input_one, user_input_two, user_input_three)
    print("New Output data: ")
    print(neural_network.think(np.array([user_input_one, user_input_two, user_input_three])))
    print("Wow, we did it!")
