-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Not used by in any of the standard tests, but useful for displaying tournament results by a friendly name
CREATE TABLE TournamentNames (
    Id serial primary key,
    TournamentName text
);

-- Relates playerId to a name
CREATE TABLE PlayerNames (
  Id serial primary key,
  PlayerName text
  );

-- Contains records of players in a tournament, and their match history
CREATE TABLE PlayerResults (
  TournamentId integer references TournamentNames(Id),
  PlayerId integer references PlayerNames(Id),
  Wins integer,
  Losses integer,
  TotalMatches integer
  );

-- This view is used to display the results easily, and sorts players by wins
CREATE VIEW TournamentResults AS SELECT TournamentId, PlayerId, PlayerName, Wins, Losses, TotalMatches from PlayerResults, PlayerNames
WHERE PlayerResults.PlayerId = PlayerNames.Id
ORDER BY Wins DESC;
