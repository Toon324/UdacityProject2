#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

from tournament import *

def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    tournamentName = "Tournament A"
    createTournament(tournamentName)
    tournamentId = getTournamentId(tournamentName)

    deleteMatches(tournamentId)
    deletePlayers(tournamentId)
    c = countPlayers(tournamentId)
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print "1. countPlayers(tournamentId) returns 0 after initial deletePlayers(tournamentId) execution."
    registerPlayer(tournamentId, "Chandra Nalaar")
    c = countPlayers(tournamentId)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers(tournamentId) should be 1. Got {c}".format(c=c))
    print "2. countPlayers(tournamentId) returns 1 after one player is registered."
    registerPlayer(tournamentId, "Jace Beleren")
    c = countPlayers(tournamentId)
    if c != 2:
        raise ValueError(
            "After two players register, countPlayers(tournamentId) should be 2. Got {c}".format(c=c))
    print "3. countPlayers(tournamentId) returns 2 after two players are registered."
    deletePlayers(tournamentId)
    c = countPlayers(tournamentId)
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print "4. countPlayers(tournamentId) returns zero after registered players are deleted.\n5. Player records successfully deleted."

def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    tournamentName = "Tournament B"
    createTournament(tournamentName)
    tournamentId = getTournamentId(tournamentName)

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
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    tournamentName = "Tournament C"
    createTournament(tournamentName)
    tournamentId = getTournamentId(tournamentName)

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
    deleteMatches(tournamentId)
    standings = playerStandings(tournamentId)
    if len(standings) != 4:
        raise ValueError("Match deletion should not change number of players in standings.")
    for (i, n, w, m) in standings:
        if m != 0:
            raise ValueError("After deleting matches, players should have zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have zero wins recorded.")
    print "8. After match deletion, player standings are properly reset.\n9. Matches are properly deleted."

def testPairings():
    """
    Test that pairings are generated properly both before and after match reporting.
    """
    tournamentName = "Tournament D"
    createTournament(tournamentName)
    tournamentId = getTournamentId(tournamentName)

    deleteMatches(tournamentId)
    deletePlayers(tournamentId)
    registerPlayer(tournamentId, "Twilight Sparkle")
    registerPlayer(tournamentId, "Fluttershy")
    registerPlayer(tournamentId, "Applejack")
    registerPlayer(tournamentId, "Pinkie Pie")
    registerPlayer(tournamentId, "Rarity")
    registerPlayer(tournamentId, "Rainbow Dash")
    registerPlayer(tournamentId, "Princess Celestia")
    registerPlayer(tournamentId, "Princess Luna")
    standings = playerStandings(tournamentId)
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swissPairings(tournamentId)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    reportMatch(tournamentId, id1, id2)
    reportMatch(tournamentId, id3, id4)
    reportMatch(tournamentId, id5, id6)
    reportMatch(tournamentId, id7, id8)
    pairings = swissPairings(tournamentId)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "10. After one match, players with one win are properly paired."


if __name__ == '__main__':
    testCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
    deleteAllTournaments()
