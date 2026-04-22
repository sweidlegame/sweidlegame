class Producer: 
    # Represents an item the player can buy to generate currency automatically.
    def __init__(self, price, production):
        self.owned = 0           # How many of this producer the player has
        self.price = price       # Current cost to buy one
        self.production = production # How much currency this generates per unit

    def purchase(self):
        # Attempts to buy a producer. Deducts currency and scales the price.
        global currency
        global currencypersecond

        if currency >= self.price:
            currency -= self.price
            self.owned += 1

            # Increase the base Currency Per Second (CPS)
            currencypersecond += self.production

            # Exponential scaling: The price triples after every purchase
            self.price *= 3

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


# --- GLOBAL GAME STATE ---
currency = 0             # Total money available to spend
currencypersecond = 1    # Total money earned every second (starts at 1)

# Initialize the Drain: Occurs every 15 seconds (0.25 min), cuts income by 50% (0.5)
drain = Drain(0.25, 0.5)

# Initialize a list of Producer objects with varying prices and yields
producers = [
    Producer(10, 3),      # Cheap, low yield
    Producer(500, 10),
    Producer(2500, 25),
    Producer(10000, 100),
    Producer(50000, 300)  # Expensive, high yield
]


# --- API FUNCTIONS (Called by JavaScript) ---

def increment():
    # Manual click function: Adds CPS to currency immediately
    global currency
    currency += currencypersecond
    return currency


def second():
    # Main tick function: Ran every 1 second by the JS game loop
    global currency

    # Handle the drain countdown and status
    drain.drain_increment_sec()
    multiplier = drain.get_multiplier()

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
