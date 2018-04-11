# simulate that streamanalytics is installed as a python package
import context

import streamanalytics as sa

def main():
    credentials = sa.utils.file_lines_to_array('scripts/conf/api_keys.txt')
    tags = sa.utils.file_lines_to_array('scripts/conf/tags.txt')

    streamer = sa.Streamer()
    streamer(credentials, tags)

    cond = True
    while cond:
        inp = input('Press q then Enter to quit streaming: ')
        cond = (not inp == 'q')

    streamer.disconnect()
    print('Exiting Stream')

if __name__ == '__main__':
    main()
