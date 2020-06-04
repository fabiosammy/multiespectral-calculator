#!/usr/bin/env python
# coding: utf-8

# Images ./images/agudos/sequoia/<altitude>/[Reg1, Reg2, Reg3]/*.TIFF
# Mover para ./images/agudos/selected/<altitude>/<amostra-id>/
# Fazer o stacking em ./images/agudos/stitched/<altitude>/<amostra-id>/
# Fazer recortes em ./images/agudos/roi/<altitude>/amostra-id/

import os
import csv
import exiftool
from geopy import distance
from shutil import copy2

def match_image_point(amostra, altitude, image_data):
  amostra_location = [amostra['latitude'], amostra['longitude']]
  image_location = [image_data['Composite:GPSLatitude'], image_data['Composite:GPSLongitude']]
  # TODO: Considerer the altitude to the maximum distance
  return distance.geodesic(amostra_location, image_location).m <= 100.0

if __name__ == "__main__":
  csv_database = 'amostras-table-database.csv'

  # Read csv to memory
  csv_reader = ''
  with open(csv_database, mode='r') as csv_file:
    csv_memory_file = csv_file.read()
  csv_reader = csv.DictReader(csv_memory_file.splitlines(), delimiter=',')

  for amostra in csv_reader:
    # Read each image
    selected_images_path = './images/agudos/selected'
    images_path = './images/agudos/sequoia/'
    altitudes = ['10m', '30m', '60m', '90m']
    altitudes = ['90m']
    regions = ['Reg1', 'Reg2', 'Reg3']

    for altitude in altitudes:
      # Ignore amostras selecteds
      new_path = os.path.join(selected_images_path, altitude, amostra['id'])
      print("Selecting {}...".format(new_path))
      if not os.path.exists(new_path):
        os.makedirs(new_path)
      else:
        counter = len(os.listdir(new_path))
        print("Amostra: {} | Altitude: {} | selected images: {} - jumped".format(amostra['id'], altitude, counter))
        continue
      # if amostra['selected'] != 'true':
      #   print("Ignore amostra:{}".format(amostra['id']))
      #   continue

      counter = 0
      for region in regions:
        region_images_path = os.path.join(images_path, altitude, region)
        for image in os.listdir(region_images_path):
          # Ignore non TIF images
          image_ext = image.split('.')
          if len(image_ext) < 2 or image_ext[1] != 'TIF':
            continue

          image_full_path = os.path.join(region_images_path, image)

          # Read metadata of image
          image_data = ''
          with exiftool.ExifTool() as et:
            image_data = et.get_metadata(image_full_path)

          # Check the distance and select/copy
          if match_image_point(amostra, altitude, image_data):
            copy2(image_full_path, new_path)
            counter += 1

      print("Amostra: {} | Altitude: {} | selected images: {}".format(amostra['id'], altitude, counter))
      # exit(1)
  
