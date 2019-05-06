import os

for root, dirs, files in os.walk('annotated_data'):
    for name in files:
        print(name)
        if '.txt' in name:
            with open(os.path.join(root, name)) as f:
                lst = list()
                relations = list()
                lines = f.readlines()
                for line in lines:
                    tokens = line.split()
                    if tokens[0] == 'EVENT' or tokens[0] == 'TIMEX':
                        tag = tokens[0]
                        text = tokens[1]
                        start = tokens[2]
                        end = tokens[3]
                        lst.append([int(text), int(start), int(end), tag])
                    if tokens[0] == 'TLINK':
                        tag1 = tokens[1]
                        text = tokens[2]
                        start1 = tokens[3]
                        end1 = tokens[4]
                        tag2 = tokens[5]
                        start2 = tokens[7]
                        end2 = tokens[8]
                        relations.append([int(text), int(start1), int(start2)])
                f_write = open(name, 'w')
                lst.sort()
                pre = None
                for cur in lst:
                    if pre is None:
                        pre = cur
                        continue
                    if pre[0] != cur[0]:
                        pre = cur
                        continue
                    if [pre[0], pre[1], cur[1]] not in relations:
                        line_unspecified = '\t'.join(['TLINK', pre[3], str(pre[0]), str(pre[1]), str(pre[2]), cur[3], str(cur[0]), str(cur[1]), str(cur[2]), 'unspecified'])
                        f_write.write(line_unspecified)
                        f_write.write('\n')
                    pre = cur
