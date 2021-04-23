import time

import requests
import urwid
import yaml


def fetch():
    display = "Name (Prices USD)              Market          Postmarket      Volume          \n"
    quotes = []
    stocks = ",".join(config['stocks'])
    cryptos = ",".join([crypto + "-USD" for crypto in config['cryptos']])
    forexes = ",".join([forex + "USD=X" for forex in config['forexes']])
    others = ",".join(config['others'])
    query = ",".join([stocks, cryptos, forexes, others]).strip(",")
    data = requests.get(
        f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={query}").json()

    for quote in data["quoteResponse"]["result"]:
        quotes.append([fix_string(quote["symbol"] + ": " + quote["quoteType"], 30), fix_string(quote["regularMarketPrice"], 15), fix_string(quote.get("postMarketPrice", "0.00"), 15), fix_string(quote.get("regularMarketVolume", 0), 15) +
                       "\n", fix_string(quote["shortName"], 30), fix_string(str(quote["regularMarketChangePercent"]) + "%", 15), fix_string(str(quote.get("postMarketChangePercent", "0.00")) + "%", 15), fix_string(quote["marketState"], 15)])

    if config["sort"] == "alpha":
        quotes.sort(key=lambda x: x[4], reverse=config["reverse"])
    elif config["sort"] == "change":
        quotes.sort(key=lambda x: float(x[5].strip().strip(
            "%")) + float(x[6].strip().strip("%")), reverse=config["reverse"])
    elif config["sort"] == "symbol":
        quotes.sort(key=lambda x: x[0], reverse=config["reverse"])
    elif config["sort"] == "trading":
        quotes.sort(key=lambda x: x[7], reverse=config["reverse"])
    elif config["sort"] == "value":
        quotes.sort(key=lambda x: x[1], reverse=config["reverse"])

    display += "\n".join("".join(quote) for quote in quotes)
    return display


def fix_string(string, length):
    if type(string) != str:
        string = str(string)
    if len(string) > length:
        string = string[:length]
    else:
        string += " " * (length - len(string))
    return string + " "


def formatted_time():
    return time.strftime("%H:%M:%S", time.localtime())


def keystroke(key):
    if key == "up" or key == "page up":
        scroll_up(loop)
    elif key == "down" or key == "page down":
        scroll_down(loop)
    elif key == "r" or key == "R":
        refresh(loop, None)
    elif key == "q" or key == "Q":
        raise urwid.ExitMainLoop()


def refresh(_loop, _data):
    global last_query, last_query_size, last_update
    last_query = fetch()
    last_query_size = len(last_query)
    last_update = formatted_time()
    body.base_widget.set_text(last_query[scroll_location:])
    footer.base_widget.set_text([("key", "↑/PgUp"), ("text", " Up  "), ("key", "↓/PgDn"), ("text", " Down  "), ("key", "R"), ("text", " Refresh  "),
                                 ("key", "Q"), ("text", " Quit  "), ("key", f"{scroll_location}/{last_query_size}"), ("text", " Chars  "), ("key", last_update), ("text", " Updated")])
    _loop.set_alarm_in(config["refresh"], refresh)
    _loop.draw_screen()


def scroll_up(_loop):
    global scroll_location
    scroll_location = max(scroll_location - 80, 0)  # 80 chars
    body.base_widget.set_text(last_query[scroll_location:])
    footer.base_widget.set_text([("key", "↑/PgUp"), ("text", " Up  "), ("key", "↓/PgDn"), ("text", " Down  "), ("key", "R"), ("text", " Refresh  "),
                                 ("key", "Q"), ("text", " Quit  "), ("key", f"{scroll_location}/{last_query_size}"), ("text", " Chars  "), ("key", last_update), ("text", " Updated")])
    _loop.draw_screen()


def scroll_down(_loop):
    global scroll_location
    scroll_location = min(scroll_location + 80, last_query_size)  # 80 chars
    body.base_widget.set_text(last_query[scroll_location:])
    footer.base_widget.set_text([("key", "↑/PgUp"), ("text", " Up  "), ("key", "↓/PgDn"), ("text", " Down  "), ("key", "R"), ("text", " Refresh  "),
                                 ("key", "Q"), ("text", " Quit  "), ("key", f"{scroll_location}/{last_query_size}"), ("text", " Chars  "), ("key", last_update), ("text", " Updated")])
    _loop.draw_screen()


with open("config.yml", "r") as conf:
    config = yaml.full_load(conf)
    if not config["stocks"]:
        config["stocks"] = []
    if not config["cryptos"]:
        config["cryptos"] = []
    if not config["forexes"]:
        config["forexes"] = []
    if not config["others"]:
        config["others"] = []

if config["theme"] == "light":
    palette = [("positive", "light green", "white"), ("negative", "light red", "white"), ("text", "black", "white"),
               ("bold text", "black,bold", "white"), ("key", "black,standout,bold", "white"), ("title", "black,underline", "white")]
elif config["theme"] == "dark":
    palette = [("positive", "light green", "black"), ("negative", "light red", "black"), ("text", "white", "black"),
               ("bold text", "white,bold", "black"), ("key", "white,standout,bold", "black"), ("title", "white,underline", "black")]
elif config["theme"] == "default":
    palette = [("positive", "light green", ""), ("negative", "light red", ""), ("text", "", ""),
               ("bold text", "bold", ""), ("key", "standout,bold", ""), ("title", "underline", "")]
else:
    raise Exception("Configured theme invalid, please refer to documentation.")

header = f"stonktrack: {len(config['stocks'])} {'stocks' if len(config['stocks']) != 1 else 'stock'}, {len(config['cryptos'])} {'cryptocurrencies' if len(config['cryptos']) != 1 else 'cryptocurrency'}, {len(config['forexes'])} {'forexes' if len(config['forexes']) != 1 else 'forex'}, and {len(config['others'])} other {'investments' if len(config['others']) != 1 else 'investment'}"
header = urwid.Text([("title", header)])
body = urwid.Filler(urwid.Text([("text", "Loading prices...")]), valign="top")
body = urwid.LineBox(urwid.Padding(body, align="left"))
footer = urwid.Text([("key", "↑/PgUp"), ("text", " Up  "), ("key", "↓/PgDn"), ("text", " Down  "), ("key", "R"), ("text", " Refresh  "),
                     ("key", "Q"), ("text", " Quit  "), ("key", "0/0"), ("text", " Chars  "), ("key", "Never"), ("text", " Updated")])

layout = urwid.Frame(header=header, body=body,
                     footer=footer, focus_part="footer")
loop = urwid.MainLoop(
    layout, palette, unhandled_input=keystroke, handle_mouse=False)
scroll_location = 0
last_query_size = 0
last_update = ""
last_query = ""

if __name__ == "__main__":
    loop.set_alarm_in(0, refresh)
    loop.run()
