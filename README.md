# StockBot

<hr />

## A Python/Terminal Based Interface to Display Graphs and Screen Stocks Based on Indicators or Trend

This program was built with the yfinance module was created with the intent of expediting the stock screening process for those who have formulaic stock strategies and would like to automate their daily market check, as well as serve as a final project before I begin my studies in front-end development.

<hr />

## FEATURES
- Create different profiles and save settings/watchlists on each profile
- Launch charts with customizable indicators and aesthetic properties
- Filter stocks based on indicator-based conditions
- Screen stocks based on a customizable trend algorithm
- Extensive error prevention and input verification

<hr />

## HOW TO INSTALL AND RUN
In short, clone the repository onto your device using git bash (or another git application with similar capabilities) and install the dependencies below. Note that this was written from the perspective of a windows user (but the instructions will likely still be useful given you replace any windows specific instructions).
1. Clone the Repository (Skip if you already have a way to clone the repository)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;1.1 Go to the Git downloads website and click https://git-scm.com/downloads "Download for Windows"<br/>
&nbsp;&nbsp;&nbsp;&nbsp;1.2 Once the installation file downloads, open it and follow the setup process (with the recommended settings unless you wish otherwise)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;1.3 When the git files download, open GIT GUI and click 'Clone Existing Repository'<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.1 In "Souce Location", paste this link: https://github.com/ChrisMV2007/StockBot.git <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.2 In "Target Directory", locate where you want the program files to reside.<br/>
2. Install the Dependencies (skip files that are already on your computer)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;2.1 Install python https://www.python.org/downloads/<br/>
&nbsp;&nbsp;&nbsp;&nbsp;2.2 Pip should install along with python. In the command prompt, run the following commands:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.2.1 pip install matplotlib<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.2.2 pip install pandas<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.2.3 pip install datetime<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.2.4 pip install yfinance<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.2.5 pip install mplfinance<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.2.6 pip install functools<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.2.7 pip install csv<br/>
3. Run the Program<br/>
&nbsp;&nbsp;&nbsp;&nbsp;3.1 Go to the directory that you stored the files in<br/>
&nbsp;&nbsp;&nbsp;&nbsp;3.2 Pray<br/>
&nbsp;&nbsp;&nbsp;&nbsp;3.3 Open the main.py file with Python<br/>

<hr />

## INPUT GUIDE / USER MANUAL

### Login / Signup
The login interface is self explanitory; input "log in" to log in, "sign up" to create a new profile. When signing up, entering a user that does not exist will automatically create that profile.

### Settings
The settings menu is used to change default chart settings and your watchlist. Most of the menu is navigable via the options and input guides, but some potenntially unspecific aspects of the input are listed here.
- "indicators" allows you to select the indicators that show when launching a chart
- Indicator settings require knowledge of the indicator you are changing the setting for; make sure that you know what each value means and how the indicator works before changing it's settings
- Stochastic RSI has 2 colors (1 for the k line and 1 for the d line); it takes 2 colors but asks for them in separate input lines
- Stock history allows you to change the length or the interval; the interval is how long is in between each candle/line point (ex: 1d, 90m, etc.) and the length is how many intervals into the past the chart displays (ex: interval = 2d & length = 30 means that the chart will display a stock's history 60 days into the past with each) candle/line point being 2 days apart.
- Moving average location changes whether moving averages (ema/sma) are displayed seperate or with the stock prices history when the chart is launched
- Watchlist is input as all caps tickers with commas in between each ticker (ex: MSFT,AAPL,GOOG)
- For "indicator colors", colors are entered as hex values; a hashtag followed by 6 digits (ex: #239001)

### Chart and Manual Chart
Chart displays charts based on default chart settings (see settings to change default chart settings). Manual chart opens the settings interface and allows you to make chart customizations to your chart without having to change your settings. For both manual and auto chart you are given the option to launch charts for either a particular stock or every stock in your watchlist. 

### 

