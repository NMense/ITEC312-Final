import sqlite3
import time

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys=ON")
        
# Create the database
    def create_database(self):
        # Create database file and connect it to variable
        conn = sqlite3.connect('match.db')
        cursor = conn.cursor()
    
        # Create database
        cursor.execute(self.create_match())
        cursor.execute(self.create_sport())
        cursor.execute(self.create_team())
        cursor.execute(self.create_teammatch())
    
        # Save and close
        conn.commit()
        conn.close()

# Creates the match table. Used to track time and location of matches
    def create_match(self):
        match = """CREATE TABLE IF NOT EXISTS Match(
                    MatchID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Date TEXT NOT NULL,
                    Location TEXT,
                    SportID INTEGER,
                    FOREIGN KEY(SportID) REFERENCES
                        Sport(SportID))"""
        
        return match

# Creates the sport table. Used to identify which sport was played in a match
    def create_sport(self):
        sport = """CREATE TABLE IF NOT EXISTS Sport(
                    SportID INTEGER PRIMARY KEY AUTOINCREMENT,
                    S_Name TEXT NOT NULL)"""
    
        return sport

# Creates the team table. Used to keep track of team details
    def create_team(self):
        team = """CREATE TABLE IF NOT EXISTS Team(
                    TeamID INTEGER PRIMARY KEY AUTOINCREMENT,
                    T_Name TEXT NOT NULL,
                    School TEXT)"""

        return team

# Creates the TeamMatch table. This is the inbetween table to create a M:M between the Team and Match tables. Tracks score
    def create_teammatch(self):
        teammatch = """CREATE TABLE IF NOT EXISTS TeamMatch(
                        Score INTEGER,
                        TeamID INTEGER,
                        MatchID INTEGER,
                        FOREIGN KEY(TeamID) REFERENCES
                            Team(TeamID),
                        FOREIGN KEY(MatchID) REFERENCES
                            Match(MatchID),
                        PRIMARY KEY(TeamID, MatchID))"""

        return teammatch

# Adds team to the Team table
    def add_team(self, conn, cursor):
        # Prompts user for team and school name
        t_name = input("What is the name of the team? ")
        school = input("What school is this team from? ")
    
        # SQL variables and statement
        add = """INSERT INTO Team(T_Name, School)
                 VALUES(?, ?)"""     
        team = (t_name, school)
                 
        cursor.execute(add, team)
        
        conn.commit()
        conn.close()
    
# Updates team field in Team
    def update_team(self, conn, cursor):
        team = int(input("What is the TeamID you are trying to update? "))
    
        # Menu for choice
        print("Choose the field to update")
        print("1) Team Name")
        print("2) School")
        ch = int(input())
    
        # Uses ch from menu
        # Updates name for TeamID of choice
        if ch == 1:
            name = input("What is the new name of the team? ")
        
            update = """UPDATE Team SET T_Name = ? WHERE TeamID = ?"""
            fields = (name, team)
            cursor.execute(update, fields)
            
            conn.commit()
            print("Name has been updated")
        
        # Updates school for TeamID of choice
        elif ch == 2:
            school = input("What is the new school of the team? ")
        
            update = """UPDATE Team SET School = ? WHERE TeamID = ?"""
            fields = (school, team)
            cursor.execute(update, fields)
        
            conn.commit()
            print("School has been updated")

# Lists teams currently in database
    def list_team(self, conn, cursor):
        # Fetches list of teams
        cursor.execute("SELECT * FROM Team")
        results = cursor.fetchall()
    
        print("TeamID, T_Name, School")
        for row in results:
            print(row)
        
        conn.commit()
        conn.close()
    
# Deletes team from TEAM table
    def delete_team(self, conn, cursor):
        team_id = int(input("What is the team ID you would like to delete? "))
    
        remove = """DELETE FROM Team WHERE TeamID = ?"""
                
        cursor.execute(remove, (team_id,))
    
        conn.commit()
        conn.close()

# Searches for a team by team_id
    def search_team_by_id(self, conn, cursor, team_id):
        search_query = "SELECT TeamID, T_Name, School FROM Team WHERE TeamID = ?"
    
        cursor.execute(search_query, (team_id,))
        team = cursor.fetchone()
    
        if team:
            print(f"Team found - ID: {team[0]}, Name: {team[1]}, School: {team[2]}")
        else:
            print("Team not found for the given ID.")
        
# Adds sport to the Sport table
    def add_sport(self, conn, cursor):
        # Prompts user for team and school name
        s_name = input("What is the name of the sport? ")
    
        # SQL variables and statement
        add = """INSERT INTO Sport(S_Name)
                 VALUES(?)"""     
                 
        cursor.execute(add, (s_name,))
        
        conn.commit()
        conn.close()

# Updates name of sport
    def update_sport(self, conn, cursor):
        sport = int(input("What is the SportID you are trying to update? "))
    
        name = input("What is the new name of the sport? ")
    
        update = """UPDATE Sport SET S_Name = ? WHERE SportID = ?"""
        fields = (name, sport)
        cursor.execute(update, fields)
    
        conn.commit()
        print("Name has been updated")

# Lists sports currently in Sport table
    def list_sport(self, conn, cursor):
        # Fetches list of sports
        cursor.execute("SELECT * FROM Sport")
        results = cursor.fetchall()
    
        print("SportID, S_Name")
        for row in results:
            print(row)
    
        conn.commit()
        conn.close()
    
# Deletes sport from Sport table
    def delete_sport(self, conn, cursor):
        s_id = int(input("What is the sport ID you would like to delete? "))
    
        remove = """DELETE FROM Sport WHERE SportID = ?"""
                
        cursor.execute(remove, (s_id,))
    
        conn.commit()
        conn.close()

# Searches for a sport by sport_id
    def search_sport_by_id(self, conn, cursor, sport_id):
        search_query = "SELECT SportID, S_Name FROM Sport WHERE SportID = ?"
    
        cursor.execute(search_query, (sport_id,))
        sport = cursor.fetchone()
    
        if sport:
            print(f"Sport found - ID: {sport[0]}, Name: {sport[1]}")
        else:
            print("Sport not found for the given ID.")

# Adds match to Match and Teammatch
    def add_match(self, conn, cursor):
        sport = int(input("What is the sportID of the sport being played? "))
        team1 = input("What is the the teamID of the home team? ")
        team2 = input("What is the the teamID of the away team? ")
        date = input("What is the date of the match? Format: YYYY-MM-DD HH:MM ")
        loc = input("What is the location of the match being played? ")
    
    # Adds row to Match
        match = (sport, date, loc)
        add_match = """INSERT INTO Match(SportID, Date, Location)
                    VALUES(?, ?, ?)"""
        cursor.execute(add_match, match)
    
    # Finds newly created matchid in Match
        matchid = self.find_match(conn, cursor, match)

    # Adds to Teammatch with no scores
        add_teammatch = """INSERT INTO Teammatch(MatchID, TeamID)
                        VALUES(?,?)"""
        teammatch1 = (matchid, team1)                    
        teammatch2 = (matchid, team2)
    
        cursor.execute(add_teammatch, teammatch1)
        cursor.execute(add_teammatch, teammatch2)
    
        conn.commit()
        print("Match has been created")
        conn.close()

# Finds match in Match
    def find_match(self, conn, cursor, match):
        search = """SELECT MatchID FROM Match WHERE SportID = ? AND Date = ? AND Location = ?"""
    
        # Gets MatchID as tuple
        result = cursor.execute(search, match)
        result = cursor.fetchone()
    
        # Converts to str and searchs for numeric values
        m_id = self.tuple_to_int(result)
        print("MatchID is", m_id)
    
        return m_id

# Lists matches in Match
    def list_match(self, conn, cursor):
        cursor.execute("SELECT * FROM Match")
        results = cursor.fetchall()
    
        print("MatchID, Date, Location, SportID")
        for row in results:
            print(row)
        
        conn.close()

# Deletes match from Match
    def delete_match(self, conn, cursor):
        m_id = int(input("What is the MatchID you would like to delete? "))
    
        # Removes from Teammatch to prevent integrity error first
        remove1 = """DELETE FROM Teammatch WHERE MatchID = ?"""
    
        # Removes from Match
        remove2 = """DELETE FROM Match WHERE MatchID = ?"""
                
        cursor.execute(remove1, (m_id,))
        cursor.execute(remove2, (m_id,))
    
        conn.commit()
    
        print("Match has been removed")

# Updates match scores in Teammatch
    def update_match(self, conn, cursor):
        m_id = int(input("What is the MatchID you are trying to update? "))
    
        teammatchfind = """SELECT TeamID FROM Teammatch WHERE MatchID = ?"""
        results = cursor.execute(teammatchfind, (m_id,))
        results = cursor.fetchall()
    
        for row in results:
            teamid = self.tuple_to_int(row)
            team = self.find_team_name(conn, cursor, teamid)
        
            print("What was the points for", team, "? ")
            score = int(input()) 
            var = (score, m_id, teamid)
        
            self.update_teammatch(conn, cursor, var)
    
        conn.commit()
        print("Score has been updated")
     
# Updates score in Teammatch
    def update_teammatch(self, conn, cursor, var):
        update = """UPDATE Teammatch SET Score = ? WHERE MatchID = ? AND TeamID = ?"""
    
        cursor.execute(update, var)
      
# Converts tuple to str to search for numeric values and return as int
    def tuple_to_int(self, num):
        m_id = ""
        new_id = str(num)
        for char in new_id:
            if char.isnumeric():
                m_id += char
    
        # Returns as int
        m_id = int(m_id) 
        return m_id

# Returns the name of a team from Team
    def find_team_name(conn, cursor, t_id):
        search = """SELECT T_Name FROM Team WHERE TeamID = ?"""
    
        result = cursor.execute(search, (t_id,))
        result = cursor.fetchone()
        return result
