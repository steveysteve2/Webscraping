# pip install requests (to be able to get HTML pages and load them into Python)
# pip install bs4 (for beautifulsoup - python tool to parse HTML)


from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


##############FOR MACS THAT HAVE ERRORS LOOK HERE################
#https://timonweb.com/tutorials/fixing-certificate_verify_failed-error-when-trying-requests_html-out-on-mac/

############## ALTERNATIVELY IF PASSWORD IS AN ISSUE FOR MAC USERS ########################
##  > cd "/Applications/Python 3.6/"
##  > sudo "./Install Certificates.command"


url = 'https://www.worldometers.info/coronavirus/country/us'
# Request in case 404 Forbidden error
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers=headers)

webpage = urlopen(req).read()

soup = BeautifulSoup(webpage, 'html.parser')

print(soup.title.text)

table_rows = soup.findAll("tr")

state_death_ratio = ""
state_best_testing = ""
state_worst_testing = ""
high_death_ratio = 0.0
high_test_ratio = 0.0
low_test_ratio = 100.0

# print(table_rows[:2])

for row in table_rows[2:53]:
    td = row.findAll("td")
    state = td[1].text
    print(state)
    tcases = int((td[2].text).replace(",",""))
    print(f"Total Cases: {tcases}")
    tdeaths = int((td[4].text).replace(",",""))
    print(f"Total Deaths: {tdeaths}")
    ttested = int((td[10].text).replace(",",""))
    print(f"Total Tested: {ttested}")
    pop = int((td[12].text).replace(",",""))
    print(f"Total Population: {pop}")
    dratio = tdeaths/tcases
    print(f"Death Ratio: {dratio:.2%}")
    tratio = ttested/pop
    print(f"Test Ratio: {tratio:.2%}")

    if dratio > high_death_ratio:
        high_death_ratio = dratio
        state_death_ratio = state

    if tratio > high_test_ratio:
        high_test_ratio = tratio
        state_worst_testing = state

    if tratio < low_test_ratio:
        low_test_ratio = tratio
        state_best_testing = state

    input()

print(f"State with best testing: {state_best_testing}")
print(f"Test Ratio: {high_test_ratio:.2%}")
print(f"\nState with worst testing: {state_worst_testing}")
print(f"Test Ratio: {low_test_ratio:.2%}")
print(f"\nState with highest death ratio: {state_death_ratio}")
print(f"Death Ratio: {high_death_ratio:.2%}")


#SOME USEFUL FUNCTIONS IN BEAUTIFULSOUP
#-----------------------------------------------#
# find(tag, attributes, recursive, text, keywords)
# findAll(tag, attributes, recursive, text, limit, keywords)

#Tags: find("h1","h2","h3", etc.)
#Attributes: find("span", {"class":{"green","red"}})
#Text: nameList = Objfind(text="the prince")
#Limit = find with limit of 1
#keyword: allText = Obj.find(id="title",class="text")