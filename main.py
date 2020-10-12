import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from random import randint
import time
import json

headers = {"Accept-Language": "en-US,en;q=0.5"}


def start_screen_select():
    user_option = input("> ")
    if user_option.lower() == "1":
        top1000_movies()
    elif user_option.lower() == "2":
        user_help()
    elif user_option.lower() == "3":
        user_quit()
    else:
        print("Please choose one of the given options")
        print(sep="")
        time.sleep(0.8)
        title_screen()


def title_screen():
    print("================================")
    print("=         IMDB Scraper         =")
    print("================================")
    print("=      (1)Top 1000 Movies      =")
    print("=      (2)Help                 =")
    print("=      (3)Quit                 =")
    print("================================")
    start_screen_select()


def top1000_movies():
    sorting_order = ""
    user_option_sort = input("How would you like to sort them by?:"
                             "\n"
                             "(1) Movie Title "
                             " (2) Movie Year "
                             " (3) Genre  "
                             " (4) IMDB Rating "
                             " (5) MetaScore "
                             " (6) No. of Votes "
                             " (7) Length of Movie "
                             " (8) Age Certificate "
                             "\n> ")

    if user_option_sort == "1":
        sorting_order = "Movie"
        print("You have chosen to get the Top 1000 Movies on IMDB, sorted by Movie Title")
    elif user_option_sort == "2":
        sorting_order = "Year"
        print("You have chosen to get the Top 1000 Movies on IMDB, sorted by Movie Year")
    elif user_option_sort == "3":
        sorting_order = "Genre"
        print("You have chosen to get the Top 1000 Movies on IMDB, sorted by Length of Movie")
    elif user_option_sort == "4":
        sorting_order = "Rating"
        print("You have chosen to get the Top 1000 Movies on IMDB, sorted by IMDB Rating")
    elif user_option_sort == "5":
        sorting_order = "metaScore"
        print("You have chosen to get the Top 1000 Movies on IMDB ,sorted by MetaScore")
    elif user_option_sort == "6":
        sorting_order = "Votes"
        print("You have chosen to get the Top 1000 Movies on IMDB,sorted  by Genre")
    elif user_option_sort == "7":
        sorting_order = "Length"
        print("You have chosen to get the Top 1000 Movies on IMDB, sorted by No. of Votes")
    elif user_option_sort == "8":
        sorting_order = "Age Certificate"
        print("You have chosen to get the Top 1000 Movies on IMDB, sorted by Age Certificate")
    else:
        print("Please choose one of the given options")

    file_name = input("\nThis program will output the results to a file."
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

            genre = container.p.find('span', class_='genre').text.strip() \
                if container.p.find('span', class_='genre') else ''
            genres.append(genre)

            certificate = container.p.find('span', class_='certificate').text \
                if container.p.find('span', class_='certificate') else ''
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

    # prints results in the form of JSON

    # df = pd.DataFrame(movies)
    # print(df.to_json(orient="records", indent=4))

    print(sep="")
    output = movies.sort_values(by=[sorting_order])
    print(output)

    output.to_csv(file_name + '.csv')
    print("Items have been collected and written to " + file_name + ".csv")
    print(sep="")
    title_screen()


def user_help():
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
    title_screen()


def user_quit():
    reply = str(input("Are you sure you want to quit?" + ' (Y/N): ')).lower().strip()
    if reply == 'y':
        return True
    elif reply == 'n':
        print(sep="")
        title_screen()
    else:
        print("Please choose a valid option: ")
        user_quit()


title_screen()
