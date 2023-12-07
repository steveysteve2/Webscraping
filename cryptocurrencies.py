from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from twilio.rest import Client
import keys

url = 'https://www.coingecko.com/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
req = Request(url, headers=headers)
page = urlopen(req).read()			
soup = BeautifulSoup(page, 'html.parser')

#Twilio texting code
client = Client(keys.accountsid, keys.authToken)
TwilioNumber = '+18337712336'
myCell = '+15129217887'
msg = 'Ethereum over $2,000. Sell now!'

print(soup.title.text)
table = soup.find("table")
coins = table.findAll("tr")

for c in range(1,6):
    name = coins[c].find("div", class_="tw-text-gray-700 dark:tw-text-moon-100 tw-font-semibold tw-text-sm tw-leading-5").text.rstrip("\n")
    print(f"\n{name}")
    price = float(coins[c].find("span",class_="").text.replace(",","").replace("$","").replace("\n",""))
    print(f"${price:.2f}")
    #checks if change goes up or down
    ratechange = coins[c].findAll('td')
    if ratechange[6].find("span", class_="gecko-up"):
        change = float(ratechange[6].find("span", class_="gecko-up").text.replace("%",""))
        print(f"+{change}%")
        newprice = price*(1+(change/100))
    else:
        change = float(ratechange[6].find("span", class_="gecko-down").text.replace("%",""))
        print(f"-{change}%")
        newprice = price*(1-(change/100))

    print(f"${newprice:.2f}")
    #check if Ethereum is over $2,000:
    if "Ethereum" in name and newprice > 2000:
        txtmsg = client.messages.create(to=myCell, from_=TwilioNumber, body=msg)
        print(f"Message Status: {txtmsg.status}")
        print(msg)
    
    input()