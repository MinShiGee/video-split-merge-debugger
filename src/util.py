import os
import time
from . import ffmpeg_module as ffmpeg
from . import constant as const

def make_splited_num_name(name:str, num:int) -> str:
    tmp = name.split('.')
    number_name = tmp[0] + const.cut_name_parse_code + str(num) + '.' + tmp[1]
    return number_name

def make_drawtext_name(name:str):
    tmp = name.split('.')
    return tmp[0] + '_F.' + tmp[1]

def make_split_code(src_name:str, num:int, start_time:float = None, frame_cnt:int = None) -> str:
    code = 'ffmpeg -y '
    if start_time != None:
        code += '-ss {} '.format(start_time)
    code += '-i {} '.format(const.src_url + src_name)
    code += '-c:v libx264 -an '
    if frame_cnt != None:
        code += '-frames {} '.format(frame_cnt)
    code += '{}'.format(const.cut_url + make_splited_num_name(src_name, num))
    return code

def get_number_from_number_name(name:str) -> int:
    res = None
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
    return inv_files

def make_merge_code(src_txt:str, out_name:str) -> str:
    code = 'ffmpeg -f concat -safe 0 -i {} -c copy {}'.format(const.merge_txt_url + src_txt, const.merge_media_url + out_name)
    return code

def write_merge_text(src_name:str, names:list) -> list:
    code = make_job_code()
    name_data = src_name.split('.')
    only_txt_name = name_data[0] + const.merged_media_parse_code + code
    merge_media_name = only_txt_name + '.' + name_data[-1]
    only_txt_name += '.txt'
    f = open('{}'.format(const.merge_txt_url + only_txt_name), "w")
    for data in names:
        f.write('file \'{}\'\n'.format(const.rel_to_cut_media + data))
    f.close()
    
    res = [merge_media_name, only_txt_name]
    return res 

def remove_legacy_files(urls:list):
    for url in urls:
        files = os.listdir(url)
        for file in files:
            os.remove(url + file)
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