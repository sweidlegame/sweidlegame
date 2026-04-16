class Producer:
    def __init__(self, owned, price, production):
        self.owned = owned
        self.price = price
        self.production = production

    def purchase(self):
        global currency
        global currencypersecond

        if currency >= self.price:
            currency -= self.price
            self.owned += 1

            # Increase CPS
            currencypersecond += self.production

            # Increase price for next purchase
            self.price = self.price * 3

        return currency

    def get_price(self):
        return self.price


currency = 0
currencypersecond = 1

producer1 = Producer(0, 10, 3)


def increment():
    global currency
    currency += 1
    return currency

def second():
    global currency
    currency += currencypersecond
    return currency

def CPS():
    return currencypersecond

def buy_producer():
    return producer1.purchase()

def producer_price():
    return producer1.get_price()



