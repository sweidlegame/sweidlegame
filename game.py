import random
import math
import js
import json

class Producer: 
    # Represents an item the player can buy to generate currency automatically.
    def __init__(self, price, production):
        self.owned = 0           # How many of this producer the player has
        self.price = price       # Current cost to buy one
        self.production = production # How much currency this generates per unit
	
    def setOwned(self, owned):
        global currencypersecond
        self.owned = owned
	
        currencypersecond = self.production * owned

        for i in range(owned):
	        self.price = self.price ** 1.12
	        self.price = math.ceil(self.price)

    def purchase(self):
        # Attempts to buy a producer. Deducts currency and scales the price.
        global currency
        global currencypersecond

        if currency >= self.price:
            currency -= self.price
            self.owned += 1

            # Increase the base Currency Per Second (CPS)
            currencypersecond += self.production

            # Exponential scaling: The price increases exponentially to prevent reliance on one producer, but still keep them useful for a few sequential purchases
            self.price = self.price ** 1.12
            self.price = math.ceil(self.price)

        return currency


class Drain:
    # A mechanic that periodically reduces the player's income (a 'debuff').
    def __init__(self, timeM, debuff):
        self.timeS = timeM * 60           # Convert minutes input to seconds
        self.nextDrainTimerSec = self.timeS # Countdown until the next drain starts
        self.drainActive = False          # Current state of the drain
        self.drainDebuff = debuff         # The multiplier (e.g., 0.5 = 50% income)

    def stop_drain(self):
        # Resets the drain timer and deactivates the penalty.
        self.drainActive = False
        self.nextDrainTimerSec = self.timeS

    def drain_increment_sec(self):
        # Reduces the timer by 1 second. If it hits 0, the drain activates
        if self.drainActive:
            return # Don't count down if already active

        self.nextDrainTimerSec -= 1

        if self.nextDrainTimerSec <= 0:
            self.drainActive = True

    def get_multiplier(self):
        # Returns the current income multiplier (1.0 if healthy, debuff if active)
        if self.drainActive:
            return self.drainDebuff
        return 1
class Simon: 
    # Represents an item the player can buy to generate currency automatically.
    def __init__(self, streak, requirement):
        self.streak = streak         # Highest streak, so it can provide bonuses later
        self.requirement = requirement     # what streak is required to remove drain?
        self.sequence = []
        self.currentstreak = 0
        self.passed = False
    def clearlose(self):
        #Clear for initialization or loss
        self.currentstreak = 0
        self.sequence = []
        self.step()
    def clearwin(self):
        #Repel drain and clear for next use on event of loss of a streak that already passed the victory point
        drain.stop_drain()
        self.clearlose()

    def genentry(self):
        return random.choice(["red", "green", "blue","yellow"])
        
    def step(self):
        self.sequence.append(self.genentry())
    def attempt(self,playerseq):
        i = 0
        while i < len(self.sequence):
            if len(playerseq) == len(self.sequence) and playerseq[i] == self.sequence[i]:
                True
            else:
                if self.currentstreak > self.requirement:
                    self.clearwin()
                else:
                    self.clearlose()
                return 0
            i = i+1
        self.currentstreak += 1
        self.step()
        if self.currentstreak > self.streak:
            self.streak = self.currentstreak
        return 1
    def gethighscore(self):
        return self.streak
    def getstreak(self):
        return self.currentstreak
    def getsequence(self):
        return self.sequence


class SaveFile:
    def __init__(self):
        self.data = {}


    def savefile(self, currency, producers, streak):
        self.data["Currency"] = currency
        self.data["Streak"] = streak

        for i in range(len(producers)):
            self.data[i] = producers[i].owned

        json_data = json.dumps(self.data)
        js.localStorage.setItem("saved_data", json_data)


    def loadfile(self):
        raw_data = js.localStorage.getItem("saved_data")
		
        if raw_data:
            return json.load(raw_data)
		
        return {}


# --- GLOBAL GAME STATE ---
currency = 10             # Total money available to spend
currencypersecond = 0    # Total money earned every second (starts at 1)
Simon = Simon(0,3)
Simon.clearlose()
# Initialize the Drain: Occurs every 15 seconds (0.25 min), cuts income by 50% (0.5)
drain = Drain(0.25, 0.5)
savef = SaveFile()

# Initialize a list of Producer objects with varying prices and yields
producers = [
    Producer(10, 3),      # Cheap, low yield
    Producer(500, 10),
    Producer(2500, 25),
    Producer(10000, 100),
    Producer(50000, 300)  # Expensive, high yield
]



# --- API FUNCTIONS (Called by JavaScript) ---
def save():
	savef.savefile(currency, producers, Simon.gethighscore())

def load():
    data = savef.loadfile()
	
    if data:
        currency = data["Currency"]
        Simon.streak = data["Streak"]
	
        for i in range(len(producers)):
            producers[i].setOwned(data[i])
		

def increment():
    # Manual click function: Adds CPS to currency immediately
    global currency

    multiplier = drain.get_multiplier()
    multiplier += 0.05*multiplier*Simon.gethighscore()
    currency += 0.35*currencypersecond*multiplier
    if currencypersecond == 0:
        currency += 1
    
    currency = math.ceil(currency)
   
    return currency


def second():
    # Main tick function: Ran every 1 second by the JS game loop
    global currency

    # Handle the drain countdown and status
    drain.drain_increment_sec()
    multiplier = drain.get_multiplier()
    multiplier += 0.05*multiplier*Simon.gethighscore()

    # Calculate income: (Base CPS) * (0.5 if drain is active, else 1.0)
    currency += currencypersecond * multiplier
    return currency


def CPS():
    # Returns the current base Currency Per Second
    return currencypersecond


def buy_producer(index):
    # Bridge function to allow JS to trigger a purchase by index
    return producers[index].purchase()


def get_price(index):
    # Returns the current price of a specific producer
    return producers[index].price


def get_owned(index):
    # Returns how many of a specific producer are owned
    return producers[index].owned


def get_production(index):
    # Returns how much a single unit of this producer generates
    return producers[index].production


def is_drain_active():
    # Checks if the penalty is currently affecting income
    return drain.drainActive

def get_drain_multiplier():
    # Checks the severity of the current drain
    return drain.get_multiplier()

def stop_drain():
    # Allows the player to 'fix' the drain and resume normal production
    drain.stop_drain()
    return currency
def simongetstreak():
    return Simon.getstreak()
def attempt(sequence):
    return Simon.attempt(sequence)
def getcurrency():
    return currency
def simongethigh():
    return Simon.gethighscore()
def simongetsequence():
    return Simon.getsequence()
