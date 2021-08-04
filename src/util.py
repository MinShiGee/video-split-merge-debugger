import os
import time
from . import ffmpeg_module as ffmpeg
from sys import hash_info

media_locate = './src/media/'
merge_meta_to_media_url = '../media/'
media_numbering_suffix = '_@'

def make_job_code() -> str:
    now = time.localtime()
    return "%04d_%02d_%02d_%02d_%02d_%02d" % (
        now.tm_year, 
        now.tm_mon, 
        now.tm_mday, 
        now.tm_hour, 
        now.tm_min, 
        now.tm_sec
    )

def make_url(name:str) -> str:
    global media_locate
    url = media_locate + name
    return url

def parse_url(url:str):
    '''
    return tuple(파일이름,파일확장자,경로)
    ex: ('sample', 'mp4', './src/media/')
    '''
    global media_numbering_suffix
    parsed_url = url.split('/')
    name_code = parsed_url[-1].split('.')
    name = name_code[0]
    code = name_code[1]
    return (name,code,''.join(['{}/'.format(data) for data in parsed_url[:-1]]))

def make_numbering_name(url:str, num:int) ->str:
    url_data = parse_url(url)
    res_url = '{}{}{}{}.{}'.format(url_data[2],url_data[0],media_numbering_suffix,num,url_data[1])
    return res_url

def make_merged_url(src_url:str, job_code:str) -> str:
    parsed_url = parse_url(src_url)
    merged_url = parsed_url[2] + parsed_url[0] + '_M@' + job_code + '.' + parsed_url[1]
    return merged_url

def make_vaild_time(time:str):
    '''
    todo parsing time data
    '''
    #time = '\'{}\''.format(time)
    return time

def make_divided_media_list(url:str):
    global media_numbering_suffix
    parsed_url = parse_url(url)
    filename = parsed_url[0] + media_numbering_suffix
    all_files:list = os.listdir(media_locate)
    files:list = [name for name in all_files if name.startswith(filename)]
    return files

def remove_legacy_media_files(url:str):
    global media_locate
    legacy_list = make_divided_media_list(url)
    for name in legacy_list:
        loc = media_locate + name
        os.remove(loc)

def write_merge_medium_txt(src_url:str, merging_section:list):
    global merge_meta_to_media_url
    if merging_section == None:
        merging_section = make_divided_media_list(src_url)
    else:
        pass
    merging_section = ['{}{}'.format(merge_meta_to_media_url, name) for name in merging_section]
    parsed_url = parse_url(src_url)
    job_code = make_job_code()
    filename = './src/merge_meta/' + parsed_url[0] + '_out{}_'.format(len(merging_section)) + job_code + '.txt'
    file = open(filename, "w")
    for url in merging_section:
        data = 'file \'{}\'\n'.format(url)
        file.write(data)
    file.close()
    return (filename, job_code)

def write_gop_info_text(filename:str):
    f = open('./src/log/{}_@gop_log.txt'.format(filename), "w")
    data = ['{} {}\n'.format(i, pic) for i, pic in enumerate(ffmpeg.get_gop_info(make_url(filename)))]
    f.write(''.join(data))
    f.close()

def compare_gop_info_txt(meta:str, filename1:str, filename2:str) -> bool:
    f1_data = ffmpeg.get_gop_info(make_url(filename1))
    f2_data = ffmpeg.get_gop_info(make_url(filename2))
    diff = ''
    diff_cnt = 0
    gap = len(f1_data) - len(f2_data)
    if gap < 0:
        f1_data += [None for _ in range(abs(gap))]
    else:
        f2_data += [None for _ in range(gap)]

    for i, d1, d2 in zip(range(len(f1_data)), f1_data, f2_data):
        if d1 == d2:
            continue
        diff += 'frame: {}, ori-pic: {}, mer-pic: {}\n'.format(i,d1,d2)
        diff_cnt += 1

    f = open('./src/comp/{}_C@{}.txt'.format(filename1,filename2),"w")
    f.write(meta + diff + '\ndiff-cnt : {}'.format(diff_cnt))
    f.close()
    return diff == ''

def init_log():
    f = open('log.txt','w')
    f.close()

def append_log(line:str):
    f = open('log.txt',"a")
    f.write(line + '\n')
    f.close()