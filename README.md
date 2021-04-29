# stonktrack
![GitHub release (latest by date)](https://img.shields.io/github/v/release/slightlyskepticalpotat/stonktrack?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/stonktrack?style=flat-square)
![GitHub](https://img.shields.io/github/license/slightlyskepticalpotat/stonktrack?style=flat-square)
![Python Version](https://img.shields.io/badge/python-%3E%3D%203.6-blue?style=flat-square)

Stonktrack is a terminal utility that can track stocks, cryptocurrencies, forexes, and more. Built with Python and urwid, it's different from other terminal finance trackers in that it can track a variety of assets, fetches  non-delayed real-time data, and does not require an API key. Stocktrack can also automatically convert prices into your local currency.

## Getting Started

### Installing and Running
This program can be installed in two different ways. You can install it directly with pip (recommended), or clone the repository and run the code yourself. Either way, you will need Python 3.6 or higher to run the code.

#### Using Pip
```
$ pip3 install stonktrack
$ nano config.yml
$ python3 -m stonktrack
```

#### Manually
```
$ git clone https://github.com/slightlyskepticalpotat/stonktrack.git
$ cd stonktrack
$ pip3 install -r requirements.txt
$ nano config.yml
$ python3 stonktrack.py
```

### Usage
Stonktrack is configured through a single configuration file named `config.yml`. Configuration options are explained in [CONFIG.md](https://github.com/slightlyskepticalpotat/stonktrack/blob/main/CONFIG.md), and a sample configuration file is provided in [config.yml](https://github.com/slightlyskepticalpotat/stonktrack/blob/main/config.yml).

## Screenshots
More screenshots of various options are available in [/screenshots](https://github.com/slightlyskepticalpotat/stonktrack/blob/main/screenshots).

![stonktrack](https://github.com/slightlyskepticalpotat/stonktrack/blob/main/screenshots/stonktrack.png)
> Normal stonktrack, with colour and a scrollbar

---

![stonktrack-bw](https://github.com/slightlyskepticalpotat/stonktrack/blob/main/screenshots/stonktrack-bw.png)
> Monochrome mode is less distracting for some

---

![stonktrack-focus](https://github.com/slightlyskepticalpotat/stonktrack/blob/main/screenshots/stonktrack-focus.png)
> The focus tab displays in-depth stats

---

![stonktrack-phone](https://github.com/slightlyskepticalpotat/stonktrack/blob/main/screenshots/stonktrack-phone.png)
> Stonktrack works on mobile (Android + Termux)

## Contributing
Bug reports, forks, and pull requests are all welcome. Feel free to open an issue!

## Licence
This project is licensed under the GNU Affero General Public License v3.0, and makes use of other open-source libraries. For more information, please refer to our [LICENSE](https://github.com/slightlyskepticalpotat/stonktrack/blob/main/LICENSE).
