import re
"""
Recover two entities in the tlink tags and add their context words (winder of 2)
Output: C-2, C-1, W1, C+1, C+2, C-2, C-1, W2, C+1, C+2, target label
"""

re_unitid = re.compile('(<UNIT_ID=")(.*?)(">)')


tlinks = []
f = open("annotated_data/gold.txt", encoding='utf-8')
for line in f:
    if line.startswith('TLINK'):
        tag = line.strip('\n').split('\t')
        tlinks.append(tag)
# print(tlinks)

uid2idx = {}

data = open("ECON-NEWS-1.xml").read()
for match in re_unitid.finditer(data):
    pos = match.start(2)
    uid = match.group(2)
    uid2idx[uid] = pos

def previous2(text, start):
    space = 0
    left = start
    while space < 3:
        if text[left-1] in '><:.,!?':
            break
        if text[left-1] == ' ':
            space += 1
        left -= 1
    substr = text[left:start].lower()
    if space == 0:
        return '*start*', '*start*'
    if space == 1:
        return '*start*', substr.strip(' ')
    if space in (2, 3):
        x = substr.strip(' ').split(' ')
        return ['*start*'] * (2-len(x)) + x

def next2(text, end):
    space = 0
    right = end-1
    while space < 3:
        if text[right+1] in '><:.,!?':
            break
        if text[right+1] == ' ':
            space += 1
        right += 1
    substr = text[end:right+1].lower()
    # print(substr, space)
    if space == 0:
        return '*end*', '*end*'
    if space == 1:
        return substr.strip(' '), '*end*'
    if space in (2, 3):
        x = substr.strip(' ').split(' ')
        return x + (2 - len(x)) * ['*end*']


with open("features.txt", "w") as fo:
    for tag in tlinks:
        uid = tag[2]
        first_start = int(tag[3]) + uid2idx[uid]
        first_end = int(tag[4]) + uid2idx[uid]
        second_start = int(tag[7]) + uid2idx[uid]
        second_end = int(tag[8]) + uid2idx[uid]
        target = tag[9]
        w1 = data[first_start: first_end].lower()
        w1p = previous2(data, first_start)
        w1n = next2(data, first_end)
        w2 = data[second_start: second_end].lower()
        w2p = previous2(data, second_start)
        w2n = next2(data, second_end)
        fo.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%
                 (w1p[0], w1p[1], w1, w1n[0], w1n[1], w2p[0], w2p[1], w2, w2n[0], w2n[1], target))

