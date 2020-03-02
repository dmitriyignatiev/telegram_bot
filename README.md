# telegram_bot
simple bot for telegram

main commands:
1.	/list or /lst - returns list of all available rates from: https://api.exchangeratesapi.io/latest?base=USD. 

2. exchange $10 to CAD or  /exchange 10 USD to CAD 
- converts to the second currency with two decimal precision and return.
Ex.:  $15.55

3.	/history USD/CAD for 7 days 
- return an image graph chart which shows the exchange rate graph/chart of the selected currency for the last 7 days.

0. run telegram /new_bot => recieve API => paste to app_test.py on line #16 istaead of API_TOKEN(bot = telebot.TeleBot(API_TOKEN))
00. find your socks5 proxy => paste you roxy server on app_test.py on line #18 (apihelper.proxy = {'https':'socks5h://<your socks5 proxy>'})
1. clone or download
2. create venv and install all dependencies
3. pip install pyTelegramBotAPI
4. pip install pandas
5. pip install mysql.connector
6. pip install sqlalchemy
7. pip install requests[SOCKS]
8. build docker-compose up for mysql db
9. run python app_test.py
10. enjoy
