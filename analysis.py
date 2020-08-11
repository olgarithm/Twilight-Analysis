"""
Olga Andreeva
Section AA
Runs analysis on the scrapped data to get the actors
who have been in the most projects since Twilight along
with the highest grossing movies they've been in and
which movie that was.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def get_projects(df):
    """
    Given a DataFrame that has all the actors information in it,
    returns a sorted DataFrame by num_projects.
    """
    columns = ['name', 'num_projects']
    return df.sort_values(by='num_projects', ascending=False).loc[:, columns]


def get_grossing_movies(df):
    """
    Given a DataFrame that has all the actors information in it,
    returns a sorted DataFrame by gross_dollar_amount.
    """
    columns = ['name', 'highest_grossing_movie', 'gross_dollar_amount']
    return df.sort_values(by='gross_dollar_amount',
                          ascending=False).loc[:, columns]


def main():
    """
    Performs analysis on actors.csv, like who has been in the most
    projects since Twilight and which movie for each actor was the
    highest grossing movie (excluding the Twilight series).
    Graphs both results.
    """
    df = pd.read_csv('actors.csv').dropna()
    highest_grossing = get_grossing_movies(df)
    g = sns.catplot(x="gross_dollar_amount", y="name", color="lightgreen",
                    kind="bar", data=highest_grossing)
    g.fig.get_axes()[0].set_xscale('log')
    plt.title('Twilight Actors Highest Grossing Movies')
    plt.xlabel('Gross Dollar Amount')
    plt.ylabel('Actor Name')
    plt.savefig('highest-grossing.png', bbox_inches='tight')

    most_projects = get_projects(df)
    sns.catplot(x="num_projects", y="name", color="lightgreen",
                kind="bar", data=most_projects)
    plt.title('Twilight Actors With the Most Projects')
    plt.xlabel('Number Projects')
    plt.ylabel('Actor Name')
    plt.savefig('most-projects.png', bbox_inches='tight')


if __name__ == '__main__':
    main()
