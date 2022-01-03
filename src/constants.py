from types import SimpleNamespace

from src.utils.keyboard import create_keyboard

keys = SimpleNamespace(
    settings = ':gear: تنظیمات',
    add_stock =  ':plus: افزودن نماد',
    portfolio = ':basket: پرتفوی',
    exit = ':cross_mark: خروج',
)

keyboards = SimpleNamespace(
    main = create_keyboard(keys.portfolio, keys.add_stock),
    exit = create_keyboard(keys.exit),
)

states  = SimpleNamespace(
    main = 'MAIN',
    add_stock = 'ADDING A STOCK',
)

bot_messages = SimpleNamespace(
    start = ' سلام، خوش آمدی',
    add_stock = 'یکی از نماد‌های بورس تهران را تایپ کن:',
    exit = 'خارج شدید.',
)
