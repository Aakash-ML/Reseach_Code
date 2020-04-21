
class Agent:
    """ Base class for all Agent class """
    agentCount = 0

    def __init__(self,cash=1000, stocks=0):
        self.ID = Agent.agentCount # agent id unique to each agent.
        self.cash = cash
        self.stocks = stocks
        self.indicators = None # define at the time of creation.
        self.transaction = []
        self.pridiction_model = None
        self.model_Config = None
        self.ROI = []
        Agent.agentCount += 1
    
    def displayCount(self):
        """ Print total number of agents program."""
        print("Total Agents number of agents are: %d" % Agent.agentCount)
    
    def sell_All(self, selling_rate):
        """ Model sell stocks at the given rate and convert it to cash """
        value = self.stocks* selling_rate
        self.stocks = 0
        self.cash  = self.cash + value
        self.transaction.append(f"Sell {self.stocks} at {selling_rate} moneyLeft {self.cash}")
    
    def buy_All(self, buying_price):
        """ Model for Buying stocks at the given buying price. """
        stocks_No = int(self.cash / buying_price)
        self.stocks = self.stocks + stocks_No
        self.cash = self.cash - buying_price*stocks_No
        self.transaction.append(f"Buy {stocks_No} at {buying_price} moneyLeft {self.cash}")
    
    def displayTransiction(self):
        """ Display all the transactions made by the agent """
        return self.transaction
        #print("The list of transiction done by agentId: {} is: {}".format(self.ID, self.transaction))

    # def define_pridiction_model(self, model_list):
    #     if len(model_list)>no_pridictionModel:
    #         raise ValueError("More models then configuration per agent.")
    #     if type(model_list) == list():
    #         raise TypeError("Model list is not list")
    #     self.pridiction_model = model_list

    

