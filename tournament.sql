-- Table definitions for the tournament project.
--

--  Contains Tournament information
CREATE TABLE Tournaments (
    Id serial primary key,
    Name text
);

-- Contains Player information
CREATE TABLE Players (
  Id serial primary key,
  Name text
  );

-- Contains records of players in a tournament, and their match history
CREATE TABLE PlayerResults (
  TournamentId integer references Tournaments(Id),
  PlayerId integer references Players(Id),
  Wins integer,
  Losses integer
  );

-- This view is used to display the results easily, and sorts players by wins
CREATE VIEW TournamentResults AS
 SELECT TournamentId,
            Players.Id as PlayerId,
            Players.Name as Name,
            Wins,
            Losses
 FROM PlayerResults,
      Players
 WHERE PlayerResults.PlayerId = Players.Id
 ORDER BY Wins DESC;
