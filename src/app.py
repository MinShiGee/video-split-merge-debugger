from collections import defaultdict
from . import ffmpeg_module as ffmpeg
from . import util

def run_app(config: defaultdict(None)):
    filename = config['filename']
    split_section = config['section']
    if filename == None:
        print('filename is not available.')
        return
    
    util.init_log()
    util.write_gop_info_text(filename)
    src_url = util.make_url(filename)
    ffmpeg.split_media(src_url,split_section)
    merged_file_name = ffmpeg.merge_media(src_url)
    util.write_gop_info_text(merged_file_name)
    for name in util.make_divided_media_list(src_url):
        util.append_log('{} end_time = '.format(name) + ffmpeg.get_media_endtime(util.make_url(name)))    
    util.append_log('merg end_time = ' + ffmpeg.get_media_endtime(util.make_url(merged_file_name)))
    print_bar = '==============================='
    util.compare_gop_info_txt(
            '<meta-data>\nori : {} \nmerg : {} \nseg : {} \n{} \n'.format(filename,merged_file_name,''.join(['{}, '.format(str(i)) for i in split_section]),print_bar),
            filename, 
            merged_file_name
    )
    return