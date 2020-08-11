"""
Olga Andreeva
Section AA
Scrapes IMDB to get information about the actors in Twilight.
The information is how many projects they've been in since Twilight
and the most profitable project (excluding the Twilight saga)
"""

import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

# Movies to exclude from calculations.
twilight_movies = ["The Twilight Saga: Breaking Dawn - Part 2",
                   "The Twilight Saga: Breaking Dawn - Part 1",
                   "The Twilight Saga: Eclipse", "The Twilight Saga: New Moon"]
# We only want to look at the first 33 actors on the page because
# after that, it becomes extras
num_actors = 33
# The characters within the first 33 who aren't given names
# (and should be removed before analysis)
non_named_characters = ["High School Administrator", "Mine Security Guard",
                        "Jacob's Friend", "Frat Boy", "Waitress"]


def get_box_office(link):
    """
    Given a movie/tv show link, returns the cumulative worldwide gross
    of that movie/tv show as an int. If it is not found on the page, returns 0.
    """
    page = requests.get('https://www.imdb.com' + link)
    page_content = BeautifulSoup(page.content, 'html.parser')
    gross = page_content.find('h4', string='Cumulative Worldwide Gross:')
    if (gross is not None):
        return int(gross.parent.get_text()[30:].replace(',', ''))
    return 0


def get_films(actor):
    """
    Given an actor's IMDB HTML content, finds all of the projects that
    they acted in and returns it in an array.
    """
    selection = '#filmo-head-actress + .filmo-category-section .filmo-row'
    films = [s for s in actor.select(selection)]
    if (not films):
        selection = '#filmo-head-actor + .filmo-category-section .filmo-row'
        films = [s for s in actor.select(selection)]
    return films


def collect_data(twilight):
    """
    Given the Twilight IMDB page HTML content, collects all the actors'
    IMDB pages to query. Returns a DataFrame of the number of projects
    they've been in, their highest grossing movie (excluding the Twilight
    saga), and the highest grossing movie box office numbers.
    """
    cast_links = [page.get('href') for page
                  in twilight.select('.article .cast_list .primary_photo a')]

    actors_names = []
    number_projects = []
    highest_grossing_movies = []
    gross_dollar_amount = []
    for actor_link in cast_links[:num_actors]:
        actor_imdb = requests.get('https://www.imdb.com/' + actor_link)
        actor = BeautifulSoup(actor_imdb.content, 'html.parser')
        name = actor.find(class_="itemprop").get_text()
        if (name not in non_named_characters):
            films = get_films(actor)
            num_projects = 0
            highest_gross = 0
            gross_movie = ""
            for film in films:
                year = re.sub('[^0-9,.]', '',
                              film.find(class_='year_column').get_text())
                if (year != '' and int(year) > 2008 and
                   film.find('a').get_text() not in twilight_movies):
                    num_projects += 1
                    link = film.find('a').get('href')
                    box_office_earning = get_box_office(link)
                    if (box_office_earning > highest_gross):
                        highest_gross = box_office_earning
                        gross_movie = film.find('a').get_text()
            actors_names.append(name)
            number_projects.append(num_projects)
            highest_grossing_movies.append(gross_movie)
            gross_dollar_amount.append(highest_gross)
    return pd.DataFrame({
        'name': actors_names,
        'num_projects': number_projects,
        'highest_grossing_movie': highest_grossing_movies,
        'gross_dollar_amount': gross_dollar_amount
    })


def main():
    """
    Scrape the Twilight IMDB page for actors' projects
    to get the necessary data. Exports the final
    dataset into actors.csv
    """
    twilight_url = "https://www.imdb.com/title/tt1099212/" \
                   "fullcredits?ref_=tt_cl_sm#cast"
    twilight = requests.get(twilight_url)
    twilight_page = BeautifulSoup(twilight.content, 'html.parser')
    df = collect_data(twilight_page)
    df.to_csv(path_or_buf="actors.csv", index=False)


if __name__ == '__main__':
    main()
