import time

import requests
import urwid
import yaml

from scroll import Scrollable, ScrollBar


def fetch():
    display = [
        ("bold text", f"{fix_string('Name (Prices ' + config['prices'] + ')', 28)}Market          Postmarket      Volume         \n")]
    quotes = []
    stocks = ",".join(config['stocks'])
    cryptos = ",".join([crypto + "-USD" for crypto in config['cryptos']])
    forexes = ",".join([forex + "=X" for forex in config['forexes']])
    others = ",".join(config['others'])
    query = ",".join([stocks, cryptos, forexes, others]).strip(",")
    data = session.get(
        f"https://query1.finance.yahoo.com/v7/finance/quote?fields=symbol,quoteType,regularMarketPrice,postMarketPrice,regularMarketVolume,shortName,regularMarketChangePercent,postMarketChangePercent,marketState&symbols={query}").json()

    if config['prices'] == "USD":
        rate = 1
    else:
        rate_data = session.get(
            f"https://query1.finance.yahoo.com/v7/finance/quote?fields=regularMarketPrice&symbols=USD{config['prices']}=X").json()
        if not rate_data["quoteResponse"]["result"][0]:
            raise Exception(
                "Configured display currency invalid, please refer to documentation.")
        rate = rate_data["quoteResponse"]["result"][0]["regularMarketPrice"]

    for quote in data["quoteResponse"]["result"]:
        try:
            quotes.append([fix_string(quote["symbol"] + ": " + quote["quoteType"], 28), fix_string(format(quote["regularMarketPrice"] * rate, ".4f"), 15), fix_string(format(quote.get("postMarketPrice", 0.00) * rate, ".4f"), 15), fix_string(quote.get("regularMarketVolume", 0), 15) +
                           "\n", fix_string(quote["shortName"], 28), fix_string(format(quote["regularMarketChangePercent"], ".2f") + "%", 15), fix_string(format(quote.get("postMarketChangePercent", 0.00), ".2f") + "%", 15), fix_string(quote["marketState"], 15) + "\n"])
        except:
            pass

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

    for line in quotes:
        for value in line:
            if "%" in value and "-" in value:
                display.append(("negative", value))
            elif "%" in value and value != "0.00%":
                display.append(("positive", value))
            elif "PRE" in value or "CLOSED" in value:  # also covers PREPRE
                display.append(("negative", value))
            elif "REGULAR" in value:
                display.append(("positive", value))
            else:
                display.append(("text", value))
    return display


def fix_string(string, length):
    string = str(string)
    string = string[:min(length, len(string) + 1)]
    string += " " * (length - len(string))
    return string + " "


def keystroke(key):
    if key == "C" or key == "c":
        load_config()
    elif key == "R" or key == "r":
        refresh(loop, None)
    elif key == "Q" or key == "q":
        raise urwid.ExitMainLoop()


def load_config():
    with open("config.yml", "r") as conf:
        global config
        config = yaml.full_load(conf)
        if not config["stocks"]:
            config["stocks"] = []
        if not config["cryptos"]:
            config["cryptos"] = []
        if not config["forexes"]:
            config["forexes"] = []
        if not config["others"]:
            config["others"] = []


def refresh(_loop, _data):
    global last_query, last_update
    last_query = fetch()
    last_update = time.strftime("%H:%M:%S", time.localtime())
    body.base_widget.set_text(last_query)
    footer.base_widget.set_text([("key", "C"), ("text", " Reload Config  "), ("key", "R"), ("text", " Refresh Prices  "), (
        "key", "Q"), ("text", " Quit Program  "), ("key", last_update), ("text", " Last Refresh")])
    _loop.set_alarm_in(config["refresh"], refresh)
    _loop.draw_screen()


load_config()

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

if config["colour"] == True:
    pass
elif config["colour"] == False:
    palette[0] = (palette[0][0], palette[2][1], palette[2][2])
    palette[1] = (palette[1][0], palette[2][1], palette[2][2])
else:
    raise Exception(
        "Configured colour invalid, please refer to documentation.")

header = f"stonktrack: {len(config['stocks'])} {'stocks' if len(config['stocks']) != 1 else 'stock'}, {len(config['cryptos'])} {'cryptocurrencies' if len(config['cryptos']) != 1 else 'cryptocurrency'}, {len(config['forexes'])} {'forexes' if len(config['forexes']) != 1 else 'forex'}, and {len(config['others'])} other {'investments' if len(config['others']) != 1 else 'investment'}"
header = urwid.Text([("title", header)])
body = urwid.LineBox(ScrollBar(Scrollable(
    urwid.Text([("text", "Loading...")]))))
footer = urwid.Text([("key", "C"), ("text", " Reload Config  "), ("key", "R"), ("text", " Refresh Prices  "),
                     ("key", "Q"), ("text", " Quit Program  "), ("key", "Never"), ("text", " Last Refresh")])

layout = urwid.Frame(header=header, body=body,
                     footer=footer, focus_part="footer")
layout.set_focus("body")
loop = urwid.MainLoop(
    layout, palette, unhandled_input=keystroke, handle_mouse=False)
last_update = ""
last_query = ""
session = requests.Session()

if __name__ == "__main__":
    loop.set_alarm_in(0, refresh)
    loop.run()
