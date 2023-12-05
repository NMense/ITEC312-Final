from database import Database
import sqlite3
import time

def database_main():
    try:
        conn = sqlite3.connect('match.db')
        cursor = conn.cursor()
        db = Database('match.db')
        # Foreign key enforcement
        cursor.execute("PRAGMA foreign_keys=ON")
    
        # Choice list for operation
        print("What would you like to do?")
        print("1) Match options")
        print("2) Team options")
        print("3) Sport options")
        print("4) Create database")
        print("5) Save and quit program")
        ch = int(input())
        
        if ch == 1: #Match sub menu
            print("Match Menu:")
            print("1) Add Match")
            print("2) Update Match")
            print("3) List All Matches")
            print("4) Delete Match")
            ch2 = int(input())
            if ch2 == 1:
                db.add_match(conn, cursor)
            elif ch2 == 2:
                db.update_match(conn, cursor)
            elif ch2 == 3:
                db.list_match(conn, cursor)
            elif ch2 == 4:
                db.delete_match(conn, cursor)
            else:
                print("Option not available. Did you enter the correct value?")
                time.sleep(2)
                database_main()
        elif ch == 2: #Team sub menu
            print("Team Menu:")
            print("1) Add Team")
            print("2) Update Team")
            print("3) List All Teams")
            print("4) Search Teams by TeamID")
            print("5) Delete Team")
            ch3 = int(input())
            if ch3 == 1:
                db.add_team(conn, cursor)
            elif ch3 == 2:
                db.update_team(conn, cursor)
            elif ch3 == 3:
                db.list_team(conn, cursor)
            elif ch3 == 4:
                print("What TeamID to search for?")
                team_id_choice = int(input())
                db.search_team_by_id(conn, cursor, team_id_choice)
            elif ch3 == 5:
                db.delete_team(conn,cursor)
            else:
                print("Option not available. Did you enter the correct value?")
                time.sleep(2)
                database_main()
        elif ch == 3: #Sport sub menu
            print("Sport Menu:")
            print("1) Add Sport")
            print("2) Update Sport")
            print("3) List All Sports")
            print("4) Search Sports by SportID")
            print("5) Delete Sport")
            ch4 = int(input())
            if ch4 == 1:
                db.add_sport(conn, cursor)
            elif ch4 == 2:
                db.update_sport(conn, cursor)
            elif ch4 == 3:
                db.list_sport(conn, cursor)
            elif ch4 == 4:
                print("What SportID to search for?")
                sport_id_choice = int(input())
                db.search_sport_by_id(conn, cursor, sport_id_choice)
            elif ch4 == 5:
                db.delete_sport(conn, cursor)
            else:
                print("Option not available. Did you enter the correct value?")
                time.sleep(2)
                database_main()
        elif ch == 4:
            print("WARNING: You are about to create all database files in order to run this program.")
            print("This will delete any older instances of the database. Are you sure?")
            print("1 for yes, 2 for no.")
            ch5 = int(input())
            if ch5 == 1:
                db.create_database()
            elif ch5 == 2:
                database_main()
            else:
                print("Option not available. Did you enter the correct value?")
                time.sleep(2)
                database_main()
        elif ch == 5: #Save and quit program
            print("Goodbye!")
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
