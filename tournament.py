#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

score_type = {"win": 3, "lose": 0, "draw": 1, "bye": 3}


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("delete from matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("delete from players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("select count(*) as num from players")
    row = cur.fetchone()
    conn.close()
    return row[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("insert into players(name) values(%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("select id,name,wins,matches from playerStandings")
    result = cur.fetchall()
    conn.close()
    return result


def reportMatch(winner, loser, draw=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    is_draw = 0
    is_win = 1
    is_lose = 0
    if(draw):
        is_draw = 1
        is_win = 0
        is_lose = 0

    conn = connect()
    cur = conn.cursor()
    cur.execute("""insert into matches(player_id,opponent_id,is_win,is_lose,is_draw,is_bye,
        score) values(%s,%s,%s,%s,%s,0,%s)""", (winner, loser, is_win, is_lose, is_draw, score_type['win']),)
    cur.execute("""insert into matches(player_id,opponent_id,is_win,is_lose,is_draw,is_bye,
        score) values(%s,%s,%s,%s,%s,0,%s)""", (loser, winner, is_lose, is_win, is_draw, score_type['lose']),)
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id AS id1,
               a.name AS name1,
               b.id AS id2,
               b.name AS name2
        FROM playersranking a, playersranking b
        WHERE (NOT exists
            (SELECT *
             FROM matches
             WHERE (a.id=matches.player_id
               AND b.id=matches.opponent_id) or (b.id=matches.player_id
               AND a.id=matches.opponent_id) ))
          AND a.id<b.id
          and a.rid<b.rid
          and a.rank>=b.rank;
        """)
    result = cur.fetchall()
    conn.close()
    return result
