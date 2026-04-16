class Producer:
    def __init__(self, price, production):
        self.owned = 0
        self.price = price
        self.production = production

    def purchase(self):
        global currency
        global currencypersecond

        if currency >= self.price:
            currency -= self.price
            self.owned += 1

            # Add CPS
            currencypersecond += self.production

            # Scale cost
            self.price *= 3

        return currency


# --- GAME STATE ---
currency = 0
currencypersecond = 1

# Create 5 producers
producers = [
    Producer(10, 3),     # Producer 1
    Producer(500, 10),   # Producer 2
    Producer(2500, 25),  # Producer 3
    Producer(10000, 100),# Producer 4
    Producer(50000, 300) # Producer 5
]


# --- FUNCTIONS FOR JS ---
def increment():
    global currency
    global currencypersecond

    currency += currencypersecond
    return currency

def second():
    global currency
    currency += currencypersecond
    return currency

def CPS():
    return currencypersecond

def buy_producer(index):
    return producers[index].purchase()

def get_price(index):
    return producers[index].price

def get_owned(index):
    return producers[index].owned
    
def get_production(index):
    return producers[index].production
