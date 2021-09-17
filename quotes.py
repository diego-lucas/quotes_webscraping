import requests
import pandas as pd
from bs4 import BeautifulSoup as soup


url = "https://quotes.toscrape.com/page/1/"

rows = []

while url != None:
    
    print("\n\nPAGE:", url)
    response = requests.get(url)
    content = soup(response.content, "lxml")

    quotes = content.find_all("div", class_="quote")

    for quote in quotes:

        quote_content = quote.find("span", class_="text").text.strip()
        autor = quote.find("small", class_="author").text.strip()
        tags_list = quote.find("div", class_="tags").find_all("a")
        tags_list = [tag.text.strip() for tag in tags_list]
        tags = ", ".join(tags_list)

        row = (
            quote_content, autor, tags
        )
        rows.append(row)
    
    # Check if have the button "next"
    next = content.find("ul", class_="pager").find("li", class_="next")
    if next:
        url = "https://quotes.toscrape.com" + next.find("a")["href"]
    else:
        url = None

columns = (
    "quote_content", "autor", "tags"
)
df = pd.DataFrame(rows, columns=columns)
print(df)
df.to_excel("quotes.xlsx", index=False)