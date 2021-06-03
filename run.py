import os
import sys

'''
1. 下载首页的网页，确定总的表格页数
2. 下载每一页的表格，拿到专辑名字与id的对应关系
3. 有了id就可以下载每个专辑的每日数据，专辑名字+歌手名作为命名
'''

def get_page_num(path='homepage.txt'):
    with open(path, 'r') as f:
        contents = f.read()
    page_num = contents.count('?page=')
    return page_num


def download_table_page(page_num, prefix='http://y.saoju.net/szzj/?page='):
    table_page_path_list = []
    for page_idx in range(1, page_num+1):
        url = prefix+str(page_idx)
        path = 'tablepage_'+str(page_idx)+'.txt'
        os.system('wget -q %s -O %s'%(url, path))
        sys.stdout.write('\rDownloading pages of the album table (http://y.saoju.net/szzj/?page=%s): %02d/%02d'%(page_idx, page_idx+1, page_num))
        table_page_path_list.append(path)
    print()
    return table_page_path_list

def get_album_artist_list(table_page_path_list):
    album_artist_list = []
    for table_page_path in table_page_path_list:
        with open(table_page_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if "/szzj/album/" in line and "/szzj/artist/" in line:
                album_id = line.split('\"')[1].split('/')[3]
                artist_id = line.split('\"')[5].split('/')[3]
                album_name = line.split('>')[1].split('<')[0]
                artist_name = line.split('>')[3].split('<')[0]
                album_artist_list.append([album_id, album_name.replace('/', '&'), artist_id, artist_name.replace('/', '&')])
    return album_artist_list

def clear():
    os.system('rm homepage.txt')
    os.system('rm tablepage_*')


if __name__ == "__main__":
    # download first page
    os.system('wget -q http://y.saoju.net/szzj/ -O homepage.txt')
    print('Downloading the home page (http://y.saoju.net/szzj/)')
    # get page number of table
    page_num = get_page_num()
    # download table pages
    table_page_path_list = download_table_page(page_num)
    album_artist_list = get_album_artist_list(table_page_path_list)
    # download data csv
    download_dir = 'download_data/'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    album_num = len(album_artist_list)
    for idx, album_artist in enumerate(album_artist_list):
        album_id, album_name = album_artist[0], album_artist[1]
        artist_id, artist_name = album_artist[2], album_artist[3]
        download_path = os.path.join(download_dir, '%s@%s.csv'%(album_name, artist_name))
        os.system('wget -q http://y.saoju.net/szzj/album/%s/daily -O \"%s\"'%(album_id, download_path))
        sys.stdout.write('\rDownloading the daily sale data into directory \"%s\": %04d/%04d '%(download_dir, idx+1, album_num))
    # clear()







