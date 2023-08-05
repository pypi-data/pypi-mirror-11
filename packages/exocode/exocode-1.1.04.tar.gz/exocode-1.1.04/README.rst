**ExoCode**

Generates .csv files including data on the existence of various features of interest 
from the Digitized Sky Survey (DSS), 2-micron All Sky Survey (2MASS), and 
Wide-field Infrared Survey Explorer (WISE) image catalogs. The goal is to use the 
data to identify candidates that might have circumstellar debris disks. 

Dependent on scikit-image (skimage), matplotlib, numpy, and pyfits. 

---------------

**TO USE:**

* Use dataAcq.py to retrieve the images for one of the provided catalogs in  Catalogs/

  * You can also use one of your own, provided the format remains the same: ra,dec (degrees)

  * Data included for tam_cat_sample.csv catalog under FITS/TAM/

*  Use dataGen.py to run analysis on the downloaded images and output the results to a new .csv

**Run Guidelines:**

*New Graphical Interface*

* run application

* select desired catalog

* follow prompts to gather data, flip through indices

* future updates will implement support for image display and easier search through data


Command line: (in exoCode containing directory)

    cd exoCode

    python dataGen.py

In python:

    from exoCode import dataGen
