# Portfolio-Alerts
This program will pull current stock values from yfinance (Yahoo Finance) API, and send an SMS text message alert via Twilio API when the users invenstment portfolio moves by a certain percent threshold.

This program is designed to run on a Linux virtual server. Currently used in an Amazon AWS EC2 Linux Ubuntu.

The user can enter the stocks they own and their quantities in the tickers.json file. Every hour (time can also be assigned in the params.json file), the program will pull stock price data from yfinance API and determine if the users investment portfolio has moved by a certain percent threshold (also assigned in the params.json file). 

If the user's investment portfolio moves over the percent threshod, the program will send an SMS alert via Twilio API alerting the user of a movement in their portfolio.

Assign tickers and the amount of shares held in the tickers.json file. EX: "MSFT": 30, "AAPL": 40

Assign parameters in the params.json file. Params include username, running (boolean value to toggle program), sleep timer, percent threshold alert, sms enabling (boolean value), and Twilio SMS parameters.
