# simulate that hotelinformatics is installed at PYTHON_PATH
import context

import streamanalytics as ts

def main():
    credentials = ts.utils.file_lines_to_array('scripts/conf/api_keys.txt')
    tags = ts.utils.file_lines_to_array('scripts/conf/tags.txt')

    streamer = ts.Streamer()
    streamer(credentials, tags)

if __name__ == '__main__':
    main()
