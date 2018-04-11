# simulate that streamanalytics is installed as a python package
import context

import streamanalytics as ts

def main():
    histo = ts.Histogrammer()
    time_hist = histo.get_histo('data/data.txt', 'date_time', bin_width=10)
    histo.plot_histo(time_hist)

    # OR directly from file
    # histo.plot_histo_from_file('data/data_hist.txt')

if __name__ == '__main__':
    main()
