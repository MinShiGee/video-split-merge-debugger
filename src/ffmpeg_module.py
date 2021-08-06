import os
from . import constant as const
import threading
import subprocess
from . import util

video_rate = None
print_log = False

def get_frame_info(url:str = './src/media/test.mp4') -> list:
    res : str = str(
        subprocess.check_output("ffprobe -select_streams v -show_frames -show_entries frame -of csv {}".format(url), shell=True)
    ).split('\\r\\n')
    return res

def split_media_section(code:str):
    os.system(code)

def split_media(name:str, sections:list):
    head_frame_list = [0] + sections
    tail_frame_list = sections + [None]
    codes = []
    for i, head, tail, in zip(range(len(head_frame_list)), head_frame_list, tail_frame_list):
        start_time = None
        frame_cnt = None
        if head != 0:
            start_time = head / video_rate
        if tail != None:
            frame_cnt = tail - head
        code = util.make_split_code(name, i, start_time, frame_cnt)
        codes.append(code)

    jobs = [threading.Thread(target=split_media_section, args=([code]), daemon=True) for code in codes]
    for job in jobs:
        job.start()
    for job in jobs:
        job.join()
    
    util.append_log('\n======Split Code======\n')
    for code in codes:
        util.append_log(code)
    return

def merge_media(name:str, sections:list) -> list:
    '''
    arr[3] = [merge_media_name, merge_txt_name, job_code]
    '''

    sections = util.get_merge_url_list(name, sections)
    media_data = util.write_merge_text(name,sections)
    merge_media_name = media_data[0]
    merge_txt_name = media_data[1]
    code = util.make_merge_code(merge_txt_name,merge_media_name)
    os.system(code)

    util.append_log('\n======Merge Urls======\n')
    for url in sections:
        util.append_log(url)
    
    util.append_log('\n======Merge Code======\n')
    util.append_log(code)
    return media_data

def excute_draw_text(loc:str,name:str,pos:int) -> str:
    url = loc + name
    tmp = name.split('.')
    url2 = loc + tmp[0] + '_F.' + tmp[1]
    code = 'ffmpeg -y -i {} -vf \"drawtext=fontfile=Arial.ttf: text=\'%{}{}{}\': '.format(url,'{','frame_num','}')
    code += 'start_number=1: x=(w-tw)/2: y=h-({}*lh): '.format(pos)
    code += 'fontcolor=black: fontsize=80: box=1: boxcolor=yellow: boxborderw=5\" -c:a copy {}'.format(url2)
    os.system(code)
    return code
