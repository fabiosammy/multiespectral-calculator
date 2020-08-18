#!/usr/bin/env python2
# coding: utf-8

import sys
import os
import csv
import numpy as np
import caffe

from config import *

def show_progress(now, to):
  i = now * 100 / to
  sys.stdout.write('\r')
  sys.stdout.write("[%-20s] %d%%" % ('='*(i/5), i))
  sys.stdout.flush()

if __name__ == "__main__":
  # soil_properties = ['k', 'smp']
  # soil_properties = ['ca', 'cacl2', 'mg', 'p', 'al']
  soil_properties = ['k']

  for soil_property in soil_properties:
    deploy_prototxt = os.path.join('./models', soil_property, 'deploy.prototxt')
    caffe_model = os.path.join('./models', soil_property, 'snapshot_iter_86605.caffemodel')
    labels = os.path.join('./models', soil_property, 'labels.txt')
    mean = os.path.join('./models', soil_property, 'mean.binaryproto')


    caffe.set_mode_gpu()
    net = caffe.Net(deploy_prototxt, caffe_model, caffe.TEST)
    batch_size = 680
    net.blobs['data'].reshape(batch_size,3,227,227)

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    # transformer.set_mean('data', np.load(mean).mean(1).mean(1))
    transformer.set_transpose('data', (2,0,1))
    transformer.set_channel_swap('data', (2,1,0)) # if using RGB instead of BGR
    transformer.set_raw_scale('data', 255.0)

    label_mapping = np.loadtxt(labels, str, delimiter='\t')

    for amostra_category in os.listdir(os.path.join(to_classify_images_path, soil_property)):
      for amostra_id in os.listdir(os.path.join(to_classify_images_path, soil_property, amostra_category)):
        database_csv_file_path = './databases/classificator-{}-{}.csv'.format(str(soil_property), str(amostra_id))
        database_csv_file = open(database_csv_file_path, 'w')
        csv_writer = csv.writer(database_csv_file, delimiter=',')
        csv_writer.writerow(['soil_property','amostra_id','image_id','original_class','classified_class','precision','correct'])
        id_counter = 0
        len_combined_indexes = 328440
        batch_counter = 0
        csv_lines = []
        imgs = []

        for index_name_1 in os.listdir(os.path.join(to_classify_images_path, soil_property, amostra_category, amostra_id)):
          for image_name in os.listdir(os.path.join(to_classify_images_path, soil_property, amostra_category, amostra_id, index_name_1)):
            show_progress(id_counter, len_combined_indexes)
            load_image_path = os.path.join(to_classify_images_path, soil_property, amostra_category, amostra_id, index_name_1, image_name)

            img = caffe.io.load_image(load_image_path)
            imgs.append(transformer.preprocess('data', img))
            csv_lines.append([soil_property, amostra_id, image_name.replace('.png', ''), amostra_category])
            batch_counter += 1

            if batch_counter == batch_size:
              net.blobs['data'].data[...] = imgs
              output = net.forward()
              output_probs = output['softmax']

              output_prob_index = 0
              for output_prob in output_probs:
                top_inds = output_prob.argsort()[::-1][:5]
                csv_line = csv_lines[output_prob_index]
                csv_writer.writerow([
                  csv_line[0],
                  csv_line[1],
                  csv_line[2],
                  csv_line[3],
                  label_mapping[top_inds[0]],
                  round(output_prob[top_inds[0]], 3),
                  csv_line[3] == label_mapping[top_inds[0]]
                ])
                output_prob_index += 1

              imgs = None
              imgs = []
              csv_lines = None
              csv_lines = []

              batch_counter = 0

            id_counter += 1

        database_csv_file.close()

  print("done")
