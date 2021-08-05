from collections import defaultdict
from typing import List
import threading
import os
from . import ffmpeg_module as ffmpeg
from . import util
from . import constant as const

check_list = ['filename','video_rate','split_sections','merge_sections']
dir_list = [
        const.src_url,
        const.cut_url,
        const.log_url,
        const.merge_txt_url,
        const.merge_media_url
]

def run_app(config: defaultdict(None)):

    if config['remove_legacy_files'] ==True:
        util.remove_legacy_files(dir_list[1:])

    for check_key in check_list:
        if config[check_key] == None:
            print('Config Error. check key = {}'.format(check_key))
            return

    job:threading.Thread = None
    if config['src_draw_text'] == True:
        job = threading.Thread(target=ffmpeg.excute_draw_text, args=[const.src_url,config['filename'],3],daemon=True)
        job.start()
        if config['use_after_draw_text'] == True:
            job.join()
            config['filename'] = util.make_drawtext_name(config['filename'])
            job = None

    util.init_log()
    setup(config)

    if config['split'] == True:
        ffmpeg.split_media(config['filename'], config['split_sections'])
    if config['merge'] == True:
        ffmpeg.merge_media(config['filename'], config['merge_sections'])
    if config['print_log'] == True:
        pass
    
    if job != None:
        job.join()

    return

def setup(config:dict):
    make_dir()
    ffmpeg.video_rate = const.video_rate[config['video_rate']]
    write_log_header(config)
    return
    
def make_dir():
    util.print_header_line('make directory')
    
    for dir in dir_list:
        try:
            os.mkdir(dir)
            print('make dir : {}'.format(dir))
        except:
            print('check dir : {}'.format(dir))
    return

def write_log_header(config:dict):
    util.append_log('<log-header>')
    util.append_log('file_name = ' + str(config['filename']))
    util.append_log('video_rate = ' + str(ffmpeg.video_rate))
    if config['split'] == True:
        data = ''.join([str(d) +', ' for d in config['split_sections']])
        util.append_log('split_secton = {}'.format(data))
    util.append_log('########################################')
    return