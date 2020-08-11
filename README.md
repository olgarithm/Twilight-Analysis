# Twilight Actors After Twilight

This project seeks to find which actor has acted in the most projects after
their appearance in the critically acclaimed movie Twilight (2008) and
what the most successful movie that each of the actors have been in
since Twilight. The below steps detail how to run the code to get the
answer to these questions.

## Step 1
The first file to run is `actors.py`. This file requires these modules:
* requests
* re
* pandas
* BeautifulSoup

The result of this will be a CSV file of this format
named `actors.csv`:

| name | num_projects | highest_grossing_movie | gross_dollar_amount |
| ----------- | ----------- | ----------- | ----------- |
| Kristen Stewart     | 29 | Snow White and the Huntsman |396592829
| ...   | ...        | ... | ... |

## Step 2
The next file to run is `analysis.py`. This file requires these modules:
* pandas
* seaborn
* matplotlib

The result of this will be two plots, one that represents the
highest grossing movies actors have been in (`highest-grossing.png`)
and one that represents how many projects each of the actors has
been in since 2008 (`most-projects.png`)