import re
import os
from xml.etree import ElementTree as ET

re_unitid = re.compile('(<UNIT_ID=")(.*?)(">)')


for fn in os.listdir('annotated_data'):
    if not fn.endswith('.xml'):
        continue
    uids = []
    xml = ET.parse(fn)
    root = xml.getroot()
    text = root.find('TEXT')
    tags = root.find('TAGS')
    for match in re_unitid.finditer(text.text):
        pos = match.start(2)
        uid = match.group(2)
        uids.append((pos, uid))
    anno = []
    id_dict = {}
    for tag in tags.iter():
        label = tag.tag
        if label == 'TLINK':
            continue
        if label == 'TAGS':
            continue
        span_start, span_end = tag.attrib['spans'].split('~')
        tag_id = tag.attrib['id']
        start = int(span_start)
        end = int(span_end)
        pre_pos = 0
        pre_uid = ''
        for pos, uid in uids:
            if pos > start:
                break
            else:
                pre_pos = pos
                pre_uid = uid
        anno.append((label, pre_uid, start-pre_pos, end-pre_pos))
        id_dict[tag_id] = (label, pre_uid, start-pre_pos, end-pre_pos)
    tlinks = []
    for tag in tags.iter():
        label = tag.tag
        if label != 'TLINK':
            continue
        try:
            from_id = tag.attrib['fromID']
            to_id = tag.attrib['toID']
            for attr in tag.attrib:
                if attr in ("overlap", "after", "unrealized", "before"):
                    break
            else:
                attr = "unspecified"
            tlinks.append((*id_dict[from_id], *id_dict[to_id], attr))
        except:
            pass
    with open(fn[-10:-4] + '.txt', 'w') as fo:
        for a in anno:
            fo.write('%s\t%s\t%s\t%s\n'% a)
        for t in tlinks:
            fo.write('TLINK\t')
            fo.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'% t)





