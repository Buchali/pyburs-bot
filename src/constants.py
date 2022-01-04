from types import SimpleNamespace

from src.utils.keyboard import create_keyboard

keys = SimpleNamespace(
    settings = ':gear: تنظیمات',
    add_stock =  ':plus: افزودن نماد به پرتفوی',
    portfolio = ':basket: پرتفوی',
    exit = ':cross_mark: خروج',
)

keyboards = SimpleNamespace(
    main = create_keyboard(keys.portfolio),
    exit = create_keyboard(keys.exit),
    stock = create_keyboard(keys.add_stock, keys.exit, row_width=1),
)

states  = SimpleNamespace(
    main = 'MAIN',
    stock = 'STOCK',
)

bot_messages = SimpleNamespace(
    exit = 'خارج شدید.',
    not_stock = 'متاسفانه، نماد مورد نظر شما یافت نشد! :thumbs_down:',
    stock_added = 'با موفقیت به پورتفوی اضافه شد :check_mark_button:',
    portfolio = f"پورتفوی شما :basket: \n {20 * '_'} \n\n",
    new_symbol = f"\n {70 * 'ـ'} \n\n می‌تونی نماد جدید تایپ کنی:"
)
