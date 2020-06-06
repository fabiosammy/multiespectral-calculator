#!/usr/bin/python2.7

import os
import numpy as np
import gdal

# These methods as been developmented using:
# https://micasense.github.io/imageprocessing/Alignment-10Band.html

import sys
sys.path.insert(0, './imageprocessing')
import micasense.imageset as imageset
import micasense.capture as capture

def stack_image(images_list, path_sample_point, new_path_sample_point, image_id):
  images_to_stitch = filter(lambda x: "_{}_".format(image_id) in x, images_list)
  gre_image = filter(lambda x: "_GRE" in x, images_to_stitch)[0]
  nir_image = filter(lambda x: "_NIR" in x, images_to_stitch)[0]
  red_image = filter(lambda x: "_RED" in x, images_to_stitch)[0]
  reg_image = filter(lambda x: "_REG" in x, images_to_stitch)[0]
  print("{}, {}, {}, {}.".format(gre_image, nir_image, red_image, reg_image))
  imgset = load_images_into_image_set(path_sample_point, image_id)
  align_images(new_path_sample_point, imgset)

def load_images_into_image_set(path_sample_point, image_id):
  panelNames = None
  useDLS = False
  panelCap = None
  img_type = 'radiance'
  return imageset.ImageSet.from_directory(path_sample_point, "*_{}_*.TIF".format(image_id))

def align_images(new_path_sample_point, imgset, warp_matrices = None, irradiance = None, overwrite = True):
  for _i, capture in enumerate(imgset.captures):
    outputFilename = capture.uuid+'.tif'
    fullOutputPath = os.path.join(new_path_sample_point, outputFilename)
    if (not os.path.exists(fullOutputPath)) or overwrite:
      if(len(capture.images) == len(imgset.captures[0].images)):
        capture.create_aligned_capture(irradiance_list=irradiance, warp_matrices=warp_matrices)
        capture.save_capture_as_stack(fullOutputPath)
    capture.clear_image_data()

def export_image(im_display, filename, sort_by_wavelength = True):
  rows, cols, bands = im_display.shape

  driver = gdal.GetDriverByName('GTiff')
  
  out_raster = driver.Create(
    filename + ".tiff", 
    cols, rows, bands, 
    gdal.GDT_UInt16, 
    options = [ 'INTERLEAVE=BAND','COMPRESS=DEFLATE' ]
  )
  
  try:
    if sort_by_wavelength:
      eo_list = list(np.argsort(capture.center_wavelengths()))
    else:
      eo_list = capture.eo_indices()

    for outband,inband in enumerate(eo_list):
      outband = out_raster.GetRasterBand(outband+1)
      outdata = im_aligned[:,:,inband]
      outdata[outdata<0] = 0
      outdata[outdata>2] = 2   #limit reflectance data to 200% to allow some specular reflections
      outband.WriteArray(outdata*32768) # scale reflectance images so 100% = 32768
      outband.FlushCache()

    for outband,inband in enumerate(capture.lw_indices()):
      outband = outRaster.GetRasterBand(len(eo_list)+outband+1)
      outdata = (im_aligned[:,:,inband]+273.15) * 100 # scale data from float degC to back to centi-Kelvin to fit into uint16
      outdata[outdata<0] = 0
      outdata[outdata>65535] = 65535
      outband.WriteArray(outdata)
      outband.FlushCache()
  finally:
    out_raster = None