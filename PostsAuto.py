import os
import shutil

source_pdf_path = 'C:/Users/wenychan/Desktop/pdf'
target_pdf_path = 'C:/GitHub/wenyuchang.github.io/pdf/'
target_md_path = 'C:/GitHub/wenyuchang.github.io/_posts/%s'

for root, dirs, files in os.walk(source_pdf_path):
    for f in files:
        if f.endswith('pdf'):
            name = f.split('.')
            time = '%s-%s-%s-' % (name[0][:4], name[0][4:6], name[0][6:8])
            name[0] = name[0][8:]
            print name[0]
            f_o_name = name[0]
            name[0] = name[0].replace(' ', '-')
            f_name = name[0].replace('-', '')
            name = '.'.join(name)
            shutil.copy(os.path.join(root, f), os.path.join(target_pdf_path, name))

            content = '''---
layout: post
date: [[date]]
title: [[title]]
docurl: /pdf/[[path]]
---

[[path]]'''

            post_f_name = '%s%s.md' % (time, f_name)
            content = content.replace('[[date]]', time[:-1])
            content = content.replace('[[title]]', f_o_name)
            content = content.replace('[[path]]', name)
            f = open(target_md_path % post_f_name, 'w+')
            f.write(content)
            f.close()
    break