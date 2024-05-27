Our program provides the framework for the encrypted and readable password generator and manager. The access to the password manager is regulated by the master password. When the account is created, the user enters their master password. The program, then, stores this password as a hash in hash.txt. When the user enters the program and has an existing account, they are prompted to enter their master password. If the hashed version of the entered password equals the hash stored in the file, the user gets access to the program’s further functionality.

The user is presented with a choice of whether to store or retrieve their password. If the user chooses to store the password, they will be prompted to enter the website and username. The program will then automatically generate a readable and random password, encrypt it and insert it into the database for future retrieval. 

The password generation process involves a series of strategic steps to ensure both security and memorability. Initially, the system loads a wordlist, credited to George Flanagin, which provides a robust selection of words. From this list, two words are randomly chosen and then combined with a sequence of digits and special characters drawn from the default alphabet, which includes both upper and lower case letters, digits, and symbols such as '/+=!~-?'. This combination is then shuffled to randomize the order, enhancing the password's complexity. To finalize the password, five letters within the sequence are randomly capitalized, further securing the password against potential brute-force or dictionary attacks. These steps collectively create a strong and unique password every time.

To further enhance the readability and reduce common typographical errors in passwords, the password generation process includes additional modifications. Specifically, every lowercase 'i' in the chosen words is replaced with an uppercase 'L', and every uppercase 'O' is replaced with a lowercase 'o'. These substitutions help avoid confusion between visually similar characters, making the passwords easier to read and enter correctly while maintaining their complexity and security. This adjustment acts as a safety net, ensuring that passwords are both strong and user-friendly.


The encryption happens in pencryption.py and works as follows. The password is converted to bytes, which allow for further key derivation. We use salt to prevent rainbow table attacks. We use 100000 iterations to hash the password and thus increase the security of encryption. And we set the cryptographic key to 32 in length.
If the user chooses to retrieve the password, they will be prompted to enter the website and username and if the information for the provided credentials is valid, the program retrieves the password from the database, decrypts it and prints it out to the screen.

The program has a number of traps. First of all, the user input is checked against containing any characters, except for digits and alphabet characters. This helps us prevent SQL-injection attacks. Second, the program throws a number of sql exceptions. Third, even if the exception is thrown, the program behaves appropriately, printing out a meaningful message and informing the user of their options. For example, if the user is trying to retrieve a password from the website that the database has no information about, the user will get a message “I do not have data for the provided website and/or username." and will offer the user to either quit the program or continue.








