import os
import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
path = r'./Presidents'  # remove the trailing '\'
data = {}
lmtzr = WordNetLemmatizer()
cachedStopWords = stopwords.words('english')

def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]+',' ', text)

for dir_entry in os.listdir(path):
    dir_entry_path = os.path.join(path, dir_entry)
    if os.path.isfile(dir_entry_path):
        with open(dir_entry_path, 'r') as my_file:
            original_file = my_file.read()
            proc_file = original_file.replace('\n',' ') # remove newline
            proc_file = proc_file.replace(',',' ') # remove comma
            proc_file = proc_file.replace('"', ' ') # remove double qoute
            proc_file = proc_file.replace(".", ' ') # remove period
            proc_file = proc_file.replace(":", ' ') # remove colon
            proc_file = proc_file.replace("--", ' ') #
            proc_file = remove_non_ascii_2(proc_file) # illegal character
            proc_file = ' '.join([word for word in proc_file.split() if word not in cachedStopWords])
            # proc_file = proc_file.decode('utf-8')
            words = proc_file.split()
            words = [lmtzr.lemmatize(word) for word in words] # lemmatize

            proc_file = " ".join(words)
            proc_file = proc_file.lower()

            data[dir_entry] = proc_file

for (filename, content) in data.items():
    f = open('./processed_nonstop/'+filename, 'w+')
    f.write(content)
    f.close()

