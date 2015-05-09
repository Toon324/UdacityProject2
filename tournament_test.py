#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testSetupTournaments():
    deleteAllTournaments()
    createTournament('Card Games on Motorcycles')
    createTournament('Who has the best moustache')
    createTournament('Pie eating Contest')
    print "0. Three tournaments setup"

def testDeleteMatches(tournamentId):
    deleteMatches(tournamentId)
    print "1. Old matches can be deleted."


def testDelete(tournamentId):
    deleteMatches(tournamentId)
    deletePlayers(tournamentId)
    print "2. Player records can be deleted."


def testCount(tournamentId):
    deleteMatches(tournamentId)
    deletePlayers(tournamentId)
    c = countPlayers(tournamentId)
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister(tournamentId):
    deleteMatches(tournamentId)
    deletePlayers(tournamentId)
    registerPlayer(tournamentId, "Chandra Nalaar")
    c = countPlayers(tournamentId)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete(tournamentId):
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


def testStandingsBeforeMatches(tournamentId):
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


def testReportMatches(tournamentId):
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


def testPairings(tournamentId):
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

def testMultiPairing(tournamentId):
    standings = playerStandings(tournamentId)
    [id1, id2, id3, id4] = [row[0] for row in standings]

    reportMatch(tournamentId, id1, id2)
    reportMatch(tournamentId, id3, id4)

    pairings = swissPairings(tournamentId)
    if len(pairings) != 2:
        raise ValueError(
            str(tournamentId) + ": For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "Tournament " + str(tournamentId) + ": After one match, players with one win should be paired.")

def testMultiTournament():

    t1 = getTournamentId('Card Games on Motorcycles')
    t2 = getTournamentId('Who has the best moustache')

    registerPlayer(t1, "Ken")
    registerPlayer(t1, "Barbie")
    registerPlayer(t1, "Stacy's Mom")
    registerPlayer(t1, "Stacy")

    registerPlayer(t2, "Mark Haynes")
    registerPlayer(t2, "Jacob Reynolds")
    registerPlayer(t2, "Sir Lancelot")
    registerPlayer(t2, "Snoop Dawg")

    c1 = countPlayers(t1)
    c2 = countPlayers(t2)

    if (c1 != 4):
        raise ValueError("Tournament " + str(t1) + " should have 4 players, but " + str(c1) + " was found.")

    if (c2 != 4):
        raise ValueError("Tournament " + str(t2) + " should have 4 players, but " + str(c2) + " was found.")

    print "9. Multiple tournaments maintain counts properly."

    testMultiPairing(t1)
    testMultiPairing(t2)

    print "10. Swiss pairings for multiple tournaments are correct."

if __name__ == '__main__':
    #Sets up 3 tournaments for testing
    testSetupTournaments()

    t0 = getTournamentId('Pie eating Contest')

    testDeleteMatches(t0)
    testDelete(t0)
    testCount(t0)
    testRegister(t0)
    testRegisterCountDelete(t0)
    testStandingsBeforeMatches(t0)
    testReportMatches(t0)
    testPairings(t0)
    testMultiTournament()
    print "Success!  All tests pass!"
