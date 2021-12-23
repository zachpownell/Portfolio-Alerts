# Portfolio-Alerts
This program will pull current stock values from yfinance (Yahoo Finance) API, and send an SMS text message alert when the users invenstment portfolio moves by a certain percent threshod.

This program is meant to run on an Amazon AWS EC2 instance.

The user can enter the stocks they own, as well as how many shares, in the tickers.json file. Every iteration (assigned in the params.json file), the program will pull stock price data from yfinance and determine if the users portfolio has moved a certain percent threshold (also assigned in the params.json file). 

If the user's investment portfolio moves over the percent threshod, the program will send an SMS alert via Twilio alerting the user of portfolio movement.

Assign your tickers and the amount of shares held in the tickers.json file. EX: "MSFT": 30, "AAPL": 40

Assign your parameters in the params.json. The user can enter a username, running (boolean value to toggle program), sleep timer, percent threshold alert, sms enabling (boolean value), and Twilio SMS parameters.
