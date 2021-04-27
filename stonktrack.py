import time

import urwid
import yaml

from requests import Session
from scroll import Scrollable, ScrollBar


def fetch():
    display = [
        ("bold text",
         f"{fix_string('Name (Prices ' + config['prices'] + ')', 28)}Market          Postmarket      Volume         \n")]
    quotes = []
    global data
    data = session.get(
        f"https://query1.finance.yahoo.com/v7/finance/quote?fields=symbol,quoteType,regularMarketPrice,postMarketPrice,regularMarketVolume,shortName,longName,regularMarketChangePercent,postMarketChangePercent,marketState&symbols={query}").json()["quoteResponse"]["result"]

    if config["prices"] == "USD":
        rate = 1
    else:
        rate_data = session.get(
            f"https://query1.finance.yahoo.com/v7/finance/quote?fields=regularMarketPrice&symbols=USD{config['prices']}=X").json()["quoteResponse"]["result"]
        if not rate_data[0]:
            raise Exception(
                "Configured display currency invalid, please refer to documentation.")
        rate = rate_data[0]["regularMarketPrice"]

    if config["sort"] == "alpha":
        data.sort(key=lambda x: x["shortName"], reverse=config["reverse"])
    elif config["sort"] == "change":
        data.sort(
            key=lambda x: x["regularMarketChangePercent"] +
            x.get(
                "postMarketChangePercent",
                0.00),
            reverse=config["reverse"])
    elif config["sort"] == "symbol":
        data.sort(key=lambda x: x["symbol"], reverse=config["reverse"])
    elif config["sort"] == "trading":
        data.sort(key=lambda x: x["marketState"], reverse=config["reverse"])
    elif config["sort"] == "value":
        data.sort(
            key=lambda x: x["regularMarketPrice"],
            reverse=config["reverse"])

    for quote in data:
        try:
            quotes.append(
                [quote["symbol"] + ": " + quote["quoteType"],
                 fix_string(
                     format(quote["regularMarketPrice"] * rate, ".4f"),
                     15),
                 fix_string(
                     format(
                         quote.get("postMarketPrice", 0.00) * rate, ".4f"),
                     15),
                 fix_string(quote.get("regularMarketVolume", 0),
                            15) + "\n", fix_string(quote["shortName"],
                                                   28),
                 fix_string(
                     format(quote["regularMarketChangePercent"],
                            ".2f") + "%", 15),
                 fix_string(
                     format(
                         quote.get("postMarketChangePercent", 0.00),
                         ".2f") + "%", 15),
                 fix_string(quote["marketState"],
                            15) + "\n"])  # fix 0th later
        except BaseException:
            pass

    for i in range(len(quotes)):
        quotes[i][0] = fix_string(str(i + 1) + ". " + quotes[i][0], 28)
    quotes[-1][-1] = quotes[-1][-1].strip()  # strip last newline

    tracked = query.count(",") + 1 - len(data)
    if tracked:  # if data is missing
        quotes.append(
            f"\n\nData unavailable for {tracked} {'investments' if tracked != 1 else 'investment'}.")

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


def focus_fetch():
    focus = []
    focus_data = data[focus_index]  # use preexisting query for speed

    focus.append(
        ("title",
         f"{focus_index + 1}. {focus_data['symbol']}: {focus_data['longName'] if 'longName' in focus_data else focus_data['shortName']} ({focus_data['quoteType']}) (Data from {focus_data['fullExchangeName']})"))
    return focus


def fix_string(string, length):
    string = str(string)
    string = string[:min(length, len(string) + 1)]
    string += " " * (length - len(string))
    return string + " "


def keystroke(key):
    global focus_index
    if key == "C" or key == "c":
        load_config()
    elif key == "left":
        focus_index = (focus_index - 1) % len(data)
        refresh(loop, None)
    elif key == "right":
        focus_index = (focus_index + 1) % len(data)
        refresh(loop, None)
    elif key == "R" or key == "r":
        refresh(loop, None)
    elif key == "Q" or key == "q":
        raise urwid.ExitMainLoop()


def load_config():
    global config, query
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
    stocks = ",".join(config['stocks'])
    cryptos = ",".join([crypto + "-USD" for crypto in config['cryptos']])
    forexes = ",".join([forex + "=X" for forex in config['forexes']])
    others = ",".join(config['others'])
    query = ",".join([stocks, cryptos, forexes, others]).strip(",")


def refresh(_loop, _data):
    global last_update
    last_update = time.strftime("%H:%M:%S", time.localtime())
    body.base_widget.contents[0][0].base_widget.set_text(fetch())
    if config["focus"]:
        body.base_widget.contents[2][0].base_widget.set_text(focus_fetch())
    footer.base_widget.contents[1][0].base_widget.set_text(
        [("key", "R"),
         ("text", " Reload "),
         ("key", "◀ ▶ "),  # displays incorrectly without extra space
         ("text", " Toggle "),
         ("key", "C"),
         ("text", " Config "),
         ("key", "Q"),
         ("text", " Quit "),
         ("text", "│ "),
         ("key", sort_name()),
         ("text", " Sort "),
         ("key", str(focus_index + 1)),
         ("text", " Focus "),
         ("key", last_update),
         ("text", " Updated")])
    _loop.set_alarm_in(config["refresh"], refresh)
    _loop.draw_screen()


def sort_name():
    if config["reverse"]:
        return "▼ " + config["sort"].capitalize()
    else:
        return "▲ " + config["sort"].capitalize()


load_config()

if config["theme"] == "light":
    palette = [
        ("positive", "light green", "white"),
        ("negative", "light red", "white"),
        ("text", "black", "white"),
        ("bold text", "black,bold", "white"),
        ("key", "black,standout,bold", "white"),
        ("title", "black,underline", "white")]
elif config["theme"] == "dark":
    palette = [
        ("positive", "light green", "black"),
        ("negative", "light red", "black"),
        ("text", "white", "black"),
        ("bold text", "white,bold", "black"),
        ("key", "white,standout,bold", "black"),
        ("title", "white,underline", "black")]
elif config["theme"] == "default":
    palette = [
        ("positive", "light green", ""),
        ("negative", "light red", ""),
        ("text", "", ""),
        ("bold text", "bold", ""),
        ("key", "standout,bold", ""),
        ("title", "underline", "")]
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

last_update = "Never"
focus_index = 0
session = Session()

header = f"stonktrack: tracking {len(config['stocks'])} {'stocks' if len(config['stocks']) != 1 else 'stock'}, {len(config['cryptos'])} {'cryptocurrencies' if len(config['cryptos']) != 1 else 'cryptocurrency'}, {len(config['forexes'])} {'forexes' if len(config['forexes']) != 1 else 'forex'}, and {len(config['others'])} {'others' if len(config['others']) != 1 else 'other'}"
header = urwid.Pile([urwid.Text([("title", header)]), urwid.Divider("─")])
if config["focus"]:
    body = urwid.Pile(
        [urwid.LineBox(
            urwid.Text([("text", "Loading prices...")]),
            tline="", bline=""),
         urwid.Divider("─"),
         urwid.LineBox(
             urwid.Text([("text", "Loading focus...")]),
             tline="", bline="")])
else:
    body = urwid.Pile(
        [urwid.LineBox(
            urwid.Text([("text", "Loading prices...")]),
            tline="", bline="")])
footer = urwid.Pile([urwid.Divider("─"), urwid.Text(
    [("key", "R"),
     ("text", " Reload "),
     ("key", "◀ ▶ "),  # displays incorrectly without extra space
     ("text", " Toggle "),
     ("key", "C"),
     ("text", " Config "),
     ("key", "Q"),
     ("text", " Quit "),
     ("text", "│ "),
     ("key", sort_name()),
     ("text", " Sort "),
     ("key", str(focus_index + 1)),
     ("text", " Focus "),
     ("key", last_update),
     ("text", " Updated")])])

layout = urwid.Frame(header=header, body=ScrollBar(Scrollable(body)),
                     footer=footer, focus_part="body")
loop = urwid.MainLoop(
    layout, palette, unhandled_input=keystroke, handle_mouse=False)

if __name__ == "__main__":
    loop.set_alarm_in(0, refresh)
    loop.run()
