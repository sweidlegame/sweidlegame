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

class Drain:
    def __init__(self, timeM, debuff):
        self.timeS = timeM * 60 # default time between drains
        self.nextDrainTimerSec = self.timeS  # convert mins -> secs
        self.currentDrainTimeS = 0 # the amount of time the drain has been active (sec)
        self.drainActive = False # controls if the drain is active
        self.drainDebuff = debuff # as a %; CPS * debuff = drainCPS

    def stop_drain(self):
        self.drainActive = False # disable drain


    def drain_increment_sec(self): # this should activate every second even when drain is off
        global currencypersecond
        global minigameactive

        if self.drainActive: # while the drain is active
            minigameactive = True
            currencypersecond = currencypersecond * self.drainDebuff # debuff production
            self.currentDrainTimeS += 1 # increment the amount of time the drain has been active

        else: # while the drain is inactive
            minigameactive = False
            self.nextDrainTimerSec -= 1 # reduce timer by one sec

        # start the next drain when the timer runs out
        if self.nextDrainTimerSec == 0:
            self.drainActive = True
            self.nextDrainTimerSec = self.timeS + self.currentDrainTimeS # reset timer to default + time left over
            self.currentDrainTimeS = 0 # reset current drain time


# --- GAME STATE ---
currency = 0 # total currency
currencypersecond = 1 # currency added tot total per second
minigameactive = False # if the drain minigame is active
# should the minigame var be here or in the drain class??


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
    Drain.drain_increment_sec() # update drain every second
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
