from src import app

if __name__ == '__main__':
    app.run_app(
        config= {
            'filename':'test.mp4',
            'section' : [
                99,
                222
            ],
            'print_log':True
        }
    )