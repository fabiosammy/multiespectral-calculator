#!/usr/bin/env python2
# coding: utf-8

import os
import csv
import numpy as np
import caffe

from config import *

if __name__ == "__main__":
  # soil_properties = ['k', 'smp']
  # soil_properties = ['ca', 'cacl2', 'mg', 'p', 'al']
  soil_properties = ['k']

  for soil_property in soil_properties:
    deploy_prototxt = os.path.join('./models', soil_property, 'deploy.prototxt')
    caffe_model = os.path.join('./models', soil_property, 'snapshot_iter_14435.caffemodel')
    labels = os.path.join('./models', soil_property, 'labels.txt')
    mean = os.path.join('./models', soil_property, 'mean.binaryproto')


    caffe.set_mode_gpu()
    net = caffe.Net(deploy_prototxt, caffe_model, caffe.TEST)
    net.blobs['data'].reshape(1,3,227,227)

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    # transformer.set_mean('data', np.load(mean).mean(1).mean(1))
    transformer.set_transpose('data', (2,0,1))
    transformer.set_channel_swap('data', (2,1,0)) # if using RGB instead of BGR
    transformer.set_raw_scale('data', 255.0)

    label_mapping = np.loadtxt(labels, str, delimiter='\t')

    for amostra_category in os.listdir(os.path.join(to_classify_images_path, soil_property)):
      for amostra_id in os.listdir(os.path.join(to_classify_images_path, soil_property, amostra_category)):

        database_csv_file_path = './databases/classificator-{}-{}.csv'.format(str(soil_property), str(amostra_id))
        print(database_csv_file_path)
        database_csv_file = open(database_csv_file_path, 'w')
        csv_writer = csv.writer(database_csv_file, delimiter=',')
        csv_writer.writerow(['soil_property','amostra_id','image_id','original_class','classified_class','precision','correct'])

        for image_name in os.listdir(os.path.join(to_classify_images_path, soil_property, amostra_category, amostra_id)):
          load_image_path = os.path.join(to_classify_images_path, soil_property, amostra_category, amostra_id, image_name)

          img = caffe.io.load_image(load_image_path)
          net.blobs['data'].data[...] = transformer.preprocess('data', img)
          output = net.forward()
          output_prob = output['softmax'][0]
          top_inds = output_prob.argsort()[::-1][:5]

          csv_writer.writerow([
            soil_property,
            amostra_id,
            image_name.replace('.png', ''),
            amostra_category,
            label_mapping[top_inds[0]],
            round(output_prob[top_inds[0]], 3),
            amostra_category == label_mapping[top_inds[0]]
          ])

        database_csv_file.close()

  print("done")
