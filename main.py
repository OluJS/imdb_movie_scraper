import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from random import randint



headers = {"Accept-Language": "en-US,en;q=0.5"}

titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
certificates = []

pages = np.arange(1, 1001, 50)
# pd.set_option("display.max_rows", None, "display.max_columns", None)


for page in pages:

    page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&sort=alpha,asc&start="
                        + str(page) + "&ref_=adv_nxt",
                        headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')
    movie_div = soup.find_all('div', class_='lister-item mode-advanced')

    sleep(randint(2, 10))

    for container in movie_div:
        name = container.h3.a.text
        titles.append(name)

        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)

        runtime = container.p.find('span', class_='runtime') if container.p.find('span', class_='runtime') else ''
        time.append(runtime)

        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else ''
        metascores.append(m_score)

        certificate = container.find('span', {'class':'certificate'})
        certificates.append(certificate)

        nv = container.find_all('span', attrs={'name': 'nv'})

        vote = nv[0].text
        votes.append(vote)


movies = pd.DataFrame({
    'Movie': titles,
    'Year': years,
    'Rating': imdb_ratings,
    'metaScore': metascores,
    'Votes': votes,
    'Length': time
   # 'Age Certificate': certificates
})

movies.loc[:, 'Year'] = movies['Year'].str[-5:-1].astype(int)

movies['Length'] = movies['Length'].astype(str)
movies['Length'] = movies['Length'].str.extract('(\d+)').astype(int)

movies['metaScore'] = movies['metaScore'].str.extract('(\d+)')
movies['metaScore'] = pd.to_numeric(movies['metaScore'], errors='coerce')

# to see your dataframe
print(movies)

# to see the datatypes of your columns
# print(movies.dtypes)

# to see where you're missing data and how much data is missing
print(movies.isnull().sum())

# to move all your scraped data to a CSV file
# movies.to_csv('movies.csv')