from statsmodels.stats.inter_rater import fleiss_kappa
import numpy as np
import re

re_unitid = re.compile('(<UNIT_ID=")(.*?)(">)')

files = ['NEWS-1_1-DD.xml', 'NEWS-1_1-EF.xml', 'NEWS-1_1-LC.xml',
         'NEWS-BATCH-10_1-EF.xml', 'NEWS-BATCH-2_1-EF.xml',
         'NEWS-BATCH-3_1-EF.xml', 'NEWS-BATCH-4_1-EF.xml', 'NEWS-BATCH-4_1-LC.xml',
         'NEWS-BATCH-5_1-EF.xml', 'NEWS-BATCH-5_1-LC.xml', 'NEWS-BATCH-6_1-EF.xml',
         'NEWS-BATCH-7_1-EF.xml', 'NEWS-BATCH-8_1-EF.xml', 'NEWS-BATCH-9_1-EF.xml']

news_dict = {f: set() for f in files}

for f in files:
    data = open(f).read()
    for match in re_unitid.findall(data):
        uid = match[1]
        news_dict[f].add(uid)

DD_news = set()
for f in files:
    if f.endswith("DD.xml"):
        DD_news = DD_news.union(news_dict[f])

LC_news = set()
for f in files:
    if f.endswith("LC.xml"):
        LC_news = LC_news.union(news_dict[f])

EF_news = set()
for f in files:
    if f.endswith("EF.xml"):
        EF_news = EF_news.union(news_dict[f])

all_news = DD_news & LC_news & EF_news
all_news.remove('_unit_id')
# print(all_news)

tlinks = {}
IDX = {'overlap': 0, 'after':1, 'unrealized':2, 'before':3, 'unspecified':4}
events = {}
timexs = {}
for line in open('all.txt'):
    e = line.strip('\n').split('\t')
    if e[0] == 'EVENT' and e[1] in all_news:
        eid = e[1] + e[2] + e[3]
        events[eid] = events.get(eid, 0) + 1
    elif e[0] == 'TIMEX' and e[1] in all_news:
        tid = e[1] + e[2] + e[3]
        timexs[tid] = timexs.get(tid, 0) + 1
    elif e[0] == 'TLINK' and e[2] in all_news:
        lid = e[2] + e[3] + e[4] + e[7] + e[8]
        if lid not in tlinks:
            tlinks[lid] = [0, 0, 0, 0, 0, 0]
        tlinks[lid][IDX[e[9]]] += 1

event_table = np.array([(events[i], 3 - events[i]) for i in events])
# print(event_table)

timex_table = np.array([(timexs[i], 3 - timexs[i]) for i in timexs])
# print(timex_table)

tlink_table = np.array([tlinks[i] for i in tlinks])
tlink_table[:, 5] = 3 - tlink_table.sum(axis=1)
# print(tlink_table)


print("Agreement score for EVENT tags:")
print(fleiss_kappa(event_table))
print("Agreement score for TIMEX tags:")
print(fleiss_kappa(timex_table))
print("Agreement score for TLINK tags:")
print(fleiss_kappa(tlink_table))
