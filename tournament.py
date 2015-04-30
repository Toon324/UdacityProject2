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

""" A note on database design

    To most effictively implement multi-tournament records, a table that contained a reference to tournament and player, along with Win/Loss/Tie stats was created.
    The list of all players registered is stored in the PlayerName table, which links ID to Name. Clearing a tournament's players shouldn't remove ALL players,
    and a player may wish to enter future tournaments without re-registering, so we leave the records in PlayerName untouched.

    A record in PlayerResults that matches tournamentId represents that a player is part of a tournament. This is created as 0/0/0 for W/L/T.
    Therefore, since keeping track of players in a tournament and their matches are the same record, these methods do the same thing.
"""

def deleteMatches(tournamentId):
    """Remove all the match records from the database.

    Args:
        tournamentId: The id of the tournament you would like to manipulate
    """
    cursor = Database.cursor()
    cursor.execute("UPDATE PlayerResults SET Wins = 0, Losses =0, TotalMatches = 0 WHERE TournamentId = " + str(tournamentId))
    cursor.close()


def deletePlayers(tournamentId):
    """Remove all the player records from the database.

    Args:
        tournamentId: The id of the tournament you would like to manipulate
    """
    cursor = Database.cursor()
    cursor.execute("DELETE FROM PlayerResults WHERE TournamentId = %s", str(tournamentId))
    cursor.close()

def countPlayers(tournamentId):
    """Returns the number of players currently registered.

    Args:
        tournamentId: The id of the tournament you would like to manipulate
    """
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
        tournamentId: The id of the tournament you would like to manipulate
    """

    cursor = Database.cursor()
    cursor.execute("INSERT INTO PlayerNames (PlayerName) VALUES (%s)", (bleach.clean(name),))
    cursor.execute("SELECT Id FROM PlayerNames WHERE PlayerName = %s", (bleach.clean(name),))

    playerId = cursor.fetchall()[0][0]

    cursor.execute("INSERT INTO PlayerResults (TournamentId, PlayerId, Wins, Losses, TotalMatches) VALUES (" + str(tournamentId) + ", " + str(playerId) + ", 0, 0, 0)")
    cursor.close()

def createTournament(name):
    """Adds a new tournament to the database.

    The id in this table is used across the rest of the code to reference which tournament methods are being called on.

    This method does not have to be called for the other methods to work, but is useful, as it registers an user-friendly name for the touramentId.

    Args:
        name: the name of the tournament
        tournamentId: The id of the tournament you would like to manipulate
    """

    cursor = Database.cursor()
    cursor.execute("INSERT INTO TournamentNames (TournamentName) VALUES (%s)", (bleach.clean(name),))
    cursor.close()

def playerStandings(tournamentId):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
        tournamentId: The id of the tournament you would like to manipulate

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    cursor = Database.cursor()

    cursor.execute("SELECT PlayerId, PlayerName, Wins, TotalMatches FROM TournamentResults WHERE TournamentId = %s", str(tournamentId))

    standings = cursor.fetchall()
    cursor.close()

    return standings

def reportMatch(tournamentId, winner, loser):
    """Records the outcome of a single match between two players.

    Args:
        tournamentId: The id of the tournament you would like to manipulate
        winner:  the id number of the player who won
        loser:  the id number of the player who lost
    """
    cursor = Database.cursor()
    cursor.execute("UPDATE PlayerResults SET Wins = Wins+1, TotalMatches = TotalMatches+1 WHERE TournamentId = " + str(tournamentId) + " AND PlayerId = " + str(winner))
    cursor.execute("UPDATE PlayerResults SET Losses = Losses+1, TotalMatches = TotalMatches+1 WHERE TournamentId = " + str(tournamentId) + " AND PlayerId = " + str(loser))
    cursor.close()

def swissPairings(tournamentId):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
        tournamentId: The id of the tournament you would like to manipulate

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
