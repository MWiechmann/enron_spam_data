# Enron Spam Dataset
The Enron-Spam dataset is a fantastic ressource collected by V. Metsis, I. Androutsopoulos and G. Paliouras and described in their publication ["Spam Filtering with 
Naive Bayes - Which Naive Bayes?"](https://nes.aueb.gr/ipl/nlp/pubs/ceas2006_paper.pdf). The dataset contains a total of 17.171 spam and 16.545 non-spam ("ham") e-mail messages (33.716 e-mails total). The original dataset and documentation can be found [here](http://www2.aueb.gr/users/ion/data/enron-spam/readme.txt).

However, the original datasets is recorded in such a way, that every single mail is in a seperate txt-file, distributed over several directories. This can make reading in the
data a bit cumbersome, especially for beginners. Since the data set is such a fantastic ressource, I wanted to create a offer a single download of the data through a simple csv-file.

**You probably only need the data file ("enron_spam_data.csv").** The python file ("build_data_file.py") contains the script used to construct the csv file (downloading the original raw data from the website, unpacking it, processing it and saving it into the csv file).

Processing of the data is minimal: The dataset contains the following columns:
Column | Explanation
---|---
Subject | The subject line of the e-mail
Message | The content of the e-mail. Can contain an empty string if the message had only a subject line and no body. In case of forwarded emails or replies, this also contains the original message with subject line, "from:", "to:", etc.
Spam/Ham | Has the values "spam" or "ham". Whether the message was categorized as a spam message or not.
Date | The date the e-mail arrived. Has a YYYY-MM-DD format.
