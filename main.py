#!/usr/bin/python2.7

# This is based on:
# * https://github.com/rasmusfenger/micasense_imageprocessing_sequoia
# * https://github.com/tpubben/SequoiaStacking
# * https://github.com/dobedobedo/Parrot_Sequoia_Image_Handler
# * https://github.com/GertS/pix4d_sequoia_sort
# * https://github.com/K-Adler/ParrotSequoiaReader

import os
from sequoia_stacker import stack_image

# Images ./images/agudos/sequoia/<altitude>/[Reg1, Reg2, Reg3]/*.TIFF
# Fazer o stacking em ./images/agudos/stacked/<altitude>/<region>/

if __name__ == "__main__":
  stacked_images_path = './images/agudos/stacked'
  images_path = './images/agudos/sequoia/'
  altitudes = ['10m', '30m', '60m', '90m']
  altitudes = ['90m']
  regions = ['Reg1', 'Reg2', 'Reg3']

  for altitude in altitudes:
    for region in regions:
      to_stack_images_path = os.path.join(images_path, altitude, region)
      images_list = sorted(os.listdir(to_stack_images_path))
      
      
      new_path = os.path.join(stacked_images_path, altitude, region)
      if not os.path.exists(new_path):
        os.makedirs(new_path)


      for i in range(len(images_list)/4):
        image_id = images_list[i*4].split('_')[3]
        print(image_id)
        # new_tiff_image = stack_image(images_list, to_stack_images_path, new_path, image_id)
        
