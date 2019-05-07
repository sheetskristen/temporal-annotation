
f_g = open('features_gold.txt')
f_s = open('features_silver.txt')
f_gs = open('features_all.csv', 'w')

f_gs.write(',type,event_timex,tlink_label\n')
lines = f_g.readlines()
index = 0
for line in lines:
    tokens = line.strip().split('\t')
    f_gs.write(str(index) + ','
               + 'gold' + ','
               + ' '.join(tokens[:-1]) + ','
               + tokens[-1] + '\n')
    index += 1
f_g.close()

lines = f_s.readlines()
for line in lines:
    tokens = line.strip().split('\t')
    f_gs.write(str(index) + ','
               + 'silver' + ','
               + ' '.join(tokens[:-1]) + ','
               + tokens[-1] + '\n')
    index += 1
f_s.close()
f_gs.close()
