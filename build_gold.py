import os

DD = []
LC =[]
EF = []

path = os.getcwd()

for root, dirs, files in os.walk(path):
    for f in files:
        name = f[4:6]
        fi = open(os.path.join(root, f), "r", encoding='utf-8')
        if name == 'DD':
            for line in fi:
                DD.append(line)
        elif name == 'LC':
            for line in fi:
                LC.append(line)
        elif name == 'EF':
            for line in fi:
                EF.append(line)

all = DD + LC + EF
print(len(all))
# print(*all)
with open('all.txt', 'w') as f:
    for t in all:
        f.write(t)

gold = set((set(DD) & set(LC)) | (set(DD) & set(EF)) | (set(LC) & set(EF)))
print(len(gold))
# print(*gold)
with open('gold.txt', 'w') as f:
    for t in gold:
        f.write(t)

silver = set(all)
print(len(silver))
# print(*silver)
with open('silver.txt', 'w') as f:
    for t in silver:
        f.write(t)



