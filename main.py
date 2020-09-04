import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from random import randint
import time

headers = {"Accept-Language": "en-US,en;q=0.5"}


def startScreenSelect():
    userOption = input("> ")
    if userOption.lower() == ("1"):
        top1000Movies()
    elif userOption.lower() == ("2"):
        top100Shows()
    elif userOption.lower() == ("3"):
        userHelp()
    elif userOption.lower() == ("4"):
        userQuit()
    else:
        print("Please choose one of the given options")
        print(sep="")
        time.sleep(0.8)
        titleScreen()


def titleScreen():
    print("================================")
    print("=         IMDB Scraper         =")
    print("================================")
    print("=      (1)Top 1000 Movies      =")
    print("=      (2)Top 100 Shows        =")
    print("=      (3)Help                 =")
    print("=      (4)Quit                 =")
    print("================================")
    startScreenSelect()


def top1000Movies():
    sortingOrder = ""
    userOptionSort = input("How would you like to sort them by?:"
                           "\n"
                           "(1) Movie Title "
                           " (2) Movie Year "
                           " (3) Length of Movie "
                           " (4) IMDB Rating "
                           " (5) MetaScore "
                           " (6) Genre "
                           " (7) No. of Votes "
                           " (8) Age Certificate "
                           "\n> ")


    if userOptionSort == ("1"):
        sortingOrder = "Movie"
        print("You have chosen to get the Top 1000 Movies on IMDB, sorted by Movie Title")
        '''
        ascendingOrder = input("In ascending order? (True/False): ")
        while ascendingOrder not in ["True", "False", "true", "false", "t", "f"]:
            ascendingOrderInput = input("Please choose either 'True' or 'False' ")
            if ascendingOrderInput == "True":
                ascendingOrder = True
            elif ascendingOrderInput == "False":
                ascendingOrder = False
            print(bool("Hello"))
            
            if ascendingOrder == "True":
                print("You have chosen to get the Top 1000 Movies on IMDB, sorted by Movie Title in ascending order")
            elif ascendingOrder == "False":
                print("You have chosen to get the Top 1000 Movies on IMDB, sorted by Movie Title in descending order")
        '''
    elif userOptionSort == ("2"):
        sortingOrder = "Year"
        print("You have chosen to get the Top 1000 Movies on IMDB, sorted by Movie Year")
    elif userOptionSort == ("3"):
        sortingOrder = "Genre"
        print("You have chosen to get the Top 1000 Movies on IMDB, sorted by Length of Movie")
    elif userOptionSort == ("4"):
        sortingOrder = "Rating"
        print("You have chosen to get the Top 1000 Movies on IMDB, sorted by IMDB Rating")
    elif userOptionSort == ("5"):
        sortingOrder = "metaScore"
        print("You have chosen to get the Top 1000 Movies on IMDB ,sorted by MetaScore")
    elif userOptionSort == ("6"):
        sortingOrder = "Votes"
        print("You have chosen to get the Top 1000 Movies on IMDB,sorted  by Genre")
    elif userOptionSort == ("7"):
        sortingOrder = "Length"
        print("You have chosen to get the Top 1000 Movies on IMDB, sorted by No. of Votes")
    elif userOptionSort == ("8"):
        sortingOrder = "Age Certificate"
        print("You have chosen to get the Top 1000 Movies on IMDB, sorted by Age Certificate")
    else:
        print("Please choose one of the given options")

    fileName = input("\nThis program will output the results to a file."
                      "\nPlease choose a name for this file: "
                      "\n")

    print("Please wait as your movies are collected...")
    print(sep="")

    titles = []
    years = []
    time = []
    imdb_ratings = []
    metascores = []
    genres = []
    votes = []
    certificates = []

    pages = np.arange(1, 1001, 50)
    pd.set_option(
        "display.max_columns", None,
        # 'display.max_rows', None
    )

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

            m_score = container.find('span', class_='metascore').text if container.find('span',
                                                                                        class_='metascore') else ''
            metascores.append(m_score)

            genre = container.p.find('span', class_='genre').text.strip() if container.p.find('span',
                                                                                              class_='genre') else ''
            genres.append(genre)

            certificate = container.p.find('span', class_='certificate').text if container.p.find('span',
                                                                                                  class_='certificate') else ''
            certificates.append(certificate)

            nv = container.find_all('span', attrs={'name': 'nv'})

            vote = nv[0].text
            votes.append(vote)

    movies = pd.DataFrame({
        'Movie': titles,
        'Year': years,
        'Genre': genres,
        'Rating': imdb_ratings,
        'metaScore': metascores,
        'Votes': votes,
        'Length': time,
        'Age Certificate': certificates
    })

    movies.loc[:, 'Year'] = movies['Year'].str[-5:-1].astype(int)

    movies['Length'] = movies['Length'].astype(str)
    movies['Length'] = movies['Length'].str.extract('(\d+)').astype(int)

    movies['Genre'] = movies['Genre'].astype(str)
    movies['Genre'] = movies['Genre']

    movies['Age Certificate'] = movies['Age Certificate'].astype(str)
    movies['Age Certificate'] = movies['Age Certificate']

    movies['metaScore'] = movies['metaScore'].str.extract('(\d+)')
    movies['metaScore'] = pd.to_numeric(movies['metaScore'], errors='coerce')

    movies['Votes'] = movies['Votes'].str.replace(',', '').astype(int)

    # to see your dataframe
    print(sep="")
    print(movies.sort_values(by=[sortingOrder]))

    # to see the datatypes of your columns
    # print(movies.dtypes)

    # to see where you're missing data and how much data is missing
    # print(movies.isnull().sum())

    # to move all your scraped data to a CSV file
    movies.to_csv(fileName + '.csv')
    print("Items have been collected and written to " + fileName + ".csv")
    print(sep="")
    titleScreen()


def top100Shows():
    
    titles = []
    years = []
    time = []
    imdb_ratings = []
    genres = []
    votes = []
    certificates = []
    
    movies = pd.DataFrame({
        'Movie': titles,
        'Year': years,
        'Length': time,
        'Rating': imdb_ratings,
        'Genre': genres,
        'Votes': votes,
        'Age Certificate': certificates
    })
    
    print("Work in progress, come back soon...")
    print(sep="")
    titleScreen()


def userHelp():
    print("\n")
    print("============================================================")
    print("=                          Help                            =")
    print("============================================================")
    print("- Using the options provided to you on the title screen")
    print("- Choose what list of movies or shows you would like to view")
    print("- The results will then be exported to an excel sheet ")
    print("- Happy viewing!")
    print("============================================================")
    time.sleep(3)
    print(sep="")
    titleScreen()

def userQuit():
    reply = str(input("Are you sure you want to quit?" + ' (Y/N): ')).lower().strip()
    if reply == 'y':
        return True
    elif reply == 'n':
        print(sep="")
        titleScreen()
    else:
        print("Please choose a valid option: ")
        userQuit()



titleScreen()
