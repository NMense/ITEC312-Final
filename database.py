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
    
# Updates team field in Team
def update_team(conn, cursor):
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
def list_team(conn, cursor):
    # Fetches list of teams
    cursor.execute("SELECT * FROM Team")
    results = cursor.fetchall()
    
    print("TeamID, T_Name, School")
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

# Searches for a team by team_id
def search_team_by_id(conn, cursor, team_id):
    search_query = "SELECT TeamID, T_Name, School FROM Team WHERE TeamID = ?"
    
    cursor.execute(search_query, (team_id,))
    team = cursor.fetchone()
    
    if team:
        print(f"Team found - ID: {team[0]}, Name: {team[1]}, School: {team[2]}")
    else:
        print("Team not found for the given ID.")
    
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
    
# Updates name of sport
def update_sport(conn, cursor):
    sport = int(input("What is the SportID you are trying to update? "))
    
    name = input("What is the new name of the sport? ")
    
    update = """UPDATE Sport SET S_Name = ? WHERE SportID = ?"""
    fields = (name, sport)
    cursor.execute(update, fields)
    
    conn.commit()
    print("Name has been updated")

# Lists sports currently in Sport table
def list_sport(conn, cursor):
    # Fetches list of sports
    cursor.execute("SELECT * FROM Sport")
    results = cursor.fetchall()
    
    print("SportID, S_Name")
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

# Searches for a sport by sport_id
def search_sport_by_id(conn, cursor, sport_id):
    search_query = "SELECT SportID, S_Name FROM Sport WHERE SportID = ?"
    
    cursor.execute(search_query, (sport_id,))
    sport = cursor.fetchone()
    
    if sport:
        print(f"Sport found - ID: {sport[0]}, Name: {sport[1]}")
    else:
        print("Sport not found for the given ID.")

# Adds match to Match and Teammatch
def add_match(conn, cursor):
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
    matchid = find_match(conn, cursor, match)

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
def find_match(conn, cursor, match):
    search = """SELECT MatchID FROM Match WHERE SportID = ? AND Date = ? AND Location = ?"""
    
    # Gets MatchID as tuple
    result = cursor.execute(search, match)
    result = cursor.fetchone()
    
    # Converts to str and searchs for numeric values
    m_id = tuple_to_int(result)
    print("MatchID is", m_id)
    
    return m_id

# Lists matches in Match
def list_match(conn, cursor):
    cursor.execute("SELECT * FROM Match")
    results = cursor.fetchall()
    
    print("MatchID, Date, Location, SportID")
    for row in results:
        print(row)
        
    conn.close()

# Deletes match from Match
def delete_match(conn, cursor):
    m_id = int(input("What is the MatchID you would like to delete? "))
    
    remove = """DELETE FROM Match WHERE MatchID = ?"""
                
    cursor.execute(remove, (m_id,))
    
    conn.commit()

# Updates match scores in Teammatch
def update_match(conn, cursor):
    m_id = int(input("What is the MatchID you are trying to update? "))
    
    teammatchfind = """SELECT TeamID FROM Teammatch WHERE MatchID = ?"""
    results = cursor.execute(teammatchfind, (m_id,))
    results = cursor.fetchall()
    
    for row in results:
        teamid = tuple_to_int(row)
        team = find_team_name(conn, cursor, teamid)
        
        print("What was the points for", team, "? ")
        score = int(input()) 
        var = (score, m_id, teamid)
        
        update_teammatch(conn, cursor, var)
    
    conn.commit()
    print("Score has been updated")
     
# Updates score in Teammatch
def update_teammatch(conn, cursor, var):
    update = """UPDATE Teammatch SET Score = ? WHERE MatchID = ? AND TeamID = ?"""
    
    cursor.execute(update, var)
      
# Converts tuplt to str to search for numeric values and return as int
def tuple_to_int(num):
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
            add_match(conn, cursor)
        elif ch == 2:
            update_match(conn, cursor)
        elif ch == 3:
            list_match(conn, cursor)
        elif ch == 4:
            delete_match(conn, cursor)
        elif ch == 5:
            add_team(conn, cursor)
        elif ch == 6:
            update_team(conn, cursor)
        elif ch == 7:
            list_team(conn, cursor)
        elif ch == 8:
            delete_team(conn,cursor)
        elif ch == 9:
            add_sport(conn, cursor)
        elif ch == 10:
            update_sport(conn, cursor)
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
    
    except sqlite3.IntegrityError as e:
        print("Integrity Error!")
        print(e)
    
    except sqlite3.ProgrammingError as e:
        print("Programming Error!")
        print(e)
        
    except sqlite3.OperationalError as e:
        print("Operational Error!")
        print(e)

database_main()