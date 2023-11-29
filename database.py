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

# Used to manipulate the database
def database_main():
    try:
        conn = sqlite3.connect('match.db')
        cursor = conn.cursor()
    
        # Choice list for operation
        print("What would you like to do?")
        print("1) Add Match")
        print("2) Update Match")
        print("3) Delete Match")
        print("4) Add Team")
        print("5) Update Team")
        print("6) Delete Team")
        print("7) Add Sport")
        print("8) Update Sport")
        print("9) Delete Sport")
        print("10) Quit program")
        ch = int(input)
        
        if ch == 1:
            pass
        elif ch == 2:
            pass
        elif ch == 3:
            pass
        elif ch == 4:
            pass
        elif ch == 5:
            pass
        elif ch == 6:
            pass
        elif ch == 7:
            pass
        elif ch == 8:
            pass
        elif ch == 9:
            pass
        elif ch == 10:
            conn.commit()
            conn.close()
        else:
            print("Option not available. Did you enter a value outside of 1-10?")
            time.sleep(2)
            database_main()
        
        print("\n")
        database_main()
        
    except ValueError:
            print("Value Error! Did you enter a letter for a number?")

database_main()