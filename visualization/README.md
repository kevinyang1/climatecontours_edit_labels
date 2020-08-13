### CONTENTS:
* basemap.yml - `conda env create -f basemap.yml` for python dependencies

* no_path_inference_qa.ipynb - Python functions and example code for taking inference generated .nc masks, and creating populated .xmls to input into the tool. In combination with climate .jpgs, intended use is to set up ClimateContours to perform QA on the outputs of your ML segmentation models.
  
  * How to change ranges for field coloring:
  
  1)
  

* basemaping_no_path.py - legacy code used to color and create .jpgs and color bars to display to ClimateContours users
