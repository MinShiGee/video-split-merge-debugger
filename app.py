from src import app

if __name__ == '__main__':
    app.run_app(
        config= {
            'filename':'test.mp4',
            'video_rate':'ntsc-film', # constant.video_rate['key'], info_url= https://ffmpeg.org/ffmpeg-all.html#toc-Video-rate
            'remove_legacy_files':True, #폴더에 쌓인 데이터들을 제거 *(./src/media/ 제외)
            'src_draw_text': False, #filename의 영상에 Frame정보를 띄움.
            'use_after_draw_text':False, #filename의 값이 아니라 Frame을 draw한 영상으로 작업 진행.
            'split':False,
            'split_sections' : [ #split이 True이면 사용. input section (0, section[0 ~ n], last_frame_num)
                120,
                240
            ],
            'merge':False,
            'merge_sections' : [ #merge가 True이면 사용 media_num ex:) 0, 1, 2 or all
                'all'
            ],
            'print_log':True,
        }
    )
    print('\n\n###############################\nEnd\n###############################\n\n')
    input()
