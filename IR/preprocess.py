import os
path = r'./Presidents'  # remove the trailing '\'
data = {}
for dir_entry in os.listdir(path):
    dir_entry_path = os.path.join(path, dir_entry)
    if os.path.isfile(dir_entry_path):
        with open(dir_entry_path, 'r') as my_file:
            original_file = my_file.read()
            proc_file = original_file.replace('\n',' ') # remove newline
            proc_file = proc_file.replace(',',' ') # remove comma
            proc_file = proc_file.replace('"', ' ') # remove double qoute
            proc_file = proc_file.replace(".", ' ') # remove period
            proc_file = proc_file.replace(":", ' ') # remove period
            proc_file = " ".join(proc_file.split())

            data[dir_entry] = proc_file

for (filename, content) in data.items():
    f = open('./processed/'+filename, 'w+')
    f.write(content)
    f.close()

