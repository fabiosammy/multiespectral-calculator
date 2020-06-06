#!/usr/bin/env python2
# coding: utf-8

import sys
import os
import csv
from itertools import chain, combinations
import rasterio
import numpy as np
import cv2

from vegetation_index_calculator import VegetationIndexCalculator
from config import *

def combinate_indexes(vegetation_indexes):
  # return [list(zip(x,list2)) for x in itertools.permutations(list1,len(list2))]
  # return chain(*[combinations(vegetation_indexes,i+1) for i,_ in enumerate(vegetation_indexes)])
  # return chain.from_iterable(combinations(vegetation_indexes, r) for r in range(len(vegetation_indexes)+1))
  return combinations(vegetation_indexes, 3)

def load_vegetation_indexes():
  vegetation_indexes = []
  for vegetation_index in dir(VegetationIndexCalculator):
    if vegetation_index not in VegetationIndexCalculator.exclude_methods():
      vegetation_indexes.append(vegetation_index)
  return vegetation_indexes

def load_index(amostra_id_calculated_images_path, index_name, amostra_id):
  image_name = index_name + '_0_default-' + amostra_id + '.tif'
  image_path = os.path.join(amostra_id_calculated_images_path, image_name)
  with rasterio.open(image_path) as src:
    index = src.read(1).astype('f4')
  return index

def save_index_image(profile, index_1, index_2, index_3, dst_file_path):
  cv2.normalize(index_1, index_1, 0, 255, cv2.NORM_MINMAX)
  cv2.normalize(index_2, index_3, 0, 255, cv2.NORM_MINMAX)
  cv2.normalize(index_2, index_3, 0, 255, cv2.NORM_MINMAX)
  with rasterio.open(dst_file_path, 'w', 
    count=profile['count'], crs=profile['crs'], dtype=profile['dtype'],
    driver=profile['driver'], width=profile['width'], height=profile['height']) as dst:
    dst.write_band(1, np.array(index_1, dtype = np.uint8))
    dst.write_band(2, np.array(index_2, dtype = np.uint8))
    dst.write_band(3, np.array(index_3, dtype = np.uint8))
  os.remove(dst_file_path + '.aux.xml') 

def show_progress(now, to):
  i = now * 100 / to
  sys.stdout.write('\r')
  sys.stdout.write("[%-20s] %d%%" % ('='*(i/5), i))
  sys.stdout.flush()

if __name__ == "__main__":
  vegetation_indexes = load_vegetation_indexes()
  combined_indexes = list(combinate_indexes(vegetation_indexes))

  for altitude in altitudes:
    for amostra_id in os.listdir(os.path.join(roi_images_path, altitude)):
      amostra_id_roi_images_path = os.path.join(roi_images_path, altitude, amostra_id)
      amostra_id_calculated_images_path = os.path.join(calculated_images_path, altitude, amostra_id)
      print(amostra_id_calculated_images_path)
      for image in os.listdir(amostra_id_roi_images_path):
        image_path = os.path.join(amostra_id_roi_images_path, image)
        print(image_path)
        vic = VegetationIndexCalculator(image_path)
        vic.profile.update({
          'count': 3,
          'interleave': None, 'dtype': 'uint8',
          'driver': u'PNG',
          'tiled': None,
          'nodata': None
        })

        id_counter = 1
        database_csv_file_path = './databases/{}-{}-combined-indexes.csv'.format(str(altitude), str(amostra_id))
        database_csv_file = open(database_csv_file_path, 'w')
        csv_writer = csv.writer(database_csv_file, delimiter=',')
        csv_writer.writerow(['id', 'amostra_id', 'index_1', 'index_2', 'index_3', 'file_path'])
        len_combined_indexes = len(combined_indexes)
        
        for combined_index in combined_indexes:
          show_progress(id_counter, len_combined_indexes)
          index_1 = load_index(amostra_id_calculated_images_path, combined_index[0], amostra_id)
          index_2 = load_index(amostra_id_calculated_images_path, combined_index[1], amostra_id)
          index_3 = load_index(amostra_id_calculated_images_path, combined_index[2], amostra_id)

          output_path = os.path.join(stacked_images_path, altitude, amostra_id)
          if not os.path.exists(output_path):
            os.makedirs(output_path)
          output_image_filename = str(id_counter) + '.png'
          output_path = os.path.join(output_path, output_image_filename)
          
          csv_writer.writerow([id_counter, amostra_id, combined_index[0], combined_index[1], combined_index[2], output_path])
          
          save_index_image(vic.profile, index_1, index_2, index_3, output_path)
          
          id_counter += 1
        database_csv_file.close()
