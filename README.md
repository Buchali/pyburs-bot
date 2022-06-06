# Burs Bot

This is a telegram bot for Tehran Stock Market. Using this bot to create porfolio and set stop-loss / take-profit for your stocks.

## How to run?
First, add `src` to `PYTHONPATH`:
```
export PYTHONPATH=${PWD}
```

Then, to run the Tehran Stock Market bot run the following code:
```
python src/bursbot.py
```

Or, to download Tehran Stock Market Data run the scraper:
```
pyrhon src/scraper.py
```

To run both the telegram bot and the data scraper simultaneously:
```
python src/run.py
```