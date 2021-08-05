src_url = './src/media/'
log_url = './src/log/'
cut_url = './src/tmp_media/'
merge_txt_url = './src/merge_txt/'
merge_media_url = './src/merge_url/'
rel_to_cut_media = '../tmp_media/'
cut_name_parse_code = '_@'
merged_media_parse_code = '_M@'

video_rate:dict = {
    'ntsc':30000/1001, 
    'pal':25/1,
    'qntsc':30000/1001,
    'qpal':25/1,
    'sntsc':30000/1001,
    'spal':25/1,
    'film':24/1,
    'ntsc-film':24000/1001,
}