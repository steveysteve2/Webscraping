import plotly.express as px      #use "pip3 install pandas" for plotly usage
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

avg_quotes = 0.0
longest_quote = ""
lquoteauth = ""
shortest_quote = "This is a test quote for shortest quote. Hopefully, some quotes are shorter!"
squoteauth = ""
quote_list = []
quotewordscount = 0
tag_dict = {}
auth_dict = {}
count = 1

for page in range(1,11):
    url = 'https://quotes.toscrape.com/page/' + str(page) + '/'
    # Request in case 404 Forbidden error
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url, headers=headers)
    page = urlopen(req).read()			
    soup = BeautifulSoup(page, 'html.parser')
    print(f"Page {count} of " + str(soup.title.text) + " loaded")
    count += 1

    quotes = soup.findAll("div", class_="quote")

    for q in quotes:
        quote = q.find("span",class_="text").text
        quote_list.append(quote)
    #Author Analysis
        auth = q.find("small",class_="author").text
        if auth in auth_dict:
            auth_dict[auth] += 1
        else:
            auth_dict[auth] = 1
    #Quote Analysis
        quotewords = quote.split()
        if len(quotewords) > len(longest_quote):
            longest_quote = quote
            lquoteauth = auth

        if len(quotewords) < len(shortest_quote):
            shortest_quote = quote
            squoteauth = auth

        quotewordscount += len(quotewords)
    #Tag Analysis
        tags = q.findAll("a",class_="tag")
        for t in tags:
            tag = t.text
            if tag in tag_dict:
                tag_dict[tag] += 1
            else:
                tag_dict[tag] = 1


#Visualization
#Top Ten Authors based on number of quotes:
sorted_authors = sorted(auth_dict.items(), key=lambda x:x[1], reverse=True)
sorted_dict = dict(sorted_authors)

auths = list(sorted_dict.keys())
toptenauths = auths[:10]
vals = list(sorted_dict.values())
toptenvals = vals[:10]

fig = px.bar(x=toptenauths, y=toptenvals, 
             labels={"x":"Author", "y":"No. of quotes"}, 
             title="Top Ten Authors by Number of Quotes")

fig.show()
#Top ten tags based on frequency used:
taglist = sorted(tag_dict.items(), key=lambda x:x[1], reverse=True)
sorted_tags = dict(taglist)

tags = list(sorted_tags.keys())
toptentags = tags[:10]
freq = list(sorted_tags.values())
toptenfreq = freq[:10]

fig = px.bar(x=toptentags, y=toptenfreq, 
             labels={"x":"Tag", "y":"No. of times used"}, 
             title="Top Ten Tags by Popularity")

fig.show()

totalquotes = len(quote_list)
avg_quotes = quotewordscount/totalquotes
print(f"\nQuotes by author: {sorted_dict}")
print(f"\nAuthor with most quotes: {max(auth_dict, key=auth_dict.get)}")
print(f"\nAuthor with least quotes: {min(auth_dict, key=auth_dict.get)}")
print(f"\nAverage quote length: {avg_quotes} words per quote")
print(f"\nLongest Quote ({len(longest_quote.split())} words): {longest_quote} - {lquoteauth}")
print(f"\nShortest Quote ({len(shortest_quote.split())} words): {shortest_quote} - {squoteauth}")
print(f"\nMost Popular Tag: {max(tag_dict, key=tag_dict.get)} ({max(tag_dict.values())} times)")
print(f"\nTotal tags: {len(tag_dict)}")