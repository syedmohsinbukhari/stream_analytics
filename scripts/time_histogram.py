# simulate that streamanalytics is installed as a python package
import context

import streamanalytics as ts

def main():
    analyzer = ts.DataAnalyzer()
    time_hist = analyzer.get_histo('data/data.txt', 'date_time', bin_width=60)
    analyzer.plot_histo(time_hist)

if __name__ == '__main__':
    main()
