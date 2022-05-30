START = (
    'سلام <strong>{first_name}</strong>، خوش اومدی :man_raising_hand:'
    f"\n {70 * 'ـ'}"
    '\n  :red_triangle_pointed_down: این ربات برای یادآوری حدسود و حدضرر در بازار بورس تهران طراحی شده. :warning:'
    f"\n {70 * 'ـ'}"
    '\n\n  نماد بورسی مورد نظرتو تایپ کن. :speech_balloon:'
)
EXIT = (
    'خارج شدی.'
    f"\n {30 * 'ـ'}"
    '\n\n اگه می‌خوای نماد جدید تایپ کن. :speech_balloon:'
)
NOT_SYMBOL = (
    'متاسفانه، نمادی با نام {symbol} یافت نشد! :thumbs_down:'
    f"\n {70 * 'ـ'}"
    '\n\n اگه می‌خوای نماد جدید تایپ کن. :speech_balloon:'
)
ADD_SYMBOL = (
    '<strong>{symbol}</strong> با موفقیت به پورتفو اضافه شد :check_mark_button:'
    f"\n {70 * 'ـ'}"
    '\n\n اگه می‌خوای نماد جدید تایپ کن. :speech_balloon:'
)
PORTFOLIO = (
    "پورتفوی شما :basket: \n"
    f"{20 * '_'} \n\n"
)
PORTFOLIO_SYMBOL = (
    '{symbol}\n\n'
    '|قیمت معامله: {last_price} | حد ضرر: {stop_loss} | حد سود: {take_profit}|'
)
DELETE_SYMBOL = (
    "نمادی که می‌خوای حذف شه رو تایپ کن."
)
DELETED = (
    '{symbol} با موفقیت از پورتفو حذف شد :wastebasket::check_mark_button:'
)
NOT_IN_PORTFOLIO = (
    'متاسفانه، نمادی با نام {symbol} در پرتفو شما وجود ندارد! :thumbs_down:'
)
EMPTY_PORTFOLIO = (
    "هیچ نمادی در پرتفو وجود ندارد! "
)
SYMBOL_INFO = (
    '<strong>{symbol}</strong>'
    f"\n {30 * 'ـ'}"
    '\n\n قیمت معامله: {last_price} ریال'
)
ASK_STOP_LOSS = (
    "حد ضرر مورد نظرتو برای نماد {symbol} به ریال وارد کن."
)
ASK_TAKE_PROFIT = (
    "حد سود مورد نظرتو برای نماد {symbol} به ریال وارد کن."
)
ISIN_PORTFOLIO = (
    'نماد <strong>{}</strong> قبلاً به پرتفو اضافه شده است!'
)
STOP_LOSS_ADDED = (
    'حد ضرر نماد {symbol} با موفقیت تنظیم شد. :check_mark_button:'
)
TAKE_PROFIT_ADDED = (
    'حد سود نماد {symbol} با موفقیت تنظیم شد. :check_mark_button:'
)
