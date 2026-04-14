currency = 0
currencypersecond = 1

def increment():
    global currency
    currency = currency + currencypersecond + 1
    return currency
