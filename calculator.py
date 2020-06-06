#!/usr/bin/env python2
# coding: utf-8

import warnings
warnings.filterwarnings("ignore")

import os
import rasterio
from vegetation_index_calculator import VegetationIndexCalculator
from config import *

def save_index_image(profile, index_image, dst_file_path):
  with rasterio.open(dst_file_path, 'w', **profile) as dst:
    dst.write_band(1, index_image)

if __name__ == "__main__":
  for altitude in altitudes:
    altitude_roi_images_path = os.path.join(roi_images_path, altitude)
    for amostra_id in os.listdir(altitude_roi_images_path):
      amostra_id_roi_images_path = os.path.join(roi_images_path, altitude, amostra_id)
      amostra_id_calculated_images_path = os.path.join(calculated_images_path, altitude, amostra_id)
      if not os.path.exists(amostra_id_calculated_images_path):
        os.makedirs(amostra_id_calculated_images_path)
      counter = 0
      for image in os.listdir(amostra_id_roi_images_path):
        image_path = os.path.join(amostra_id_roi_images_path, image)
        print(image_path)

        vic = VegetationIndexCalculator(image_path)
        vic.profile.update({
          # all meta data are the same except the bands number
          'count': 1, # this is the important update from 4 bands to one band
          # 'crs': rasterio.crs.CRS({'init': u'epsg:32633'}),
          'interleave': 'pixel', 'dtype': 'float32',
          'driver': u'GTiff',
          # 'transform': rasterio.transform.Affine(0.25, 0.0, 315423.629, 0.0, -0.25, 6011303.437),
          # 'height': 4721,
          # 'width': 5224,
          'tiled': False,
          'nodata': None
        })

        vegetation_indexes = [method for method in dir(VegetationIndexCalculator) if method not in VegetationIndexCalculator.exclude_methods()]
        for vegetation_index in vegetation_indexes:
          # print(vegetation_index)
          vegetation_index_image_name = vegetation_index + '_' + str(counter) + '_' + image
          save_in = os.path.join(amostra_id_calculated_images_path, vegetation_index_image_name)
          index_image = getattr(vic, vegetation_index)()
          save_index_image(vic.profile, index_image, save_in)
        counter += 1
