import re
from copy import deepcopy


#
class entry():
    # Basic entry class
    def __init__(self, fread):
        # self.start = fread.tell()

        # Head for a certain entry type
        self.head = ''

        # List of required items
        self.item_list = []

        # Preliminarily parse the content of this entry
        while True:
            c = fread.read(1)
            if not c:
                break
            if c == '{':
                self.content = curly_processor(fread)
                break
        content_replace(self.content, ['\n', '\t'])
        content_replace(self.content, [r'\s\s+'], tar=' ')

        # Further parse the content into an dictionary
        self.content_dict = {}
        self.content_dict['citation_key'] = self.content[0][1:].split(',')[0].strip()
        key = self.content[0][1:].split(',')[1].replace('=', '').strip().lower()
        value = self.content[1][0][1:-1].strip()
        self.content_dict[key] = value
        i = 2
        while i < len(self.content) - 1:
            key = self.content[i].replace(',', '').replace('=', '').strip().lower()
            i += 1
            value = self.content[i][0][1:-1].strip()
            i += 1
            self.content_dict[key] = value

    def write_bib(self, fwrite):
        fwrite.write(self.head + '{' + self.content_dict['citation_key'] + ',\n')
        for item in self.item_list[:-1]:
            if item in self.content_dict:
                fwrite.write('\t' + item + ' = {' + self.content_dict[item] + '},\n')
            else:
                fwrite.write('\t' + item + ' = {},\n')
        item = self.item_list[-1]
        if item in self.content_dict:
            fwrite.write('\t' + item + ' = {' + self.content_dict[item] + '}}\n\n')
        else:
            fwrite.write('\t' + item + ' = {}}\n\n')


class article(entry):
    def __init__(self, fread):
        super().__init__(fread)
        self.head = '@article'
        self.item_list = ['author', 'journal', 'title', 'volume', 'number', 'pages', 'month', 'year']


class inproceedings(entry):
    def __init__(self, fread):
        super().__init__(fread)
        self.head = '@inproceedings'
        self.item_list = ['author', 'booktitle', 'title', 'volume', 'number', 'pages', 'month', 'year','address']


class mastersthesis(entry):
    def __init__(self, fread):
        super().__init__(fread)
        self.head = '@mastersthesis'
        self.item_list = ['author','title','school','year']


class phdthesis(entry):
    def __init__(self, fread):
        super().__init__(fread)
        self.head = '@phdthesis'
        self.item_list = ['author','title','school','year']


def curly_processor(fread, depth = 2):
    content = [r'{']
    current_section = 0
    if depth > 1:
        while True:
            c = fread.read(1)
            if not c:
                return content
            if c == '}':
                content[current_section] += c
                return content
            if c == '{':
                content.append(curly_processor(fread,depth = depth - 1))
                content.append(r'')
                current_section += 2
            else:
                content[current_section] += c
    else:
        count_left = 1
        count_right = 0
        while True:
            c = fread.read(1)
            if not c:
                return content
            content[current_section] += c
            if c == '}':
                count_right += 1
                if count_right == count_left:
                    return content
            if c == '{':
                count_left += 1



def content_replace(content, chars, tar=''):
    for idx, item in enumerate(content):
        if type(item) == str:
            for ch in chars:
                # content[idx] = content[idx].replace(ch,tar)
                content[idx] = re.sub(ch, tar, content[idx])
        else:
            content_replace(content[idx], chars, tar=tar)
