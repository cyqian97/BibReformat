import re, os
from states import article,inproceedings,mastersthesis,phdthesis

temp = ''
push_to_temp = True
entry_list = []
old_bib_name = 'libraries//library.bib'
new_bib_name = 'libraries//library_new.bib'

with open(old_bib_name,'r') as fread:
    while True:
        c = fread.read(1)
        if not c:
            break
        if push_to_temp:
            temp = temp + c
        if re.search(r'@article', temp, flags=re.IGNORECASE):
            temp = ''
            entry_list.append(article(fread))
        elif re.search(r'@inproceedings', temp, flags=re.IGNORECASE):
            temp = ''
            entry_list.append(inproceedings(fread))
        elif re.search(r'@mastersthesis', temp, flags=re.IGNORECASE):
            temp = ''
            entry_list.append(mastersthesis(fread))
        elif re.search(r'@phdthesis', temp, flags=re.IGNORECASE):
            temp = ''
            entry_list.append(phdthesis(fread))

with open(new_bib_name,'w') as fwrite:
    title_list = []
    for entry in entry_list:
        title_list.append(entry.content_dict['title'].lower())
    for title in title_list:
        if title_list.count(title) > 1:
            print('"'+title+'"'+' has multiple citations!')
    for entry in entry_list:
        entry.write_bib(fwrite)


