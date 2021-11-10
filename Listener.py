import json
import time
import twilio
import yfinance as yf
from twilio.rest import Client
from os.path import exists

########################################################################################################################

# Name: Zach
# Todo: exception handling in reading from params file
# Todo: toggler for running in params

########################################################################################################################

# File initiation.
PARAMS_FILE = "params.json"
TICKERS_FILE = "tickers.json"

# Param dictionary initiation. If a param file does not exist, it will load in these default parameters.
params = {
    "user_name": "DEFAULT_USERNAME",
    "running": True,
    "sleep_timer": 5,
    "alert_percent_threshold": 5,
    "send_sms": True,
    "to_phone_number": "",
    "from_phone_number": "",
    "twilio_account_sid": "",
    "twilio_auth_token": ""
}

# Tickers dictionary. Will load in from tickers json file.
tickers = {}

# Portfolio values from previous and current iterations.
previous_portfolio_value = 1
current_portfolio_value = 2


# Method to load dictionaries from json file into program.
def load_file(file, dictionary):

    # Check if our json file actually exists. If it does not exist, create a new file with default parameters.
    if not exists(file):
        print("ALERT: File " + file + " does not exist. Creating...")
        with open(file, "w") as f:
            json.dump(dictionary, f)
    with open(file) as f:
        return json.load(f)


# Method to send a text message from the Twilio account to the phone number.
def send_sms(sms_message):

    try:
        client = Client(params["twilio_account_sid"], params["twilio_auth_token"])

        message = client.messages.create(
            to=params["to_phone_number"],
            from_=params["from_phone_number"],
            body=sms_message
        )

        print("SMS sent to phone number on file.")

    except Exception:

        print("ERROR: Invalid credentials for Twilio SMS messaging. Please check params file and try again.")


# As long as running = True in our param files, continue looping
while params["running"]:

    print("Loading parameters from files...")

    # Lets make sure the param and ticker files are readable.
    try:
        params = load_file(PARAMS_FILE, params)
        tickers = load_file(TICKERS_FILE, tickers)
    except json.decoder.JSONDecodeError:
        print("FATAL: Incorrect formatted json files. Please delete old json files and try again. Terminating.")
        break

    previous_portfolio_value = current_portfolio_value
    current_portfolio_value = 0

    # Lets make sure our params file looks good.
    if not {"user_name", "running", "sleep_timer", "alert_percent_threshold"} <= params.keys():
        print("FATAL: Missing keys in params file. Please delete old params file and try again. Terminating.")
        break

    # Our params file looks good. Now lets make sure our sleep timer is in range.
    if not params["sleep_timer"] in range(1, 7201):
        print("FATAL: Sleep timer is not in range in params file. Please set to a number between 60-1440. Terminating.")
        break

    print("Initiating ticker search for user " + params['user_name'] + ".")

    # Iterate through each ticker found in the tickers file. If no valid tickers are found, terminate.
    ticker_found = False
    for ticker in tickers:

        print("Searching ticker " + ticker + "...")
        ticker_value = yf.Ticker(ticker).info['regularMarketPrice']

        if ticker_value is not None:
            print("Ticker " + ticker + " found.")
            ticker_found = True
            current_portfolio_value += (ticker_value * tickers[ticker])
            print("Owns " + str(tickers[ticker]) + " " + ticker + ".")
        else:
            print("ERROR: Ticker " + ticker + " not found.")

    print("Total portfolio value for user " + params["user_name"] + ": $" + str(current_portfolio_value))

    # If no valid tickers were found, lets terminate the program.
    if not ticker_found:
        print("No valid tickers from tickers file found. Terminating.")
        break

    # Assign percent change from previous portfolio value to current value. Movement to up, down, or even.
    percent_change = ((float(current_portfolio_value) - previous_portfolio_value) / previous_portfolio_value) * 100
    movement = "up" if percent_change > 0 else "down" if percent_change < 0 else "even"

    print("Portfolio is " + movement + " by " + str(abs(percent_change)) + "%.")

    # Now lets check if our portfolio moved enough to trigger an alert.
    if percent_change > params["alert_percent_threshold"]:

        print("ALERT: Portfolio movement " + movement + " by " + str(abs(percent_change)) + "%.")

        # Lets check to see if SMS alerts are enabled.
        if params["send_sms"]:
            send_sms("ALERT: Portfolio movement " + movement + " by " + str(abs(percent_change)) + "%.")

    # Sleep the program for the duration of the timer.
    print("Sleeping for " + str(params["sleep_timer"]) + " seconds...")

    time.sleep(params["sleep_timer"])

print("Terminated.")
