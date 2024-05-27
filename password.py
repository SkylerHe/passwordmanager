#Skyler He & Alina Enikeeva

# Import system packages
import random
import string


"""
Steps:
    1. Load wordlist (credit to George Flanagin)
    2. Random pick two words from wordlist and shuffle with digits and special characters.
         default_alphabet = string.ascii_letters + string.digits + '/+=!~-?'
    3. Random capitalize 5 letters and generate the final password
"""


def password_generator(file_path):

    """
    Load words from the wordlist* file into a list. 
    Random pick two words from wordlists
    and shuffle with digits and limit special characters.
    Capitlize random 5 letters and max length is 20
    Safety set: replace lower case l to upper case, upper case O to lower case o
    Finally, return the password 
    """
    # Load words from the wordlist* file into a list
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file if line.strip()]
    
    # Define the default alphabet and shuffle it
    default_alphabet = string.ascii_letters + string.digits + '/+=!~-?'
    shuffled_alphabet = ''.join(random.sample(default_alphabet, len(default_alphabet)))

    # Select 2 random words
    selected_words = random.sample(words, k=2)
    combined = ''.join(selected_words)

    # Fill the remaining length with characters from the shuffled alphabet
    remaining_length = random.randint(5, max(5, 25 - len(combined)))
    remaining_chars = ''.join(random.choices(shuffled_alphabet, k=remaining_length))
    
    # Combine the words and remaining characters
    combined += remaining_chars
    
    # Capitalize 5 random letters
    letters = list(filter(str.isalpha, combined))
    caps = random.sample(letters, min(5, len(letters)))
    for cap in caps:
        combined = combined.replace(cap, cap.upper(), 1)
    
    # Safety net
    for letter in combined:
        if letter == "i":
            password = combined.replace(letter, letter.upper())
        elif letter == "O":
            password = combined.replace(letter, letter.lower())
    return password


