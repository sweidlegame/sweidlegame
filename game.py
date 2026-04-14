currency = 0
currencypersecond = 1

def increment():
    global currency
    currency = currency + (currencypersecond/0.5)
    return currency
def second():
    global currency
    currency = currency + currencypersecond
    return currency
