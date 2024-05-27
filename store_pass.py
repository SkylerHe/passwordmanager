# Alina Enikeeva & Skyler He
import sys
import os
import sqlite3
import getpass
from pencryption import *
import hashlib
import re
from password import password_generator
"""
Steps:
1. Create database (datetime default, website, username, password)
2. Filter input to avoid SQL injection
3. Prompt for the database password 
"""
quit = False
db = os.path.join(os.getcwd(), "pmanager.db")
def delete_entries():
    try:
        # Connect to the database
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
    
        # Use a parameterized query to insert data
        cursor.execute("DELETE FROM pmanager")
        
        conn.commit()

    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        # Close the connection
        conn.close()

    return



def insert_data(website, username, password):
    """
    Insert data into the database table
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        
        # Create a table to store user data
        cursor.execute('''CREATE TABLE IF NOT EXISTS pmanager 
                            (time datetime default current_timestamp,
                            website varchar(30),
                            username varchar(30),
                            password varchar(300)
                        );''')


        # Use a parameterized query to insert data
        cursor.execute("INSERT INTO pmanager (website, username, password) VALUES (?, ?, ?)", (website, username, password))
        
        conn.commit()

    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        # Close the connection
        conn.close()

    return

def validate(input):
    """
    This is to prevent SQL injection or buffer overflow.
    Validation is successful if input consists of alphabet
    characters and digits only. This is to prevent SQL-injection.
    """
    if re.match("^[a-zA-Z0-9]+$", input):
        return True
    else:
        return False

def retrieve_password(website, username):
    """
    Retrieve password.
    """
    global db
    try:
        # Connect to the database
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(f"SELECT password FROM pmanager WHERE website == '{website}' and username=='{username}';")
        row = cursor.fetchone()
        conn.commit()

    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        # Close the connection
        conn.close()
    return row[0]

def hash_password_sha512(password):
    # Hash the password using SHA-512
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    return hashed_password

def validate_password(master_password):
    """
    Compare the hash of the entered password with the one in the file
    """
    with open("hash.txt", "r") as hash_file:
        stored_hash = hash_file.readline()
        if stored_hash == hash_password_sha512(master_password):
            return True
    return False

def hash_and_store(master_password):
    """
    Hash the password and store the hash in the file.
    """
    with open("hash.txt", "w") as hash_file:
        hash_file.write(hash_password_sha512(master_password))
    return
   
def check_for_duplicate(website, username):
    """
    Checks, if the database has an entry for the website and
    username.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    query = "SELECT EXISTS (SELECT 1 FROM pmanager WHERE website = ? AND username = ?)"
    cursor.execute(query, (website, username))
    exists = cursor.fetchone()[0]  # Fetchone returns a tuple, [0] accesses the first element.
    conn.close()
    return exists == 1  # Returns True if the entry exists, False otherwise

 
def main():
    print("Welcome to the Password Manager program!")
    print("Please enter the requested information.")
    while True:
        existing_or_new = input("Do you have an existing account? (Y/N) ").lower()
        if existing_or_new == "y":
            master_password = getpass.getpass("Enter your master password: ")
            if not validate_password(master_password): 
                print("Wrong password. Authentication failed.")
                continue 
                #sys.exit()
        elif existing_or_new == "n":
            # delete the previous database
            delete_entries()
            print("Let's create an account!")
            master_password = getpass.getpass("Enter your master password: ")
            hash_and_store(master_password)
        else:
            bad_entry()
            continue 
        
        encryption_key = derive_key(hash_password_sha512(master_password)) 
        while True:
            contin = False
            
            store_or_retrieve = input("Would you like to store (1) or retrieve (2) the password: ").lower()
            if str(store_or_retrieve) not in ["1", "2"]:
                bad_entry()
                quit_msg()
                continue
    
            website = input("Enter the website: ")
            if validate(website) is False:
                print("I accept only alphabet characters and digits") #bad_entry()
                continue

            username = input("Enter your username: ")
            if validate(username) is False:
                print("I accept only alphabet characters and digits")
                continue    
    
            if store_or_retrieve == "1":
                # call the function to write to the database
                try:        
                    if check_for_duplicate(website, username):
                        print("The manager already stores the password for this credentials. Try retrieving.")
                        continue
                    password = password_generator("wordlist5.txt") 
                    encrypted_password = encrypt_password(password, encryption_key)
                    insert_data(website, username, encrypted_password)
                    print(f"Here is your password {password}")
                    print("It is now encrypted and stored.")
                    #sys.exit("Good Bye.")
                    quit_msg()
                    continue
                except Exception as e:
                    print(f"Error occurred {e}")
                    quit_msg()
                    continue

            elif store_or_retrieve == "2":
                # call the function to return the password
                try:
                    encrypted_password = retrieve_password(website, username)
                    decrypted_password = decrypt_password(encrypted_password, encryption_key)
                    print(f"Here is your password: {decrypted_password}")
                    quit_msg()
                    continue
                except Exception as e:
                    print("I do not have data for provided website and/or username.")
                    continue
            else:
                bad_entry()
                quit_msg()    
                continue

        if quit is True:
            sys.exit()
            break
        elif contin is True:
            continue

def bad_entry():
    print("I could not understand what you need to do.")

def quit_msg():
    quit = input("Type 'continue' to try again or 'quit' to exit: ").strip().lower()
    if quit == "quit":
        quit = True
        sys.exit("Good Bye.")
        return False
    elif quit.lower() == "continue":
        contin = True
        pass
    else:
        quit_msg()
    


if __name__ == "__main__":
    main()
