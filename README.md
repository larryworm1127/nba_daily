# NBA Daily

[![CircleCI](https://circleci.com/gh/larryworm1127/nba_daily.svg?style=svg)](https://circleci.com/gh/larryworm1127/nba_daily)

## About

NBA Daily is an on-going web project in hopes to implement better NBA stats 
delivery. By better, it mostly consists of better looking interface, responsive
content delivery, and overall simplicity to not overwhelm users. See features
section to see current features and possible future features.

## Technology

The website is built using Python 3 and Django web framework with future plans
of porting the front-end to react or angular (still deciding which is better),
and user Django-RESTframework to convert to Django server as a data API server.

NBA data are currently scrapped periodically and manually by running Python
scripts. The scrapped data are stored in local database but future plan may be
to scrap live data and use cache to avoid all the database management.

**Requirements:**

- Python 3
- Pipenv
- Npm

## Features

- **Games by date:** users can view all games on certain dates they select.
If there are no games on the selected date, the website allows user to navigate
to most recent game based on user current selected date. Note that due to
current data storage method, the games are only as up-to-date as the data that
are stored in the database.

- **Standing:** users can view conference standings for current season. Again
this is currently limited due to data storage method.

- **Player per game stats:** users can view all active NBA player seasonal 
performance stats. Pagination is implemented due to high-number of players.

- **Player detail stats:** users can view detailed stats for specific NBA 
players. These stats include career regular season averages, post-season
averages, as well as various misc player info such as age, height, etc.

- **Player game logs:** users can view player game logs in specific season.

- **Game box score:** users can view specific game box score.

- **Team per game stats:** similar to player player per game stats but for teams.

- **Team detail stats:** similar to player detail stats but for teams.

## Software Setup

### Basic logistics

To run the web app locally, start by clone the project:
```bash
$ git clone https://github.com/larryworm1127/nba_daily.git
```
Navigate into the project folder, and run the following:
```bash
$ pipenv sync
```
This will create a virtual environment for the web app and install all required
packages specified in `Pipenv.lock`.

Next run:
```bash
$ npm install
```
which will install required npm packages for the website.

### Populate database

Due to the new changes for NBA stats scraping, the current scapper no longer
functions correctly. Hence a copy of 2018-19 season data is stored in the repo
(JSON files) under `main/data` folder. A set of Django model fixtures are 
already created under `main/fixtures` to assist with populating the database.
Simply run
```bash
$ python get_data.py
```
or
```bash
$ ./get_data.py
```
and follow the command line tooltips to populate the database.

### Run the Django server

Lastly, simply run
```bash
$ python manage.py runserver
```
which will run the Django server and you can access the website home page
through localhost URL: http://127.0.0.1:8000/
