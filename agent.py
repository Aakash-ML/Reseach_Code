class Agent:
    """ Base class for all Agent class """
    agentCount = 0

    def __init__(self, cash=1000, stocks=0):
        self.ID = agentCount # agent id unique to each agent.
        self.cash = cash
        self.stocks = stocks
        self.transaction = []
        Agent.agentCount += 1
    
    def displayCount(self):
        """ Print total number of agents program."""
        print("Total Agents number of agents are: %d" % Agent.agentCount)
    
    def sell_All(self, selling_rate):
        """ Model sell stocks at the given rate and convert it to cash """
        value = self.stocks* selling_rate
        self.stocks = 0
        self.cash  = self.cash + value
        self.transaction.append(value)
    
    def buy_All(self, buying_price):
        """ Model for Buying stocks at the given buying price. """
        stocks_No = self.cash / self.buying_price
        self.stocks = self.stocks + stocks_No
        self.cash = 0
        self.transaction.append(-self.cash)
    
    def displayTransiction():
        """ Display all the transactions made by the agent """
        print("The list of transiction done by agentId: {} is: {}".format(self.ID, self.transaction))


    

