from types import SimpleNamespace

from src.utils.keyboard import create_keyboard

keys = SimpleNamespace(
    settings = ':gear: تنظیمات',
    add_symbol =  ':inbox_tray: افزودن نماد به پرتفو',
    portfolio = ':basket: پرتفو',
    exit = ':cross_mark: خروج',
    delete_symbol = ':wastebasket: حذف نماد',
    stop_loss = ':no_entry: تنظیم حد ضرر',
    take_profit = ':bullseye: تنظیم حد سود',
)
inline_keys = SimpleNamespace(
    delete_symbol = ':wastebasket: حذف نماد',
    stop_loss = ':no_entry: حد ضرر',
    take_profit = ':bullseye: حد سود',
)

keyboards = SimpleNamespace(
    main = create_keyboard(keys.portfolio),
    exit = create_keyboard(keys.exit),
    symbol = create_keyboard(keys.add_symbol, keys.exit, row_width=1),
    portfolio = create_keyboard(
        keys.take_profit, keys.stop_loss,
        keys.delete_symbol, keys.exit,
        row_width=2
        ),
)

inline_keyboards = SimpleNamespace(
    portfolio = create_keyboard(
    inline_keys.take_profit, inline_keys.stop_loss,
    inline_keys.delete_symbol,
    is_inline=True, inline_row_width=3,
    ),
)

states  = SimpleNamespace(
    MAIN = 'MAIN',
    ADDING_SYMBOL = 'ADDING SYMBOL',
    DELETE = 'DELETE',
    PORTFOLIO = 'PORTFOLIO',
    STOP_LOSS = 'STOP LOSS',
    TAKE_PROFIT = 'TAKE PROFIT',
)

urls = SimpleNamespace(
    TSE_SYMBOL_INFO = "http://www.tsetmc.com/tsev2/data/instinfofast.aspx?i={index}&c=0&e=1",
    TSE_SYMBOL_ADDRESS = "http://tsetmc.com/Loader.aspx?ParTree=151311&i={index}",
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
    '<strong>{symbol}</strong> با موفقیت از پورتفو حذف شد :wastebasket::check_mark_button:'
)
NOT_IN_PORTFOLIO_MESSAGE = (
    'متاسفانه، نمادی با نام {symbol} در پرتفو شما وجود ندارد! :thumbs_down:'
)
EMPTY_PORTFOLIO_MESSAGE = (
    "هیچ نمادی در پرتفو وجود ندارد! "
)

SYMBOL_INFO_MESSAGE = (
    '<strong>{symbol}</strong>'
    f"\n {30 * 'ـ'}"
    '\n\n قیمت معامله: {last_price} ریال'
)
STOP_LOSS_MESSAGE = (
    "نمادی که می‌خوای حد ضرر بذاری رو تایپ کن."
)
TAKE_PROFIT_MESSAGE = (
    "نمادی که می‌خوای حد سود بذاری رو تایپ کن."
)
