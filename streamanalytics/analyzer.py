import json
import os

class DataAnalyzer:
    def __init__(self):
        pass

    def convert_to_json(self, fname):
        f_dir_name = os.path.dirname(os.path.abspath(fname))
        o_fname, o_fname_ext = os.path.splitext( os.path.basename(fname) )
        o_fname = o_fname + '_json' + o_fname_ext

        with open(fname) as inp_f, \
                open(os.path.join(f_dir_name, o_fname), 'w') as out_f:
            for line in inp_f:
                data_row = eval(line)
                json_str = json.dumps(data_row, ensure_ascii=False)
                out_f.write(json_str)
                out_f.write(os.linesep)


    def construct_histogram(self, fname, time_field_name, bin_width):
        f_dir_name = os.path.dirname(os.path.abspath(fname))

        bin_width = int(bin_width)

        min_time = float('Inf')
        with open(fname) as f:
            for line in f:
                data_row = eval(line)
                print(data_row)
                break

def main():
    analyzer = DataAnalyzer()
    # analyzer.construct_histogram('data/data.txt', 'date_time', bin_width=10)
    analyzer.convert_to_json('data/data.txt')

if __name__ == '__main__':
    main()
