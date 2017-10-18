# pycpselect

A python script that mimicks parts of the cpselect function in Matlab.

### Prerequisites

You will need to have the following libraries installed:
* matplotlib
* numpy

### Installing

Download pycpselect script and import it

```
import pycpselect
```

### Using pycpselect

The function cpselect takes two inputs, both need to be the same pixel size, square, and gray-scale images or 2D matrices. The function cpselect will return the coordinates of each image that correspond to the same location on the images (selected by user) and the pixel size of the images.

```
[refpointlist,movpointlist,pixelSize] = cpselect(refImage,movImage):

refImage: reference image
movImage: moving/skewed image

refpointlist: selected coordinates in reference image
movpointlist: selected coordinates in moving/skewed image
pixelSize: pixel size of images
```

With the return coordinate we can now do an affine transformation to moving/skewed image to reference image (This function will be added soon)
