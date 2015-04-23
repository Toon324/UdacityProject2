#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=results")

##Database
Database = connect();

""" 'But wait, these methods are the same!' A note on database design

    To most effictively implement multi-tournament records, a table that contained a reference to tournament and player, along with Win/Loss/Tie stats was created.
    The list of all players registered is stored in the PlayerName table, which links ID to Name. Clearing a tournament's players shouldn't remove ALL players,
    and a player may wish to enter future tournaments without re-registering, so we leave this table unaltered.

    A record in PlayerResults that matches tournamentId represents that a player is part of a tournament. This is created as 0/0/0 for W/L/T.
    Therefore, since keeping track of players in a tournament and their matches are the same record, these methods do the same thing.
"""

def deleteMatches(tournamentId):
    """Remove all the match records from the database."""
    cursor = Database.cursor()
    cursor.execute("DELETE FROM PlayerResults WHERE TournamentId = %s", str(tournamentId))
    cursor.close()


def deletePlayers(tournamentId):
    """Remove all the player records from the database."""
    cursor = Database.cursor()
    cursor.execute("DELETE FROM PlayerResults WHERE TournamentId = %s", str(tournamentId))
    cursor.close()

def countPlayers(tournamentId):
    """Returns the number of players currently registered."""
    cursor = Database.cursor()
    cursor.execute("SELECT COUNT(*) FROM PlayerResults WHERE TournamentId = %s", str(tournamentId))

    count = cursor.fetchall()[0][0]

    cursor.close()

    return count


def registerPlayer(tournamentId, name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    cursor = Database.cursor()
    cursor.execute("INSERT INTO PlayerNames (PlayerName) VALUES (%s)", (bleach.clean(name),))
    cursor.execute("SELECT Id FROM PlayerNames WHERE PlayerName = %s", (bleach.clean(name),))

    playerId = cursor.fetchall()[0][0]

    cursor.execute("INSERT INTO PlayerResults (TournamentId, PlayerId, Wins, Losses, Ties) VALUES (" + str(tournamentId) + ", " + str(playerId) + ", 0, 0, 0)")
    cursor.close()


def playerStandings(tournamentId):
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
    cursor = Database.cursor()

    """The table supports Wins, Losses, and Ties. We use COALESCE to add these numbers up to get the total number of games, to save on Database space"""
    cursor.execute("SELECT PlayerId, PlayerName, Wins, COALESCE(Wins,0) + COALESCE(Losses, 0) + COALESCE(Ties, 0) FROM TournamentResults WHERE TournamentId = %s", str(tournamentId))

    standings = cursor.fetchall()
    cursor.close()

    return standings

def reportMatch(tournamentId, winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    cursor = Database.cursor()
    cursor.execute("UPDATE PlayerResults SET Wins = Wins+1 WHERE TournamentId = " + str(tournamentId) + " AND PlayerId = " + str(winner))
    cursor.execute("UPDATE PlayerResults SET Losses = Losses+1 WHERE TournamentId = " + str(tournamentId) + " AND PlayerId = " + str(loser))
    cursor.close()

def swissPairings(tournamentId):
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
    cursor = Database.cursor()
    cursor.execute("SELECT PlayerId, PlayerName FROM TournamentResults WHERE TournamentId = %s", str(tournamentId))

    results = cursor.fetchall()

    pairings = []

    """Build the results by taking 2 players at a time and grouping them together into a tuple. Please note, this assumes that an even number of players in the system."""
    for x in xrange (0, len(results), 2):
        pairings.append((results[x][0], results[x][1], results[x+1][0], results[x+1][1]))

    cursor.close()

    return pairings