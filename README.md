# nba_daily

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
