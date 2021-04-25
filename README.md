# stonktrack
![GitHub release (latest by date)](https://img.shields.io/github/v/release/slightlyskepticalpotat/stonktrack?style=flat-square)
![GitHub](https://img.shields.io/github/license/slightlyskepticalpotat/stonktrack?style=flat-square)
![Python Version](https://img.shields.io/badge/python-%3E%3D%203.8-blue?style=flat-square)

Stonktrack is a terminal utility that can track stocks, cryptocurrencies, forexes, and more. Built with Python and urwid, it's different from other terminal finance trackers in that it can track a variety of assets, fetches  non-delayed real-time data, and does not require an API key. Stocktrack can also automatically convert prices into your local currency.

## Getting Started

### Installing and Running
This program can be installed in two different ways. You can install it directly with pip (recommended), or clone the repository and run the code yourself. Either way, you will need Python 3.8 or higher to run the code.

Once you have installed the program with pip or cloned the repository, there are two versions of the program to choose from. `stonktrack` is the official supported version with colour and no scrolling, and `stonktrack-scroll` is the non-supported monochrome version with scrolling. `stonktrack` is recommend.

#### Using Pip
```
$ pip3 install stonktrack
$ nano config.yml
$ python3 -m stonktrack
$ python3 -m stonktrack-scroll
```

#### Manually
```
$ git clone https://github.com/slightlyskepticalpotat/stonktrack.git
$ cd stonktrack
$ pip3 install -r requirements.txt
$ nano config.yml
$ python3 stonktrack.py
$ python3 stonktrack-scroll.py
```

### Usage
Stonktrack is configured through a single configuration file named `config.yml`. Configuration options are explained in [CONFIG.md](CONFIG.md), and a sample configuration file is provided in [config.yml](config.yml).

## Screenshots
![stonktrack](screenshots/stonktrack.png)
> Normal stonktrack, with colour but no scrolling

---

![stonktrack-scroll](screenshots/stonktrack-scroll.png)
> Stonktrack-scroll, in monochrome but with scrolling

---

![stonktrack-phone](screenshots/stonktrack-phone.png)
> Stonktrack even works on mobile with Termux

## Contributing
Bug reports, forks, and pull requests are all welcome. Feel free to open an issue!

## Licence
This project is licensed under the GNU Affero General Public License v3.0. For more information, please refer to [LICENSE.md](LICENSE.md).
