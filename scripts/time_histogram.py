# simulate that streamanalytics is installed as a python package
import context

import streamanalytics as sa

def main():
    histo = sa.Histogrammer()

    # From raw data file
    time_hist = histo.get_histo('data/data.txt', 'date_time', bin_width=10)
    histo.plot_histo(time_hist)

    # OR directly from a previously generated histogram file
    # histo.plot_histo_from_file('data/data_hist.txt')

if __name__ == '__main__':
    main()
