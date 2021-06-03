import os
import sys


def filter_year(src_path, dst_path, year):
    with open(src_path, 'r') as src_f:
        lines = src_f.readlines()
    dst_f = open(dst_path, 'w')
    for line_idx, line in enumerate(lines):
        if line_idx == 0 or year in line:
            dst_f.write(line)
    dst_f.close()

if __name__ == '__main__':
    src_dir = 'download_data'
    dst_dir = '2020'
    year = '2020'
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    names = os.listdir(src_dir)
    name_num = len(names)
    for name_idx, name in enumerate(names):
        src_path = os.path.join(src_dir, name)
        dst_path = os.path.join(dst_dir, name)
        filter_year(src_path, dst_path, year)
        sys.stdout.write('\rFilter data by the year %s, save in directory \"%s\": %04d/%04d'%(year, dst_dir, name_idx+1, name_num))
    print()


