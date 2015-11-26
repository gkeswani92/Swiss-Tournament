#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM matches CASCADE")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players CASCADE")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM players")
    row = cursor.fetchone()
    conn.close()
    return row[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    
    #Adding the player to the players table
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (name) VALUES ((%s))",(name,))
    conn.commit()
    
    #Adding the player to the statistics table with a 0,0 win to played record
    cursor.execute("SELECT id from players WHERE id NOT IN (SELECT id from statistics)")
    rows = cursor.fetchall()
    for row in rows:
        cursor.execute("INSERT INTO statistics VALUES (%s, 0, 0)", (row))
    
    conn.commit()    
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from standings")
    rows = cursor.fetchall()
    return rows;
    
def reportMatch(winner, loser, draw = False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      
      draw: set to False by default. In case this parameter is made true, both players get 0.5 points for the game
    """
    
    conn = connect()
    cursor = conn.cursor()
    pointWinner = winner
    winnerPoints = 1
    loserPoints = 0
    
    if draw:
        pointWinner = None
        winnerPoints = 0.5
        loserPoints = 0.5
        
    #Made a design choice here to update statistics in case of a bye but not record it as a match
    #between the player and a dummy entry
    if loser:    
        cursor.execute("INSERT INTO matches VALUES (%s,%s,%s)",(winner,loser,pointWinner))
        
        #Updating the losers statistics
        cursor.execute("UPDATE statistics SET wins = wins + %s WHERE id = %s",(loserPoints, loser ,))
        cursor.execute("UPDATE statistics SET played = played + 1 WHERE id = %s",(loser,))
          
    #Updating the winners statistics
    cursor.execute("UPDATE statistics SET wins = wins + %s WHERE id = %s",(winnerPoints, winner,))
    cursor.execute("UPDATE statistics SET played = played + 1 WHERE id = %s",(winner,))
 
    conn.commit()
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    next_matches = []
    bye_candidate = None
    
    #If number of players are odd, select the last one as the bye candidate and
    #remove him from the creation of pairings
    if len(standings) % 2 == 1:
        bye_candidate = (standings[-1][0], standings[-1][1], None, None)
        standings = standings[:-1]
        
    for i in range(0, len(standings), 2):
        match = (standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1])
        next_matches.append(match)
    
    #If there is a bye candidate, add him to the list of matches
    if bye_candidate:
        next_matches.append(bye_candidate)
    
    return next_matches

