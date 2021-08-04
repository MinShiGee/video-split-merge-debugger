from . import util
import os
import threading
import subprocess

import src

def get_gop_info(url:str = './src/media/sample.mp4', name:str = None) -> list:
    if name != None:
        url = util.make_url(name)
    res : str = str(
        subprocess.check_output("ffprobe -select_streams v -show_frames -show_entries frame=pict_type -of csv {}".format(url), shell=True)
    ).split('\\r\\n')
    res = [res[0][8]] + [
            frame[6] 
            for frame in res 
            if len(frame.split(',')) > 0 and frame[0] == 'f'
    ]
    return res

def get_media_endtime(url:str):
    end_time = str(subprocess.check_output('ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(url), shell=True))[2:-5]
    return end_time

def get_media_timestamp_info(url:str = './src/media/sample.mp4', name:str = None):
    if name != None:
        url = util.make_url(name)
    res : str = str(subprocess.check_output('ffprobe -f lavfi -i "movie={}" -show_frames -show_entries frame=pkt_pts_time -of csv=p=0'.format(url), shell=True)).split('\\r\\n')
    end_time = [get_media_endtime(url)]
    res = ['0.000000'] + res[1:-1] + end_time
    util.append_log('time_list_length = ' + str(len(res)))
    util.append_log('end_time = ' + end_time[0])
    return res

def split_media_section(input_url:str, output_url:str, start_time:float, end_time:float):
    code = 'ffmpeg -y -ss {} -t {} -i {} -c:v copy {}'.format(start_time,end_time,input_url,output_url)
    os.system(code)
    parsed_url = util.parse_url(output_url)
    print("##################################\n\n\n {} \n\n\n".format(code))
    util.write_gop_info_text('{}.{}'.format(parsed_url[0],parsed_url[1]))

def split_media(src_url:str, sections:list):
    output_url = src_url
    frame_time_list = get_media_timestamp_info(src_url)
    media_frame_count = len(frame_time_list)
    
    start_frame_list = [0] + sections
    end_frame_list = sections + [media_frame_count - 1]

    util.remove_legacy_media_files(src_url)
    threads = [
        threading.Thread(
            target=split_media_section, 
            args=(
                src_url, 
                util.make_numbering_name(output_url,num),
                util.make_vaild_time(frame_time_list[start_frame_num]),
                float(util.make_vaild_time(frame_time_list[end_frame_num])) - float(util.make_vaild_time(frame_time_list[start_frame_num]))), 
                daemon=True,
            )
        for num, start_frame_num, end_frame_num 
        in zip(
            range(len(end_frame_list)), 
            start_frame_list, 
            end_frame_list
        )
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def merge_media(src_url:str, merging_section:list = None):
    write_info = util.write_merge_medium_txt(src_url,merging_section)
    filename = write_info[0]
    output_url = util.make_merged_url(src_url, write_info[1])
    code = 'ffmpeg -f concat -safe 0 -i {} -c copy {}'.format(filename,output_url)
    os.system(code)

    parsed_output_url = util.parse_url(output_url)
    return '{}.{}'.format(parsed_output_url[0], parsed_output_url[1])