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
