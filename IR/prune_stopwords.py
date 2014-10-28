import os
import re
from nltk.corpus import stopwords
path = r'./processed'  # remove the trailing '\'
cachedStopWords = stopwords.words('english')
data = {}

for dir_entry in os.listdir(path):
    dir_entry_path = os.path.join(path, dir_entry)
    if os.path.isfile(dir_entry_path):
        with open(dir_entry_path, 'r') as my_file:
            text = my_file.read()
            text = ' '.join([word for word in text.split() if word not in cachedStopWords])

            data[dir_entry] = text

for (filename, content) in data.items():
    f = open('./processed_nonstop/'+filename, 'w+')
    f.write(content)
    f.close()
