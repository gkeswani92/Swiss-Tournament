-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

CREATE TABLE players ( 
id serial primary key,
name text);

CREATE TABLE matches ( 
player1 integer references players(id) ON DELETE CASCADE, 
player2 integer references players(id) ON DELETE CASCADE, 
result integer, primary key(player1, player2) );

CREATE TABLE statistics (
id integer references players ON DELETE CASCADE, 
wins integer, 
played integer);

CREATE VIEW standings AS SELECT * FROM players NATURAL JOIN statistics ORDER BY wins DESC;
