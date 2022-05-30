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
