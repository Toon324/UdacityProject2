-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Not used by in any of the tests, but useful for displaying tournament results by a friendly name
CREATE TABLE TournamentNames (
    Id serial primary key,
    TournamentName text
);

CREATE TABLE PlayerNames (
  Id serial primary key,
  PlayerName text
  );

CREATE TABLE PlayerResults (
  TournamentId integer,
  PlayerId integer,
  Wins integer,
  Losses integer,
  Ties integer
  );

-- This view is used to display the results easily, and sorts players by wins
CREATE VIEW TournamentResults AS SELECT TournamentId, PlayerId, PlayerName, Wins, Losses, Ties from PlayerResults, PlayerNames
WHERE PlayerResults.PlayerId = PlayerNames.Id
ORDER BY Wins DESC;
