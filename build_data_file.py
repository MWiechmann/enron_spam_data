import requests
import shutil
import os
import re
import datetime as dt
import sys
import pandas as pd

# Downloading and Unpacking data
# Download original email dataset from Athens University of Economics and Business website
print('Beginning download of email data set from http://www.aueb.gr/users/ion/data/enron-spam...')

url_base = 'http://www.aueb.gr/users/ion/data/enron-spam/preprocessed/'
enron_list = ["enron1", "enron2", "enron3", "enron4", "enron5", "enron6"]

os.mkdir("raw data")

for entry in enron_list:
    print("Downloading archive: " + entry + "...")

    # Download current enron archive
    url = url_base + entry + ".tar.gz"
    r = requests.get(url)
    path = "raw data/" + entry + ".tar.gz"

    with open(path, 'wb') as f:
        f.write(r.content)
    print('...done! Archive saved to: ' + path)

    # Unpack current archive this will unpack to /raw data/enron1, etc
    print("Unpacking contents of " + entry + " archive...")
    shutil.unpack_archive(path, "raw data/")
    print("...done! Archive unpacked to: raw data/" + entry)

print("All email archieves downloaded and unpacked. Now beggining processing of email text files.")

# Processing data
# The data is recorded in such a way, that each message is in a seperate file.
# Therefore, we have to open each single file, parse it and add it to a dataframe

mails_list = []

print("Processing directories...")
# go through all dirs in the list
# each dir contains a ham & spam folder
for directory in enron_list:
    print("...processing " + str(directory) + "...")
    ham_folder = "raw data/" + directory + "/ham"
    spam_folder = "raw data/" + directory + "/spam"
    i = 0

    # Process ham messages in directory
    for entry in os.scandir(ham_folder):
        # This should be encoded in Latin_1 but catch encoding errors just to be sure
        try:
            file = open(entry, encoding="latin_1")
            content = file.read().split("\n", 1)
        except (UnicodeDecodeError):
            print("COULD NOT DECODE")
            print("Problem with file:" + str(entry))
            print("Error message:", sys.exc_info()[1])
        subject = content[0].replace("Subject: ", "")
        message = content[1]
        # date is contained in filename - parsed using regex pattern
        pattern = r"\d+\.(\d+-\d+-\d+)"
        date = re.search(pattern, str(entry)).group(1)
        date = dt.datetime.strptime(date, '%Y-%m-%d')
        file.close()
        mails_list.append([subject, message, "ham", date])

    # Process spam messages in directory
    for entry in os.scandir(spam_folder):
        try:
            file = open(entry)
            file = open(entry, encoding="latin_1")
        except (UnicodeDecodeError):
            print("COULD NOT DECODE")
            print("Problem with file:" + str(entry))
            print("Error message:", sys.exc_info()[1])
        subject = content[0].replace("Subject: ", "")
        message = content[1]
        # date is contained in filename - parsed using regex pattern
        pattern = r"\d+\.(\d+-\d+-\d+)"
        date = re.search(pattern, str(entry)).group(1)
        date = dt.datetime.strptime(date, '%Y-%m-%d')
        file.close()
        mails_list.append([subject, message, "spam", date])

    print(str(directory)+" processed!")

print("All directories processed. Writing to Dataframe...")
mails = pd.DataFrame(mails_list, columns=[
                     "Subject", "Message", "Spam/Ham", "Date"])
print("...done!")

# Save to file
print("Saving data to file...")
mails.to_csv("enron_spam_data.csv")
print("...done! Data saved to 'enron_spam_data.csv'")

# Confirmation message and data count
print("\nData processed and saved to file.\nMails contained in data:")
print("\nTotal:\t" + str(mails.shape[0]))
print(mails["Spam/Ham"].value_counts())