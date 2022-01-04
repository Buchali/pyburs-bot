from types import SimpleNamespace

from src.utils.keyboard import create_keyboard

keys = SimpleNamespace(
    settings = ':gear: تنظیمات',
    add_stock =  ':plus: افزودن نماد به پرتفو',
    portfolio = ':basket: پرتفو',
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

START_MESSAGE = (
    'سلام <strong>{first_name}</strong>، خوش اومدی :man_raising_hand:'
    '\n\n  نماد بورسی مورد نظرتو تایپ کن:'
)
EXIT_MESSAGE = (
    'خارج شدی.'
    f"\n {30 * 'ـ'}"
    '\n\n اگه می‌خوای نماد جدید تایپ کن.'
)
NOT_STOCK_MESSAGE = (
    'متاسفانه، نمادی با نام {symbol} یافت نشد! :thumbs_down:'
    f"\n {70 * 'ـ'}"
    '\n\n اگه می‌خوای نماد جدید تایپ کن.'
)
ADD_STOCK_MESSAGE = (
    '<strong>{symbol}</strong> با موفقیت به پورتفو اضافه شد :check_mark_button:'
    f"\n {70 * 'ـ'}"
    '\n\n اگه می‌خوای نماد جدید تایپ کن.'
)
PORTFOLIO_MESSAGE = (
    f"پورتفوی شما :basket: \n"
    f"{20 * '_'} \n\n"
    '{portfolio}'
)
