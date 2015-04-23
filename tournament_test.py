#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

tournamentId = 1

def testDeleteMatches():
    deleteMatches(tournamentId)
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches(tournamentId)
    deletePlayers(tournamentId)
    print "2. Player records can be deleted."


def testCount():
    deleteMatches(tournamentId)
    deletePlayers(tournamentId)
    c = countPlayers(tournamentId)
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches(tournamentId)
    deletePlayers(tournamentId)
    registerPlayer(tournamentId, "Chandra Nalaar")
    c = countPlayers(tournamentId)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches(tournamentId)
    deletePlayers(tournamentId)
    registerPlayer(tournamentId, "Markov Chaney")
    registerPlayer(tournamentId, "Joe Malik")
    registerPlayer(tournamentId, "Mao Tsu-hsi")
    registerPlayer(tournamentId, "Atlanta Hope")
    c = countPlayers(tournamentId)
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers(tournamentId)
    c = countPlayers(tournamentId)
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches(tournamentId)
    deletePlayers(tournamentId)
    registerPlayer(tournamentId, "Melpomene Murray")
    registerPlayer(tournamentId, "Randy Schwartz")
    standings = playerStandings(tournamentId)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches(tournamentId)
    deletePlayers(tournamentId)
    registerPlayer(tournamentId, "Bruno Walton")
    registerPlayer(tournamentId, "Boots O'Neal")
    registerPlayer(tournamentId, "Cathy Burton")
    registerPlayer(tournamentId, "Diane Grant")
    standings = playerStandings(tournamentId)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournamentId, id1, id2)
    reportMatch(tournamentId, id3, id4)
    standings = playerStandings(tournamentId)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches(tournamentId)
    deletePlayers(tournamentId)
    registerPlayer(tournamentId, "Twilight Sparkle")
    registerPlayer(tournamentId, "Fluttershy")
    registerPlayer(tournamentId, "Applejack")
    registerPlayer(tournamentId, "Pinkie Pie")
    standings = playerStandings(tournamentId)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournamentId, id1, id2)
    reportMatch(tournamentId, id3, id4)
    pairings = swissPairings(tournamentId)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."

def testMultiTournament():
    deleteMatches(0)
    deleteMatches(0)
    deletePlayers(1)
    deletePlayers(1)

    registerPlayer(0, "Mark Haynes")
    registerPlayer(0, "Jacob Reynolds")
    registerPlayer(0, "Sir Lancelot")
    registerPlayer(0, "Snoop Dawg")

    registerPlayer(1, "Ken")
    registerPlayer(1, "Barbie")

    c1 = countPlayers(0)
    c2 = countPlayers(1)

    if (c1 != 4):
        raise ValueError("Tournament 0 should have 4 players, but " + str(c1) + " was found.")

    if (c2 != 2):
        raise ValueError("Tournament 1 should have 2 players, but " + str(c2) + " was found.")

    print "9. Multiple tournaments are managed properly."


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testMultiTournament()
    print "Success!  All tests pass!"
