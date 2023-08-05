#Janelia Signal Analysis (janeliasig)
Created by **Spencer Hong**

Contact me at <spencer.hongx@gmail.com> (preferred) or <hongs@janelia.hhmi.org>


GitHub: <http://www.github.com/SpenceyHong/janeliasig>

*Janelia is a research campus of the Howard Hughes Medical Institute (HHMI). My group leader was Dr. Karel Svoboda. To learn more about Janelia, visit <http://www.janelia.org>.*
##License and Copyright
Portions of Code contained are subject to the MIT License. 

Janelia Research Campus Software Copyright 1.1

Copyright (c) 2015, Howard Hughes Medical Institute, All rights reserved.

Please see **License.txt** for more information.
##Overview
This is a Python module with ** three features **

***1)*** Tkinter-based Python GUI data browser with built-in cross-correlation analysis

***2)*** Poisson simulations to model PMT outputs

***3)*** Peak detection and photon delineation algorithms

##Installation
This module was developed and tested on Python 2.7.

Install Anacodona at <http://continuum.io/downloads>

IPython Jupyter Notebook at <http://ipython.org/install.html>

janeliasig is available on PYPI!

`pip install janeliasig`

Or

Clone this directory and run

`python setup.py install`

##GUI Browser
The GUI lies in the module folder as *gui_browser.py*

To run the GUI, type the following in bash:

**DO NOT IMPORT GUI LIKE THE REST OF THE MODULE**

`python gui_browser.py`

Or in iPython:


`ipython`

`%run gui_browser.py`


###How to use GUI
When the GUI opens, first press ***Input File*** to select your choice of .bin file. 

Then, to choose the x window range, type the mimimum and the maximum of the x window. Then, press ***Click to Change X-Window***.

To run the peak-detection method and the cross correlation, press ***Plot Detected Peaks***. 

*Maximize and Minimize functions are glitchy on cross-correlated graphs.*

The left and right arrow keys will pan the graph. Up and right arrow keys will only move the y-window slightly at a time.

To change the input file, the GUI will allow you to change it, so you don't need to close out every time you wish to change the input file.

The built-in matplotlib functions like pan, save, and subplot settings are still in place.

The sampling frequency is not dynamically set. 

##Algorithms
### How to use functions
To import the functions, the import statement should look like the following:

`import janeliasig.janeliasig.algorithm as js` (or any abbreviation)

If that is not working, make sure that janeliasig is in your site-packages folder. To find your site-packages folder, find one of your pre-installed packages. In this example, I will use numpy.

In iPython cell, run the following:

`numpy.__file__`

The source folder of **__init__.py** should tell you where your site-package folder is. 

###Docstrings
These docstrings are present in the module, but this is a  comprehensive list of all docstrings used in janeliasig.

#####load_raw_data():
`filename` refers to the full directory of the .bin file. 

`num_elements` refers to the number of elements you wish to unpack from the binary file. The **default** is infinity. I **recommend** that only 50e6 elements are unpacked at a time. 

`sourcedataformat` refers to the format of the input data. The **default** is int8. 

`targetdataformat` refers to the format of the output data. The **default** is int8.

load_raw_data() is a converted file from matlab to Python. It will unpack any binary file to make it matplotlib-compatible data. The binary file is unpacked chunks at at time to decrease the chance of system crash. 

~~~
The output is a list of all data points that you have unpacked. 
~~~

#####peakdet():
`data_array` refers to the dataset that you wish to run the detection algorithm on.

`threshold` refers to the minimum distance between a peak to a valley for the algorithm to detect it as a peak.

`x_axis` is an array of x-coordinates that go along with the `data_array`. The **default** is None. 

Will detect most peaks in any dataset. 

~~~~
The output is a tuple of two numpy arrays:(peak values and times), (valley values and times).
~~~~
***Valley refers to the minimums while peak refers to the maximums***

#####threshold_algorithm():
`threshold_value`; please refer to the docstring for **peakdet()**

`data`; again, ditto above

~~~~
The output is a tuple of two lists; peak times, peak events. The algorithm can be modified to return valley times and events. 
~~~~

#####clean_algorithm():
`data` refers to any dataset that wishes to be cleaned up using a cross-correlation and smart threshold analysis. 

`template` refers to the list of points that will act as a template for cross correlation. 
The data that I used this function on was unpacked using `load_raw_data` function.

~~~
The output is a tuple of peak events, peak times, and the correlated data. 
~~~
**This algorithm is used in the GUI. This is the extent of my progress during my time at Janelia.**

#####mean_variance_graph():
`times_data` should be a list of times that a photon has reflected back. 

This function attempts to make a mean-variance graph based on the discreet-time series data of photon arrivals. In other cases, it can be used to make a mean-variance graph of any discreet data. The mean-variance graph can be used to check if the data follows a poisson process, where the ***mean*** equals the ***variance***. 

~~~~
The output is `mean_data, variance_data, std_data`, where `mean_data` is a list of all means, `variance_data` is a list of all variances, and `std_data` is a list of standard errors. Run `plt.plot(mean_data, variance_data)` and `plt.errorbar(mean_data, variance_data, yerr= std_data)` *(plt == matplotlib.pyplot)* to visualize the output. 
~~~~
#####gaussian_kernel():
`sigma` refers to the standard deviation of the desired gaussian kernel. 

This function will take 401 points to create a full gaussian kernel. 

~~~~
The output is a gaussian kernel in a list (length of 401)
~~~~
#####make_confusion_matrix():
`gold_standard_input` refers to the "true" data, the dataset that will be used to compare all other datasets. 

`algorithm_standard_input` refers to the "detected" data, the dataset that will be compared to the true dataset. 

`threshold_max` refers to the maximium threshold level the confusion matrix will work to. The **default** is 5. 

`threshold_interval` refers to the interval that the threshold levels will be increasing. The **default** is 0.15. 

(The last two functions only make sense if you are using this function in the context of peak_detection. If you are not doing so, feel free to modify the function.)

This function also will return the **matthew's correlation coefficient** which is a single value that measures the idealness of the algorithm. 

~~~~
The output is `matrix_set, matthews_coeff_set` as a tuple.
~~~~

#####receiver_operating_curve():
`gold_standard_input`; please refer to the docstring for **make_confusion_matrix()**

`algorithm_standard_input`; again, ditto above

`threshold_max`; again, ditto above

`threshold_interval`; again, ditto above

The receiver operating curve is a visualization of the idealness of the algorithm. I ran this curve with my peak detection algorithms and poisson simulations as the `gold_standard_input`.

~~~~
The output is a tuple of false positives, true positives. But, the function calculates also false negatives and true negatives (just modify the output line).
~~~~

#####rsqured():
`x` refers to the x coordinates.

`y` refers to the y coordinates.

~~~~
The output is a r-squared value based on a linear regression.
~~~~

#####statistics():
`interval_data` refers to a list of times that a photon has reflected back.

`variable` is a counter: 1 to return variances, 2 to return means, and 3 to return standard errors. The **default** is 1, the variance. 

~~~~
The output is either the variance, the mean, or the standard error of the input list. (Modify the function to return tuples)
~~~~

#####full_simulation():
`expected` refers to the lambda of the poisson process. 

`trial` refers to how many times the poisson processs is going run to produce the expected value.

`repetition` refers to the number of times the poisson process is going to be repeated. 

The **default** is 1. 

The output is a list of three elements: [variances, means, standard errors]

***statistics() is used in this simulation***

#####poisson():
`expected`; please refer to the docstring for **full_simulation()**

`trials`; again, ditto above

~~~~
The ouput is a list of times of poisson-modulated events.
~~~~
#####poisson_interarrival():
`expected`; please refer to the docstring for **full_simulation()**

`trials`; again, ditto above

~~~~
The output is a list of times in between poisson-modulated events.
~~~~



 








