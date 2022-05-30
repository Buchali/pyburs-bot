from types import SimpleNamespace

urls = SimpleNamespace(
    TSE_SYMBOL_INFO = "http://www.tsetmc.com/tsev2/data/instinfofast.aspx?i={index}&c=0&e=1",
    TSE_SYMBOL_ADDRESS = "http://tsetmc.com/Loader.aspx?ParTree=151311&i={index}",
)
