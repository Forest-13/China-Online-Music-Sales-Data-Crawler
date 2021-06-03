import os
import sys

# input and output
src_dir = './download_data'
dst_path = 'album_sale.csv'

data = []

names = os.listdir(src_dir)
name_num = len(names)
for idx, name in enumerate(names):
    # get path of source csv file
    src_path = os.path.join(src_dir, name)
    # get album_name and singer name
    info = ('.'.join(name.split('.')[:-1])).split('@')
    album = info[0].replace(',', '&#44;')
    singer = info[1].replace(',', '&#44;')
    # get nume of sale in 200 for each album
    num_2020 = 0
    sale_2020 = 0
    with open(src_path) as f:
        lines = f.readlines()
    for line in lines[1:]:
        time = line.split(',')[0]
        num_day = int(line.split(',')[1])
        sale_day = float(line.split(',')[2])
        if '2020' in time:
            num_2020 += num_day
            sale_2020 += sale_day
    # pack useful data
    data.append({'album': album, 'singer': singer, 'num_2020': num_2020, 'sale_2020': sale_2020})
    sys.stdout.write('\rRead album data %03d/%03d'%(idx+1, name_num))
# write csv file
with open(dst_path, 'w') as f:
    f.write('专辑,歌手,销量(张),销量(元)\n')
    for item in data:
        f.write('%s,%s,%d,%.2f\n'%(item['album'], item['singer'], item['num_2020'], item['sale_2020']))



        















