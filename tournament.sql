-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--swich database to postgres
\c  postgres
--delete database if exists
drop database if exists tournament;
--create database 'tournament'
create database tournament;
--swich database to tournament'
\c tournament

-- delete view 'playersRanking' if exists
-- DROP VIEW IF EXISTS playersRanking;

-- delete view 'playerStandings' if exists
-- DROP VIEW IF EXISTS playerStandings;

-- delete talbe 'players' if exists
-- DROP TABLE IF EXISTS players;

-- create talbe 'players'
CREATE TABLE players(id serial primary key, name varchar(50));

-- delete talbe 'matches' if exists
-- DROP TABLE IF EXISTS matches;

-- create talbe 'matches'
CREATE TABLE matches(id serial primary key, round integer, player_id integer , opponent_id integer, is_win integer DEFAULT 0, is_lose integer DEFAULT 0, is_draw integer DEFAULT 0, is_bye integer DEFAULT 0, score integer DEFAULT 0);

-- create view 'playerStandings' to summerize player standings
CREATE VIEW playerStandings AS
  (SELECT a.id,
          a.name,
          COALESCE(b.wins,0) AS wins,
          COALESCE(b.loses,0) AS loses,
          COALESCE(b.draws,0) AS draws,
          COALESCE(b.byes,0) AS byes,
          COALESCE(b.scores,0) AS scores,
          COALESCE(b.matches,0) AS matches,
          COALESCE(f.opponent_scores,0) AS opponent_scores
   FROM players AS a
   LEFT JOIN
     (SELECT player_id,
             sum(is_win) AS wins,
             sum(is_lose) AS loses,
             sum(is_draw) AS draws,
             sum(is_bye) AS byes,
             sum(score) AS scores,
             count(*) AS matches
      FROM matches
      GROUP BY player_id) AS b ON a.id=b.player_id
   LEFT JOIN
     (SELECT d.player_id,
             sum(e.score) AS opponent_scores
      FROM matches d
      LEFT JOIN matches e ON d.opponent_id=e.player_id
      GROUP BY d.player_id) AS f ON a.id=f.player_id);

-- create view 'playerStandings' to add extra information in view 'playerStandings' for sorting
CREATE VIEW playersRanking AS
  (SELECT row_number() over(
                            ORDER BY scores DESC ,opponent_scores DESC) AS rid,
                       rank() over(
                                   ORDER BY scores DESC ,opponent_scores DESC) AS rank,
                              *
   FROM playerStandings);

-- SELECT a.id AS player1,
-- 	   a.name as name1,
--        a.rank AS rank1,
--        b.id AS player2,
--        b.name as name2,
--        b.rank AS rank2
-- FROM playersranking a, playersranking b
-- WHERE (NOT exists
--     (SELECT *
--      FROM matches
--      WHERE (a.id=matches.player_id
--        AND b.id=matches.opponent_id) or (b.id=matches.player_id
--        AND a.id=matches.opponent_id) ))
--   AND a.id<b.id
--   and a.rid<b.rid
--   and a.rank>=b.rank;
