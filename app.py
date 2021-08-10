from src import app

if __name__ == '__main__':
    app.run_app(
        config= {
            'remove_legacy_files':True, #폴더에 쌓인 데이터들을 제거 *(./src/media/ 제외)
            'print_src_gop_log':False,
            'use_section1':False, #아래 section1을 사용

            ##########[Section 1]##########
            'filename':'ntsc_test.mp4', # ./src/media/{filename}
            'video_rate':'ntsc', # constant.video_rate['key'], info_url= https://ffmpeg.org/ffmpeg-all.html#toc-Video-rate
            'src_draw_text': True, #filename의 영상에 Frame정보를 띄움.
            'use_after_draw_text':True, #filename의 값이 아니라 Frame을 draw한 영상으로 작업 진행.
            'split':True,
            'split_sections' : [ #split이 True이면 사용. input section (0, section[0 ~ n], last_frame_num)
                90,
                180,
            ],
            'merge':True,
            'merge_sections' : [ #merge가 True이면 사용 media_num ex:) 0, 1, 2 or all
                'all'
            ],
            'print_log':True,
            'out_draw_text':True
        }
    )
    print('\n\n###############################\nEnd\n###############################\n\n')
    input()
