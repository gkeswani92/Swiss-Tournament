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
    cursor.execute("SELECT * FROM players NATURAL JOIN statistics ORDER BY wins DESC")
    rows = cursor.fetchall()
    return rows;
    
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO matches VALUES (%s,%s,%s)",(winner,loser,winner))
    
    #Updating the winners statistics
    cursor.execute("SELECT wins, played FROM statistics WHERE id = %s",(winner,))
    rows = cursor.fetchone()
    cursor.execute("UPDATE statistics SET wins = %s WHERE id = %s",(rows[0] + 1, winner,))
    cursor.execute("UPDATE statistics SET played = %s WHERE id = %s",(rows[1] + 1, winner,))
    
    #Updating the losers statistics
    cursor.execute("SELECT wins, played FROM statistics WHERE id = %s",(loser,))
    rows = cursor.fetchone()
    cursor.execute("UPDATE statistics SET wins = %s WHERE id = %s",(rows[0], loser,))
    cursor.execute("UPDATE statistics SET played = %s WHERE id = %s",(rows[1] + 1, loser,))
   
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
    

