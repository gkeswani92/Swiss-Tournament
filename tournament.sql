-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Creating the database
CREATE DATABASE tournament;

-- Creating the players table with the id as the primary key
CREATE TABLE players ( 
id serial primary key,
name text);

CREATE TABLE matches ( 
player1 integer references players(id), 
player2 integer references players(id), 
result integer, primary key(player1, player2) );

