'''
Use Otsu's method to analyze catalog images, keep pixels only above a certain threshold

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

from skimage.filters import threshold_otsu

def threshold(img):
    '''
    Args:
      img: numpy array of image
      output_file: string representing location where 
        thresholded image should be saved
    Process image and save thresholded version
    Return (thresholded array,threshold value)
    '''

    threshold_global_otsu = threshold_otsu(img)
    global_otsu = img >= threshold_global_otsu

    return (global_otsu,threshold_global_otsu)

if __name__ == '__main__':

    #example usage:
    #display threshold(<image>)[0] using matplotlib or similar
    #print 'Threshold Value',threshold(<image>)[1]
    pass

