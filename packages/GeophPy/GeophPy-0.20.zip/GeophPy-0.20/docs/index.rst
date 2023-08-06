==================================================================
GeophPy : Tools for sub-surface geophysical survey data processing
==================================================================

.. module:: geophpy

Introduction
------------

This project was initiated through cooperation between the french CNRS units `UMR5133-Archeorient`_ (FR) and `UMR7619-Metis`_ (FR)
 
.. _`UMR5133-Archeorient`: http://www.archeorient.mom.fr/recherche-et-activites/ressources-techniques/pole-2/
.. _`UMR7619-Metis`: http://www.sisyphe.jussieu.fr/dga/

Description
-----------

GeophPy is a python module which aims at building tools to display and process sub-surface geophysics data in the field of archaeology, geology, and other.

The main feature of this module is to build a "geophysic data set" composed by series of data values Z in the format (X,Y,Z) with (X,Y) being the point position of the geophysic Z value, to process or display maps of Z values.

This module has been developped to be used in a graphical user interface software, WuMapPy.
 

Features
--------

* Building a data set from one or severals data files.
* Displaying geophysicals maps in 2D or 3D Dimensions.
* Processing data sets with geophysicals methods.
* Compatibility with Python 3.x


Installation
------------

Download the zip file "GeophPy-vx.y" and unzip it.

You can install now GeophPy with this command:

.. code-block:: console

    $ python setup.py install

WuMapPy and GeophPy are using others python modules. If the installation of one of these modules failed on windows, you can install independently thes modules using this useful web site : http://www.lfd.uci.edu/~gohlke/pythonlibs/


Quick Start
-----------
    >>> from geophpy.dataset import *

Opening files
~~~~~~~~~~~~~

You can open files indicating the column number (1...n) of the data set to be processed :
    
    - ".dat" issued from Geometrics magnetometer G-858 (named 'ascii' format with ' ' as delimiter):

    >>> dataset = DataSet.from_file(["test.dat"], format='ascii',
    delimiter=' ')

    - or XYZ files (files with column titles on the first line, and data values on the others, with X and Y in the first two columns, and Z1,...,Zn in the following columns, separated by a delimiter '\t' ',' ';'...)

    >>> dataset = DataSet.from_file(["test.xyz"], format='ascii',
    delimiter='\t')

    XYZ file example:
        =====  =====  =====
    	X      Y      Z
        =====  =====  =====
	0      0      0.34
	0      1      -0.21
	0      2      2.45
        ...    ...    ...
        =====  =====  =====


You can easily obtain the list of the available file formats with the command :

    >>> list = fileformat_getlist()
    >>> print(list)
    ['ascii']

It is possible to build a data set from a concatenation of severals files of the same format :

    - To open several selected files:
    
    >>> dataset = DataSet.from_file(["abcde.dat","fghij.dat"],
                  format='ascii', delimiter=' ', z_colnum = 5)

    - To open all files ".dat" beginning by "file":

    >>> dataset = DataSet.from_file(["file*.dat"], format='ascii',
		  delimiter=' ', z_colnum = 5)


Checking files compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Opening several files to build a data set needs to make sure that all files selected are in the same format.

It's possible to check it by reading the headers of each files:

    >>> compatibility = True
    >>> columns_nb = None
    >>> for file in fileslist :
    >>>    col_nb, rows = getlinesfrom_file(file)
    >>>    if ((columns_nb != None) and (col_nb != columns_nb)) :
    >>>        compatibility = False
    >>>        break
    >>>    else :
    >>>        columns_nb = col_nb


Data set Description
~~~~~~~~~~~~~~~~~~~~

A data set contains 3 objects:
    - info.
    - data.
    - georef.

The "info" object contains informations about the data set:
    - x_min = minimal x coordinate of the data set.
    - x_max = maximal x coordinate of the data set.
    - y_min = minimal y coordinate of the data set.
    - y_max = maximal y coordinate of the data set.
    - z_min = minimal z value of the data set.
    - z_max = maximal z value of the data set.
    - x_gridding_delta = delta between 2 x values in the interpolated image grid.
    - y_gridding_delta = delta between 2 y values in the interpolated image grid.
    - gridding_interpolation = interpolation name used for the building of the image grid.

The "data" object contains :
    - fields = names of the fields (columns) : ['X', 'Y', 'Z']
    - values = 2D array of raw values before interpolating (array with (x, y, z) values) : [[0, 0, 0.34], [0, 1, -0.21], [0, 2, 2.45], ...]
    - z_image = 2D array of current gridded z data values : [[z(x0,y0), z(x1,y0), z(x2,y0), ...], [z(x0,y1), z(x1,y1), z(x2,y1), ...], ...]

    (Note : the z_image structure is not built after openinf file, but by using gridding interpolation function) 

The "georef" object contains :
    - active = True if contains georeferencing informations, False by default.
    - pt1 = Point number 1 Coordinates, in local and utm referencing (local_x, local_y, utm_easting, utm_northing, utm_zonenumber, utm_zoneletter).    
    - pt2 = Point number 2 Coordinates, in local and utm referencing (local_x, local_y, utm_easting, utm_northing, utm_zonenumber, utm_zoneletter).    


Data set operating
~~~~~~~~~~~~~~~~~~

You can duplicate a data set to save, for example, a raw data set before processing it :

    >>> rawdataset = dataset.copy()

After having opened a file, you can interpolate (or not) data, with severals gridding interpolation methods ('none', 'nearest', 'linear', 'cubic') to build z_image structure :

    >>> dataset.interpolate(interpolation="none")

After doing this operation, it's easy to see on a same plot the map and the plots (on a grid or not if no gridding interpolation is selected):

.. image:: _static/figCarto2.PNG
   :width: 50%
   :align: center


Data set processing
~~~~~~~~~~~~~~~~~~~

Peak filtering
++++++++++++++

Peak filtering allows to filtering values lower than 'setmin' and upper than 'setmax'.
It can replace theses values by 'NaN' value (if setnan at True), or median value (if setmed at True (and setnan at False)).


Median filtering
++++++++++++++++

Median filtering allows to filtering values lower or upper than a percentage of the meaning of the (nx*ny) grid of points around.

.. image:: _static/figMedianFilter.PNG
   :width: 20%
   :align: center


Festoon filtering
+++++++++++++++++

... To Be Developped ...


Regional trend filtering
++++++++++++++++++++++++

... To Be Developped ...


Wallis filtering
++++++++++++++++

... To Be Developped ...


Plough filtering
++++++++++++++++

... To Be Developped ...


Constant destriping
+++++++++++++++++++

... To Be Developped ...


Curve destriping
++++++++++++++++

... To Be Developped ...


Logarithmic transformation
++++++++++++++++++++++++++

Introduction :

This processing is described here : "Enhancement of magnetic data by logarithmic transformation", Bill Morris, Matt Pozza, Joe Boyce and Georges Leblanc - The Leading EDGE August 2001, Vol. 20,Num 8.

Input parameters :

* multfactor : it is a multiplying factor of the data (x5, x10, x20, x100).

This factor depends on the precision of the data and is in the inverse order of this precision.


Pole Reduction
++++++++++++++

The reduction to the magnetic pole sets the data easy to read and be compared.
This processing calculates the anomaly which be obtained for the full incination of the magnetic field.
It uses a fast fourier series algorithm to work in the spectral range.

Input parameters :

* factor of apodisation, to reduce side effects.
* inclination angle, angle between the geomagnetic North and the magnetic field measured at the soil surface, in the vertical plane.
* alpha angle : it's the angle between geomagnetic North and profiles direction, in the horizontal plane.

.. image:: _static/figAnglesRepresentation.PNG
   :width: 50%
   :align: center

.. image:: _static/figWindowPoleReduction.PNG	
   :width: 50%
   :align: center

Algorithm :

.. image:: _static/figAlgoPoleReduction.PNG	

u is the spatial frequency corresponding at the x direction, and v is the spatial frequency corresponding at the y direction.

- Filling gaps :

To use the fast fourier algorithme, the data set don't have to contain gaps or 'NaN' values (Not A Number).
If the data set grid is not over interpolated, the first step will be profile by profile to fill the gaps using a spline interpolation method.

Apodisation :

It is an operation to attenuate sides effects. The factor of apodisation (0, 5, 10, 15, 20 or 25%) precises the size to extend the data values zone. Values of this extension will be attenuated by a cosinus formula :
 
.. image:: _static/figApodisation.PNG	

After processing, the size of the data values zone will become the same than before this apodisation.

Continuation
++++++++++++

The downward continuation is a solution to reduce spread of anomalies and to correct coalescences calculating the anomaly if measures would be done at a lower level.
The upward continuation allows to smooth data.

Input parameters :

* factor of apodisation, to reduce side effects.
* Technical of prospection ("Magnetic field", "Magnetic field gradient", Vertical component gradient").
* Sensors altitudes, relatives to th soil surface.
* Continuation value, above or below the soil surface.

.. image:: _static/figWindowContinuation.PNG	
   :width: 50%
   :align: center

Algorithm :

.. image:: _static/figAlgoContinuation.PNG	

The method of filling gaps or apodisation to reduce side effects are the sames than used in the pole reduction function.

 
High level processing functions
+++++++++++++++++++++++++++++++

The calling protocol of these functions are describeds in the end of this document, but about the detailed code of these processing functions, it's there :

.. automodule:: geophpy.processing.general
    :members: peakfilt, medianfilt, festoonfilt, regtrend, wallisflit, ploughfilt, destripecon, destripecurve

.. automodule:: geophpy.processing.magnetism
    :members: logtransform, polereduction, continuation

.. automodule:: geophpy.operation.general
    :members: apodisation2d


Data set plotting
~~~~~~~~~~~~~~~~~

Plot type:

It is possible to plot the data set thanks to several plot types.

To see the plot types available , you can use :

    >>> list = plottype_getlist()
    >>> print(list)
    ['2D-SURFACE','2D-CONTOUR', '2D-CONTOURF']

Interpolation:

It is possible to plot the data set by choosing several interpolations for the surface display.

To get the plotting interpolations available , you must type:

    >>> list = interpolation_getlist()
    >>> print(list)
    ['nearest', 'bilinear', 'bicubic', 'spline16', 'sinc']

Color map:

To plot a data set, you have to choose a color map.

To see the color maps available, you type:

    >>> cmaplist = colormap_getlist(creversed=False)
    >>> print(cmaplist)
    ['Blues', 'BrBG', 'BuGn', 'BuPu', 'CMRmap', 'GnBu', 'Greens', 'Greys',
     'OrRd', 'Oranges', 'PRGn', 'PiYG', 'PuBu', 'PuOr', 'PuRd','Purples',
     'RdBu','RdGy','RdPu','RdYlBu', 'RdYlGn', 'Reds', 'Spectral', 'Wistia',
     'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd', 'afmhot', 'autumn', 'binary',
     'bone', 'bwr', 'copper', 'gist_earth', 'gist_gray', 'gist_heat',
     'gist_yarg', 'gnuplot', 'gray', 'hot', 'hsv', 'jet', 'ocean', 'pink',
     'spectral', 'terrain']


Using the parameter creversed=True, you obtain the same number of color maps but with reversed colors, with a "_r" extension:

    >>> for i in range (cmapnb):
    >>>     colormap_plot(cmaplist[i-1], filename="CMAP_" +
            str(i) + ".PNG")

Examples :

.. image:: _static/figColorMap_1.PNG	
.. image:: _static/figColorMap_2.PNG	
.. image:: _static/figColorMap_3.PNG	
.. image:: _static/figColorMap_4.PNG	
.. image:: _static/figColorMap_5.PNG	
.. image:: _static/figColorMap_6.PNG	

or you can build figure and plot objects to display them in a new window:

    >>> cm_fig = None
    >>> first_time = True
    >>> for cmapname in cmaplist:
    >>>     cm_fig = colormap_plot(cmapname, fig=cm_fig)
    >>>     if (first_time == True):
    >>>         fig.show()
    >>>         first_time = False
    >>>     fig.draw()

Histogram:

To adjust the limits of color map you must view the limits of the data set:

    >>> zmin, zmax = dataset.histo_getlimits()

You can also plot the histogram curve :

    >>> dataset.histo_plot("histo.PNG", zmin, zmax, dpi=100,
        transparent=True)

to obtain :

.. image:: _static/figHisto.PNG
   :width: 50%
   :align: center

or you can build figure and plot objects to display them in a window:

    >>> h_fig = dataset.histo_plot()


Correlation map:

You can plot the correlation map of a dataset :

    >>> dataset.correlation_plotmap("corrmap.PNG", dpi=100, transparent=True)

to obtain :

.. image:: _static/figCorrelationMap.PNG
   :width: 50%
   :align: center

or you can build figure and plot objects to display them in a window:

    >>> h_fig = dataset.histo_plot()


Correlation sums:

You can plot the correlation sums of a dataset :

    >>> dataset.correlation_plotsum("corrsum.PNG", dpi=100, transparent=True)

to obtain :

.. image:: _static/figCorrelationSum.PNG
   :width: 50%
   :align: center


Map plotting:

You can plot a data set using one of these plot types:

    >>> dataset.plot('2D-SURFACE', 'gray_r', plot.PNG,
        interpolation='bilinear', transparent=True, dpi=400)

Examples :

Different plot types ('2D-SURFACE', '2D-CONTOUR', '2D-CONTOURF'):

'2D-SURFACE' :

.. image:: _static/figCarto1.PNG
   :width: 50%
   :align: center

'2D-CONTOUR' :

.. image:: _static/figCarto3.PNG
   :width: 50%
   :align: center

Different interpolations for a "2D-SURFACE" plot type ('bilinear', 'bicubic'):

With 'bilinear' interpolation:

.. image:: _static/figCarto4.PNG
   :width: 50%
   :align: center

With 'bicubic' interpolation:

.. image:: _static/figCarto5.PNG
   :width: 50%
   :align: center

It is possible not to display the color map and axis to import the picture in a SIG software.


Data Set Saving
~~~~~~~~~~~~~~~

You can save the data set in a file.

For the time being, it's only possible to save data in xyz files as it's described above:

    >>> dataset.to_file(save.csv, format='xyz')


.. _api:


Geographic Positioning Set
~~~~~~~~~~~~~~~~~~~~~~~~~~

It's possible to open one or several files with geographics coordinates of the geophysics prospection zone :
These files can be ascii files with points positions, or shapefiles.

    >>> from geoposset import *
    >>> gpset = GeoPosSet.from_file(refsys='WGS84', type='shapefile',
	["pt_topo"])	

You can get so the numbers and list of points :

    >>> list = gpset.points_getlist()
    >>> print(list)
    >>> [[0, 32.52, 34.70], [1, 32.52, 34.70]]	#with [num, x or lon, y or lat]

You can plot them :

    >>> fig = gpset.plot()
    >>> fig.show()

.. image:: _static/figGps1.PNG
   :width: 50%
   :align: center

And converting a shapefile in a kml file :

    >>> gpset.to_kml("shapefile.kml")

to view the points, lines, and surfaces described in the shapefile, on google earth :

.. image:: _static/figGps2.PNG
   :width: 50%
   :align: center

It's possible to save theses points into an ascii file (.csv) composed by :

    Line 1 : "'WGS84'", or "'UTM', utm_zoneletter, utm_zonenumber"

    Others lines : point_number; longitude; latitude; X; Y 

Example :

    WGS84
    0;32.52432754649924;34.70609241062902;0.0;0.0
    1;32.52387864354049;34.70625596577242;45.0;0.0
    2;32.52365816268757;34.70584594601077;45.0;50.0
    3;32.52343735426504;34.70543469612403;;		# (X=None, Y=None) => point not referenced in local positioning


It is possible to georeference a data set with at less 4 points.

With the data set georeferenced, it is possible to export the data set in a kml file :

    >>> dataset.to_kml('2D-SURFACE', 'gray_r', "prospection.kml",
	cmmin=-10, cmmax=10, dpi=600)

.. image:: _static/figGeoref1.PNG
   :width: 50%
   :align: center

Exporting the data set as a raster in a SIG application (as ArcGis, QGis, Grass, ...) is possible with severals picture file format ('jpg', 'png', 'tiff') :

    >>> dataset.to_raster('2D-SURFACE', 'gray_r', "prospection.png",
	cmmin=-10, cmmax=10, dpi=600)

.. image:: _static/figGeoref2.PNG
   :width: 50%
   :align: center

A world file containing positioning informations of the raster is created ('jgw' for JPG, 'pgw' dor PNG, and 'tfw' for TIFF picture format) with :

    Line 1: A: pixel size in the x-direction in map units/pixel

    Line 2: D: rotation about y-axis

    Line 3: B: rotation about x-axis

    Line 4: E: pixel size in the y-direction in map units, almost always negative[3]

    Line 5: C: x-coordinate of the center of the upper left pixel

    Line 6: F: y-coordinate of the center of the upper left pixel

Example :

    0.0062202177595

    -0.0190627320737

    0.0131914192417

    0.00860610262817

    660197.8178

    3599813.97056

Using a Graphic User Interface
-------------------------------

The name of the "Graphic User Interface" used has to be mentionned in the "matplotlibrc" file:

to use QT4 GUI :

    backend      : Qt4Agg		

Note : to use QtAgg with PySide module, add :

    backend.qt4  : PySide

or to use Tkinter GUI:

    backend      : TkAgg

Note:
*in Windows environment, this file is in the "C:\\PythonXY\\Lib\\site-packages\\matplotlib\\mpl-data" directory.

*in Linux environment, this file is in the "/etc" directory.

With QT4Agg GUI, you can plot data in a windows :

    >>> from geophpy.dataset import *
    >>> success, dataset = DataSet.from_file("DE11.dat", delimiter=' ',
        z_colnum=5)
    >>> if (success = True):
    >>>    fig, cmap = dataset.plot('2D-SURFACE', 'gist_rainbow',
           dpi=600, axisdisplay=True, cmapdisplay=True, cmmin=-10, cmmax=10)
    >>>    fig.show()

to obtain :

.. image:: _static/figGraphUserInterface.PNG
    :width: 50%
    :align: center

You can also plot data in a windows with several color maps :

    >>> from geophpy.dataset import *
    >>>			# to get the list of color maps availables
    >>> list = colormap_getlist()	
    >>> first = True				# first plot
    >>> fig = None				# no previous figure
    >>> cmap = None				# no previous color map
    >>> success, dataset = DataSet.from_file("DE11.dat", delimiter=' ',
        z_colnum=5)
    >>> if (success == True):			# if file opened
    >>>			# for each color map name in the list
    >>>    for colormapname in list :		
    >>>        fig, cmap = dataset.plot('2D-SURFACE', 'gist_rainbow',
               dpi=600, axisdisplay=True, cmapdisplay=True, cmmin=-10,
               cmmax=10)
    >>>        if (first == True):		# if first plot
    >>>           fig.show()			# displays figure windows
    >>>           first = False			# one time only
    >>>			# updates the plot in the figure windows
    >>>        p.draw()				
    >>>			# removes it to display the next
    >>>        cmap.remove()		
    >>>			# waits 3 seconds before display the plot
    >>>			# with the next color map
    >>>        time.sleep(3)			


High level API
--------------

.. automodule:: geophpy.dataset
    :members: getlinesfrom_file, fileformat_getlist, plottype_getlist, interpolation_getlist, colormap_getlist, colormap_plot, pictureformat_getlist, rasterformat_getlist, correlmap, griddinginterpolation_getlist, festooncorrelation_getlist

.. autoclass:: geophpy.dataset.DataSet
    :members: from_file, to_file, plot, histo_plot, histo_getlimits, copy, peakfilt, medianfilt, festoonfilt, regtrend, wallisfilt, ploughfilt, destripecon, destripecurve, polereduction, logtransform, continuation


Feedback & Contribute
---------------------

Your feedback is more than welcome.

Write email to lionel.darras@mom.fr or philippe.marty@upmc.fr

.. include:: ../CHANGES.rst
