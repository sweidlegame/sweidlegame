class Producer:
    def __init__(self,owned,price,production):
        # constructor (runs when object is created)
        self.owned = owned
        self.price = price
        self.production = production
        self.upgrademultiplier = 1

    def purchase(self):
       
        global currency
        if currency > price:
            currency = currency - price
            self.owned += 1
            price = price**1.05
        return

    def produce(self):
        return self.owned*self.production*self.multiplier

    def upgrade(self):
        self.upgrademodifier += 0.50







currency = 0
currencypersecond = 1

def increment():
    global currency
    currency = currency + (currencypersecond*0.4)
    return currency
def second():
    global currency
    currency = currency + currencypersecond
    return currency
def CPS():
    global currencypersecond
    return currencypersecond

