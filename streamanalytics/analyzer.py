import json
import os
import datetime
import math
import matplotlib.pyplot as plt

class DataAnalyzer:
    def __init__(self):
        pass

    def add_fname_suffix(self, fname, suffix):
        o_fname, o_fname_ext = os.path.splitext( os.path.basename(fname) )
        o_fname = o_fname + suffix + o_fname_ext
        return o_fname

    def convert_to_json(self, fname):
        f_dir_name = os.path.dirname(os.path.abspath(fname))
        o_fname = self.add_fname_suffix(fname, '_json')

        with open(fname) as inp_f, \
                open(os.path.join(f_dir_name, o_fname), 'w') as out_f:
            for line in inp_f:
                data_row = eval(line)
                json_str = json.dumps(data_row, ensure_ascii=False)
                out_f.write(json_str)
                out_f.write(os.linesep)

        return os.path.join(f_dir_name, o_fname)

    def str_to_unix_time(self, data_time_str):
        date_time_obj = datetime.datetime.strptime(data_time_str,
                                                    '%m/%d/%Y %H:%M:%S')
        date_time_unix = date_time_obj.timestamp()
        return date_time_unix

    def unix_time_to_str(self, unix_time):
        return datetime.datetime.fromtimestamp(unix_time).strftime(
                                                            '%m/%d/%Y %H:%M:%S')

    def min_unix_time(self, f_name, time_field_name):
        min_time = float('Inf')
        with open(f_name) as f:
            for line in f:
                data_row = json.loads(line)
                date_time = data_row[time_field_name]
                date_time_unix = self.str_to_unix_time(date_time)

                if date_time_unix<min_time:
                    min_time = date_time_unix
        return min_time

    def get_bin_ind(self, unix_time, start_time, bin_width):
        bin_index = math.floor( (unix_time-start_time)/bin_width )
        return bin_index

    def get_bin_start(self, bin_ind, start_time, bin_width):
        return start_time + (bin_ind*bin_width)

    def construct_histogram(self, f_name, time_field_name, min_time, bin_width):
        time_hist = {}
        with open(f_name) as f:
            for line in f:
                data_row = json.loads(line)
                date_time = data_row[time_field_name]
                date_time_unix = self.str_to_unix_time(date_time)
                time_bin = self.get_bin_ind(date_time_unix, min_time, bin_width)

                if time_bin in time_hist.keys():
                    time_hist[time_bin]['count'] += 1
                else:
                    bin_label=self.get_bin_start(time_bin, min_time, bin_width)
                    bin_label=self.unix_time_to_str(bin_label)
                    time_hist[time_bin] = {
                        'bin_start': bin_label,
                        'count': 1
                        }

        return time_hist

    def get_histo(self, fname, time_field_name, bin_width,
                        convert_to_json=False):
        f_dir_name = os.path.dirname(os.path.abspath(fname))
        f_name = fname
        if convert_to_json:
            f_name = self.convert_to_json(f_name)

        bin_width = int(bin_width)
        min_time = self.min_unix_time(f_name, time_field_name)
        time_hist = self.construct_histogram(f_name, time_field_name,
                                                min_time, bin_width)

        o_fname = self.add_fname_suffix(f_name, '_hist')
        if not os.path.exists(os.path.join(f_dir_name, o_fname)):
            out_f = open(os.path.join(f_dir_name, o_fname), 'a')
            out_f.close()

        with open(os.path.join(f_dir_name, o_fname), 'w') as out_f:
            time_hist_json = json.dumps(time_hist)
            out_f.write(time_hist_json)
        return time_hist_json

    def plot_histo(self, time_hist_json):
        time_hist = json.loads(time_hist_json)
        new_hist = {}
        for k in time_hist.keys():
            v = time_hist[k]
            new_hist[v['bin_start']] = v['count']

        plt.bar(range(len(new_hist)), list(new_hist.values()), align='center')
        plt.xlabel('time (minutes)')
        plt.ylabel('number of tweets')
        plt.show()

def main():
    analyzer = DataAnalyzer()
    time_hist = analyzer.get_histo('data/data.txt', 'date_time', bin_width=60)
    analyzer.plot_histo(time_hist)

if __name__ == '__main__':
    main()
