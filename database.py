import sqlite3
import time

# Create the database
def create_database():
    # Create database file and connect it to variable
    conn = sqlite3.connect('match.db')
    cursor = conn.cursor()
    
    # Create database
    cursor.execute(create_match())
    cursor.execute(create_sport())
    cursor.execute(create_team())
    cursor.execute(create_teammatch())
    
    # Save and close
    conn.commit()
    conn.close()

# Creates the match table. Used to track time and location of matches
def create_match():
    match = """CREATE TABLE IF NOT EXISTS Match(
                MatchID INTEGER PRIMARY KEY AUTOINCREMENT,
                Date TEXT NOT NULL,
                Location TEXT,
                SportID INTEGER,
                FOREIGN KEY(SportID) REFERENCES
                    Sport(SportID))"""
    
    return match

# Creates the sport table. Used to identify which sport was played in a match
def create_sport():
    sport = """CREATE TABLE IF NOT EXISTS Sport(
                SportID INTEGER PRIMARY KEY AUTOINCREMENT,
                S_Name TEXT NOT NULL)"""
    
    return sport

# Creates the team table. Used to keep track of team details
def create_team():
    team = """CREATE TABLE IF NOT EXISTS Team(
                TeamID INTEGER PRIMARY KEY AUTOINCREMENT,
                T_Name TEXT NOT NULL,
                School TEXT)"""

    return team

# Creates the TeamMatch table. This is the inbetween table to create a M:M between the Team and Match tables. Tracks score
def create_teammatch():
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
def add_team(conn, cursor):
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

# Lists teams currently in database
def list_team(conn, cursor):
    # Fetches list of teams
    cursor.execute("SELECT TeamID, T_Name, School FROM Team")
    results = cursor.fetchall()
    
    for row in results:
        print(row)
    
    conn.commit()
    conn.close()
    
# Deletes team from TEAM table
def delete_team(conn, cursor):
    team_id = int(input("What is the team ID you would like to delete? "))
    
    remove = """DELETE FROM Team WHERE TeamID = ?"""
                
    cursor.execute(remove, (team_id,))
    
    conn.commit()
    conn.close()
    
# Adds sport to the Sport table
def add_sport(conn, cursor):
    # Prompts user for team and school name
    s_name = input("What is the name of the sport? ")
    
    # SQL variables and statement
    add = """INSERT INTO Sport(S_Name)
             VALUES(?)"""     
                 
    cursor.execute(add, (s_name,))
        
    conn.commit()
    conn.close()

# Lists sports currently in Sport table
def list_sport(conn, cursor):
    # Fetches list of sports
    cursor.execute("SELECT SportID, S_Name FROM Sport")
    results = cursor.fetchall()
    
    for row in results:
        print(row)
    
    conn.commit()
    conn.close()
    
# Deletes sport from Sport table
def delete_sport(conn, cursor):
    s_id = int(input("What is the sport ID you would like to delete? "))
    
    remove = """DELETE FROM Sport WHERE SportID = ?"""
                
    cursor.execute(remove, (s_id,))
    
    conn.commit()
    conn.close()

# Used to manipulate the database
def database_main():
    try:
        conn = sqlite3.connect('match.db')
        cursor = conn.cursor()
        
        # Foreign key enforcement
        cursor.execute("PRAGMA foreign_keys=ON")
    
        # Choice list for operation
        print("What would you like to do?")
        print("1) Add Match")
        print("2) Update Match")
        print("3) Get list of matches")
        print("4) Delete Match")
        print("5) Add Team")
        print("6) Update Team")
        print("7) Get list of teams")
        print("8) Delete Team")
        print("9) Add Sport")
        print("10) Update Sport")
        print("11) Get list of sports")
        print("12) Delete Sport")
        print("13) Quit program")
        ch = int(input())
        
        if ch == 1:
            pass
        elif ch == 2:
            pass
        elif ch == 3:
            pass
        elif ch == 4:
            pass
        elif ch == 5:
            add_team(conn, cursor)
        elif ch == 6:
            pass
        elif ch == 7:
            list_team(conn, cursor)
        elif ch == 8:
            delete_team(conn,cursor)
        elif ch == 9:
            add_sport(conn, cursor)
        elif ch == 10:
            pass
        elif ch == 11:
            list_sport(conn, cursor)
        elif ch == 12:
            delete_sport(conn, cursor)
        elif ch == 13:
            conn.commit()
            conn.close()
            return
        else:
            print("Option not available. Did you enter a value outside of 1-10?")
            time.sleep(2)
            database_main()
        
        print("\n")
        database_main()
        
    except ValueError:
            print("Value Error! Did you enter a letter for a number?")

database_main()