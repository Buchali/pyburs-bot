from types import SimpleNamespace

from src.utils.keyboard import create_keyboard

keys = SimpleNamespace(
    settings = ':gear: تنظیمات',
    add_symbol =  ':inbox_tray: افزودن نماد به پرتفو',
    portfolio = ':basket: پرتفو',
    exit = ':cross_mark: خروج',
    delete_symbol = ':wastebasket: حذف نماد'
)

keyboards = SimpleNamespace(
    main = create_keyboard(keys.portfolio),
    exit = create_keyboard(keys.exit),
    symbol = create_keyboard(keys.add_symbol, keys.exit, row_width=1),
    portfolio = create_keyboard(keys.delete_symbol, keys.exit, row_width=1),
)

states  = SimpleNamespace(
    MAIN = 'MAIN',
    ADDING_SYMBOL = 'ADDING SYMBOL',
    DELETE = 'DELETE',
    PORTFOLIO = 'PORTFOLIO',
)

START_MESSAGE = (
    'سلام <strong>{first_name}</strong>، خوش اومدی :man_raising_hand:'
    f"\n {70 * 'ـ'}"
    '\n  :red_triangle_pointed_down: این ربات برای یادآوری حدسود و حدضرر در بازار بورس تهران طراحی شده. :warning:'
    f"\n {70 * 'ـ'}"
    '\n\n  نماد بورسی مورد نظرتو تایپ کن. :speech_balloon:'
)
EXIT_MESSAGE = (
    'خارج شدی.'
    f"\n {30 * 'ـ'}"
    '\n\n اگه می‌خوای نماد جدید تایپ کن. :speech_balloon:'
)
NOT_SYMBOL_MESSAGE = (
    'متاسفانه، نمادی با نام {symbol} یافت نشد! :thumbs_down:'
    f"\n {70 * 'ـ'}"
    '\n\n اگه می‌خوای نماد جدید تایپ کن. :speech_balloon:'
)
ADD_SYMBOL_MESSAGE = (
    '<strong>{symbol}</strong> با موفقیت به پورتفو اضافه شد :check_mark_button:'
    f"\n {70 * 'ـ'}"
    '\n\n اگه می‌خوای نماد جدید تایپ کن. :speech_balloon:'
)
PORTFOLIO_MESSAGE = (
    "پورتفوی شما :basket: \n"
    f"{20 * '_'} \n\n"
    '{portfolio}'
)
DELETE_SYMBOL_MESSAGE = (
    "نمادی که می‌خوای حذف شه رو تایپ کن."
)
DELETED_MESSAGE = (
    '<strong>{symbol}</strong> با موفقیت از پورتفو حذف شد :basket::check_mark_button:'
)
NOT_IN_PORTFOLIO_MESSAGE = (
    'متاسفانه، نمادی با نام {symbol} در پرتفو شما وجود ندارد! :thumbs_down:'
)
EMPTY_PORTFOLIO_MESSAGE = (
    "هیچ نمادی در پرتفو وجود ندارد! "
)