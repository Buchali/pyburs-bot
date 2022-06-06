# Burs Bot

This is a telegram bot for Tehran Stock Market. Using this, make a porfolio and set stop loss / take profit alerts.

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

To run both the telegram bot and the data scraper them simultaneously:
```
python src/run.py
```