import os
from . import constant as const
import threading
from . import util

def split_media_section(code:str):
    os.system(code)

def split_media(name:str, sections:list):
    head_frame_list = [1] + sections
    tail_frame_list = sections + [None]
    codes = []
    util.append_log('\n\n==========split_times==========')
    for i, head, tail, in zip(range(len(head_frame_list)), head_frame_list, tail_frame_list):
        delta = const.delta_timestamp[const.config['video_rate']]
        start_time = (head-1) * delta
        end_time = None
        frame_count = None
        if head > 1:
           start_time -= delta / 2
        if tail != None:
            end_time = (tail - 1) * delta - delta / 2
            frame_count = tail - head
        util.append_log('head = {},  start_time = {}, end_time {}'.format(head,start_time,end_time))
        code = util.make_split_code(name, i, start_time, end_time, frame_count)
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
