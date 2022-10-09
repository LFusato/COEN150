import hashlib
import time

unsaltedTable = list()
saltedTable = list()
usernames = list()
passwords = list()
plainPasswords = list()

salt = list()
usernamesSalt = list()
passwordsSalt = list()

#hashes the passwords from file and adds them to passwords list
def generate_unsalted_table():
    realPasswords = open("passes_real.txt", "r")
    for x in realPasswords:
        #hash plaintext
        unsaltedHash = hashlib.sha256(x.split()[0].encode('utf-8')).hexdigest()
        #add to unsalted table list
        unsaltedTable.append(unsaltedHash)
        #make plaintext file for reference when comparing later
        plainPasswords.append(x)
    realPasswords.close()

#separates out breached data and compares with passwords
def compare_unsalted_passwords():
    data = open("breached_data.txt", "r")
    #split text file into username and password
    for x in data:
        tabcount = 0
        position = 0
        for y in x:
            if y == "\t":
                tabcount += 1
            position += 1
            #based on formatting tab indicates user and pass, so separate
            if tabcount == 2:
                usernames.append(x[:position-2])
                passwords.append(x[position:-1])
                break

    data.close()
    
    cracked = open("cracked_passwords.txt", "w")
    userNum = 0
    totalCracked = 0
    #start computation time
    startTime = time.process_time()
    for x in passwords:
        passNum = 0
        for y in unsaltedTable:
            #when a match is found add to the cracked file
            if x == y:
                cracked.write(usernames[userNum] + "\t\t" + plainPasswords[passNum])
                totalCracked += 1
                break
            passNum += 1
        userNum += 1
    cracked.close()
    endTime = time.process_time()
    #print to console
    print("Unsalted Done in " + str(endTime - startTime) + " seconds.")
    print("A total of " + str(totalCracked) + " passwords cracked.")

def separate_salted_data():
    data = open("breached_data_salted.txt", "r")
    #split text file into username, salt, and password
    for x in data:
        tabcount = 0
        position = 0
        startOfSalt = 0
        for y in x:
            if y == "\t":
                tabcount += 1
            #tabs indicate user, salt, and pass so separate into each list
            if tabcount == 2:
                usernamesSalt.append(x[:position-1])
                startOfSalt = position + 1
                #increment tab by 1 so theres no repeat addition to list
                tabcount += 1
            if tabcount == 4:
                salt.append(x[startOfSalt:position])
            if tabcount == 5:
                passwordsSalt.append(x[position+1:-1])
                break
            position += 1

    data.close()

def generate_salted_table():
    realPasswords = open("passes_real.txt", "r")
    for x in realPasswords:
        #generate first hash with passwords only
        saltedHash1 = hashlib.sha256(x.split()[0].encode('utf-8')).hexdigest()
        maxSalts = 0
        #only complete for first 100 salts
        for y in salt[0:99]:
            #generate final hash with previous hash and salt
            saltedHash2 = hashlib.sha256(salt[maxSalts].encode('utf-8') + saltedHash1.encode('utf-8')).hexdigest()
            saltedTable.append(saltedHash2)
            maxSalts += 1
    realPasswords.close()

def compare_salted_passwords():
    cracked = open("cracked_passwords_salted.txt", "w")
    userNum = 0
    totalCracked = 0
    startTime = time.process_time()
    for x in passwordsSalt:
        passNum = 0
        for y in saltedTable:
            #compare with table for hashes that match, add to file if there is any
            if x == y:
                #% 100 is used since 100 passwords for every username due to salt
                cracked.write(usernames[userNum] + "\t\t" + plainPasswords[passNum % 100])
                totalCracked += 1
                break
            passNum += 1
        userNum += 1
    endTime = time.process_time()
    cracked.close()
    #print to console
    print("Unsalted Done in " + str(endTime - startTime) + " seconds.")
    print("A total of " + str(totalCracked) + " passwords cracked.")

#start unsalted table
print("Starting unsalted...")
generate_unsalted_table()
compare_unsalted_passwords()

#start salted table
print("Starting salted")
separate_salted_data()
generate_salted_table()
print("Salted table generated")
compare_salted_passwords()