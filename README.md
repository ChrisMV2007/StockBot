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
Below is a user manual; note that some aspects of the program are explained within itself, so the only things included are inputs that require some technical knowledge or the format for which are not explicitly stated in the program.

### Login / Signup
The login interface is self explanitory; input "log in" to log in, "sign up" to create a new profile. When signing up, entering a user that does not exist will automatically create that profile.

### Default Settings
These are the default chart/watchlist settings upon cretaing a new account.
watchlist: AAPL,MSFT,TSLA. Def

### Settings
The settings menu is used to change default chart settings and your watchlist. Most of the menu is navigable via the options and input guides, but some potenntially unspecific aspects of the input are listed here.
- "indicators" allows you to select the indicators that show when launching a chart.
- Indicator settings require knowledge of the indicator you are changing the setting for; make sure that you know what each value means and how the indicator works before changing it's settings.
- Stochastic RSI has 2 colors (1 for the k line and 1 for the d line); it takes 2 colors but asks for them in separate input lines.
- Stock history allows you to change the length or the interval; the interval is how long is in between each candle/line point (ex: 1d, 90m, etc.) and the length is how many intervals into the past the chart displays (ex: interval = 2d & length = 30 means that the chart will display a stock's history 60 days into the past with each) candle/line point being 2 days apart.
- Moving average location changes whether moving averages (ema/sma) are displayed seperate or with the stock prices history when the chart is launched.
- Watchlist is input as all caps tickers with commas in between each ticker (ex: MSFT,AAPL,GOOG).
- For "indicator colors", colors are entered as hex values; a hashtag followed by 6 digits (ex: #239001).

### Chart and Manual Chart
Chart displays charts based on default chart settings (see settings to change default chart settings). Manual chart opens the settings interface and allows you to make chart customizations to your chart without having to change your settings. For both manual and auto chart you are given the option to launch charts for either a particular stock or every stock in your watchlist. 

### Indicator Analysis
Indicator analysis allows you to screen a stock or filter your watchlist based on indicator-based conditionals. The following are instructions on how to input bounds/conditionals for each indicator (help is also given within the program). Note that the next segment assumes that you have some understanding of how the indicators themselves work.
- EMA and SMA: Both EMA and SMA both take the same inputs. First input whether you would like to set 2 conditionals (a greater than as well as a less than conditional) or just 1 (a greater than or a less than conditional). Input your conditionals as a comparison operator followed by a number; the number represents how far above or below the price of the stock the EMA/SMA is as a percentage of the price of the stock (ex: >10 means that you want the EMA to be more than 10% greater than the price of the stock). Percentages were used to make the system universal across differently priced stocks.
- RSI: Input a comparison operator followed by a number (ex: >70 or <30).
- Stochastic RSI: First input whether you would like to use the k line, d line, or both (reminder that the k line is more sensitive than the d line). For whichever line you choose (or bth), input a comparison operator followed by a number (ex: >80 or <20). 
- Both indicators have extreme and normal ranges (that will be shown in chart as well as on any screener that displays RSI or Stochastic RSI). For RSI, the normal range is 30-70 and the extreme ranges are 30- and 70+. For Stochastic RSI, the normal range is 20-80 and the extreme ranges are 20- and 80+. 
- As a general rule, RSI and Stochastic RSI values almost never exceed 100 or drop below 0.
- To use multiple indicators as conditionals, simply input the ones you would like to use with commas separating them.

### Trend Analysis
Trend analysis uses a sampling algorithm to estimate the trend of a stock as well as filter your watchlist using the trend algorithm. The following explains each input.
- This excerpt from earlier in the readme applies to the first 2 inputs on intervals and time id (essentially asking what time frame you would like to analyze the trend for): <Stock history allows you to change the length or the interval; the interval is how long is in between each candle/line point (ex: 1d, 90m, etc.) and the length is how many intervals into the past the chart displays (ex: interval = 2d & length = 30 means that the chart will display a stock's history 60 days into the past with each) candle/line point being 2 days apart>
- The program uses price samples at an interval (defined above) and averages the price over the previous x intervals from each interval. Define x as the averaging length (ex: averaging length = 10 means that each interval is averaged over the past 10 intervals).
- The step simply tells the program to take every x interval (ex: length = 30 & interval = 1d & step = 3 means 10 intervals, 3 days apart).

## Note on Modification
Quick note if you want to modify the program for your own use or import files from the program for use in your own project: all files that includes import statements are routed from the main.py file, so before importing, you should check import statements and modify them to suit your purposes.
