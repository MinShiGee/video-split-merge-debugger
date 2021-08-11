import os
from src import app
import time
import shutil
from typing import Text
from . import ffmpeg_module as ffmpeg
from . import constant as const

def make_splited_num_name(name:str, num:int) -> str:
    tmp = name.split('.')
    number_name = tmp[0] + const.cut_name_parse_code + str(num) + '.' + tmp[1]
    return number_name

def make_drawtext_name(name:str):
    tmp = name.split('.')
    return tmp[0] + '_F.' + tmp[1]

def make_split_code(src_name:str, num:int, start_time:float = None, end_time:float = None, frame_count:int = None) -> str:
    code = 'ffmpeg -y '
    code += '-ss {} '.format(start_time, end_time) 
    if end_time != None:
        code += '-to {} '.format(end_time)
    code += ' -i {} '.format(const.src_url + src_name)
    code += '-an '.format(const.video_rate[const.config['video_rate']])
    if frame_count != None:
        code += '-frames {} -vf "setpts=PTS-STARTPTS" '.format(frame_count)
    code += '{}'.format(const.cut_url + make_splited_num_name(src_name, num))
    return code

def get_number_from_number_name(name:str) -> int:
    res = -1
    try:
        res = name.split(const.cut_name_parse_code)[-1].split('.')[0]
    except:
        pass
    return int(res)

def get_merge_url_list(name:str, sections:list) -> list:
    is_all = 'all' in sections
    name_data = name.split('.')
    inv_files = [
        n 
        for n 
        in os.listdir(const.cut_url) 
        if n.startswith(name_data[0] + const.cut_name_parse_code) 
        and (is_all or get_number_from_number_name(n) 
        in sections)
    ]
    inv_files.sort(key=lambda k:get_number_from_number_name(k))
    return inv_files

def make_merge_code(src_txt:str, out_name:str) -> str:
    code = 'ffmpeg -f concat -safe 0 -i {} -c copy {}'.format(const.merge_txt_url + src_txt, const.merge_media_url + out_name)
    return code

def make_merge_names(src_name:str, code:str):
    name_data = src_name.split('.')
    only_txt_name = name_data[0] + const.merged_media_parse_code + code
    merge_media_name = only_txt_name + '.' + name_data[-1]
    only_txt_name += '.txt'
    res = [merge_media_name, only_txt_name]
    return res

def write_merge_text(src_name:str, names:list) -> list:
    code = make_job_code()
    name_data = make_merge_names(src_name, code)
    f = open('{}'.format(const.merge_txt_url + name_data[1]), "w")
    for data in names:
        f.write('file \'{}\'\n'.format(const.rel_to_cut_media + data))
    f.close()

    res = [name_data[0], name_data[1], code]
    return res 

def remove_legacy_files(urls:list):
    for url in urls:
        try:
            files = os.listdir(url)
            for file in files:
                os.remove(url + file)
        except:
            pass
    return

def make_filename_to_logurl(name:str, code:str):
    name_data = name.split('.')
    url = const.log_url + name_data[0] + '_L' + code + '.txt'
    return url

def copy_log(url:str):
    shutil.copyfile('log.txt', url)
    return

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

def write_frame_info_text(src_url:str):
    url_data = src_url.split('/')
    out_url = './src/log/{}_@frame_log.txt'.format(url_data[-1])
    os.system('ffprobe -select_streams v -show_frames -show_entries frame -of csv {} >> {}'.format(src_url, out_url))

def write_gop_info_text(src_url:str):
    url_data = src_url.split('/')
    out_url = './src/log/{}_@gop_log.txt'.format(url_data[-1])
    os.system('ffprobe -select_streams v -show_frames -show_entries frame=pict_type -of csv {} >> {}'.format(src_url, out_url))

def compare_frame_info_txt(meta:str, filename1:str, filename2:str) -> bool:
    f1_data = open('./src/log/{}_@frame_log.txt'.format(filename1),"r").read().split('\n')
    f2_data = open('./src/log/{}_@frame_log.txt'.format(filename2),"r").read().split('\n')
    meta += '\n{}\n{}\n\n'.format(filename1, filename2)
    diff = '=====diff_data=====\n\n'
    err_log = '=====err_log=====\n\npass_line = [\n'
    pass_line = []

    comp_str = open('./src/comp_list.txt',"r").read().replace('\n\n','\n') .split('\n')
    _fr = 0
    _i1 = 0
    _i2 = 0
    while len(f1_data) > _i1 and len(f2_data) > _i2:
        while len(f1_data) > _i1 and len(f1_data[_i1]) < 5:
            _i1 += 1
            pass_line.append('  src_log : {}\n'.format(_i1))
        while len(f2_data) > _i2 and len(f2_data[_i2]) < 5:
            _i2 += 1
            pass_line.append('  merge_log : {}\n'.format(_i2))
        _fr += 1
        d1 = [None for _ in range(30)]
        d2 = [None for _ in range(30)]
        if len(f1_data) > _i1:
            d1 = f1_data[_i1].split(',')
        if len(f2_data) > _i2:
            d2 = f2_data[_i2].split(',')
        diff += 'frame: {}\n'.format(_fr)
        for k,a,b in zip(comp_str,d1,d2):
            if a == b:
                continue
            diff += '{} {},{}\n'.format(k,a,b)
        diff += '\n'
        _i1 += 1
        _i2 += 1

    err_log += ''.join(pass_line) + ']\n\n'
    f = open('./src/log/{}_C@{}.txt'.format(filename1,filename2),"w")
    f.write(meta + err_log + diff)
    f.close()
    return diff == ''

def print_block_line():
    print('########################################')
    return

def print_header_line(line:str):
    print_block_line()
    print(line)
    print_block_line()
    return

def init_log():
    f = open('log.txt','w')
    f.close()

def append_log(line:str):
    f = open('log.txt',"a")
    f.write(line + '\n')
    f.close()

def write_log_block_line():
    append_log('########################################')