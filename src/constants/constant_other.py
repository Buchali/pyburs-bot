from types import SimpleNamespace


states  = SimpleNamespace(
    MAIN = 'MAIN',
    ADDING_SYMBOL = 'ADDING SYMBOL',
    DELETE = 'DELETE',
    PORTFOLIO = 'PORTFOLIO',
    STOP_LOSS = 'STOP LOSS',
    TAKE_PROFIT = 'TAKE PROFIT',
)

portfo_attr = SimpleNamespace(
    STOP_LOSS = 'stop_loss',
    TAKE_PROFIT = 'take_profit'
)
