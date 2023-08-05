# mview
Package to show graphic view of pandas.DataFrame.


## Install

    pip install mview


## Setting

An external CSV viewer is required. e.g. MS Excel, [CSVFileView](http://www.nirsoft.net/utils/csv_file_view.html).

    import mview
    mview.update_executor('path/to/csv-viewer.exe')


## Usage


    import pandas as pd
    import mview

    data = pd.read_csv('C:\\md\\select\\pp_20150422.csv')
    mview.show(data)
