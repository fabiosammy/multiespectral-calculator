#!/usr/bin/env python2
# coding: utf-8

import os, shutil
import csv
import numpy as np

from config import *

import pprint

if __name__ == "__main__":
  soil_properties = None
  csv_memory_file = None
  with open('amostras-to-group.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    soil_properties = csv_reader.fieldnames
    soil_properties.remove('id')

  soil_values = {}
  for soil_property in soil_properties:
    soil_values[soil_property] = { 'values': [] }
    with open('amostras-to-group.csv', 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file, delimiter=',')
      for line in csv_reader:
        soil_values[soil_property]['values'].append(float(line[soil_property]))
    soil_values[soil_property]['min'] = min(soil_values[soil_property]['values'])
    soil_values[soil_property]['max'] = max(soil_values[soil_property]['values'])
    soil_values[soil_property]['stdev'] = np.std(np.array(soil_values[soil_property]['values']), ddof=1)
    soil_values[soil_property]['limiar-groups'] = []
    limiar_group = soil_values[soil_property]['min']
    counter = 1
    while limiar_group < soil_values[soil_property]['max']:
      soil_values[soil_property]['limiar-groups'].append({
        'id': counter, 
        'lim-inf': limiar_group, 
        'lim-sup': limiar_group + soil_values[soil_property]['stdev'],
        'amostras': []
      })
      limiar_group += soil_values[soil_property]['stdev']
      counter += 1

  for soil_property in soil_properties:
    with open('amostras-to-group.csv', 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file, delimiter=',')
      for line in csv_reader:
        for index, limiar_group in enumerate(soil_values[soil_property]['limiar-groups']):
          if float(line[soil_property]) >= limiar_group['lim-inf'] and float(line[soil_property]) < limiar_group['lim-sup']:
            soil_values[soil_property]['limiar-groups'][index]['amostras'].append(line['id'])
            break

  pp = pprint.PrettyPrinter()
  pp.pprint(soil_values)
  print("Copying...")

  for soil_property in soil_properties:
    soil_path = os.path.join(to_classify_images_path, soil_property)
    if not os.path.exists(soil_path):
      os.makedirs(soil_path)
    print(soil_property)
    for limiar_group in soil_values[soil_property]['limiar-groups']:
      limiar_soil_path = os.path.join(soil_path, "dv{}".format(limiar_group['id']))
      if os.path.exists(limiar_soil_path):
        shutil.rmtree(limiar_soil_path)
      os.makedirs(limiar_soil_path)
      print("{}: {}".format(limiar_group['id'], limiar_group['amostras']))
      
      for amostra_id in limiar_group['amostras']:
        src_images_path = os.path.join(stacked_images_path, '90m', amostra_id)
        if not os.path.exists(src_images_path):
          continue
        if not os.path.exists(limiar_soil_path):
          continue
        dst_images_path = os.path.join(limiar_soil_path, amostra_id)
        os.system("cp -R %s %s" % (src_images_path, dst_images_path))

  print("DONE")
