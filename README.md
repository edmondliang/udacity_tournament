# udacity_tournament
This project is part of Udacity course. You can use this project in Swiss pairings system.

### Goal
The goal of the Swiss pairings system is to pair each player with an opponent who has won the same number of matches, or as close as possible.

You can assume that the number of players in a tournament is an even number. This means that no player will be left out of a round.

Your code and database only needs to support a single tournament at a time. All players who are in the database will participate in the tournament, and when you want to run a new tournament, all the game records from the previous tournament will need to be deleted. In one of the extra-credit options for this project, you can extend this program to support multiple tournaments.

### Getting Started
You will need Python version 2.7.6 or up and Postgresql 9.0 or up to get started. Download or clone this repository to your computer. Configure database setting in tournament.py and run tournament.sql in postgresql. 

### Other information
There is a unit test file(tournament_test.py) included and provided by Udacity.