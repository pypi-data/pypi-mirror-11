'''
Generates .csv data table with relevant properties for all images for all
targets in a given catalog

Copyright (c) 2015, Laura Eckman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import time
import csv 
from analysis_script import target_analysis

if __name__ == '__main__':

    #### EDITABLE ##################################################################################

    data_container = 'FITS/TAM/' #alter to analyze a different set

    min_index = 0 
    max_index = 56 #alter to analyze only a subset

    output_file = 'Results/TAM/ANALYSIS.csv' #make sure this file path actually exists!

    ################################################################################################

    t = time.time()
    full = target_analysis(min_index,data_container)

    for target in range (min_index+1,max_index):
        k = target_analysis(target,data_container)
        full.extend(k[1:])

    print time.time()-t, 'SECONDS'

    with open(output_file,'wb') as f:
        writer = csv.writer(f)
        writer.writerows(full)

    print 'COMPLETE'
