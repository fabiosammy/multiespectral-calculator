#!/usr/bin/env python2
# coding: utf-8

csv_database = 'amostras-table-database.csv'

# Images ./images/agudos/sequoia/<altitude>/[Reg1, Reg2, Reg3]/*.TIFF
# Alinhas as imagens e junstá-las em ./images/agudos/01-aligned/<altitude>/[Reg1, Reg2, Reg3]/
# Copiar selecionadas para ./images/agudos/02-selected/<altitude>/<amostra-id>/
# Fazer recortes em ./images/agudos/03-roi/<altitude>/amostra-id/<roi-counter>.TIF
# Calcular os indices e criar cada em imagem ./images/agudos/04-calculated/<altitude>/amostra-id/<roi-counter>.TIF
# Criar as stacks de combinações de indices em ./images/agudos/05-stacked/<altitude>/amostra-id/<roi-counter>.TIF
# Criar a augmentation base em ./images/agudos/06-augmentation/<altitude>/amostra-id/<roi-counter>.TIF
# Criar as classes em ./images/agudos/07-to-classify/<class-agrupation>/<new-counter>.TIF

captured_region = 'vo'

images_path = './images/' + captured_region + '/sequoia/'
# altitudes = ['10m', '30m', '60m', '90m']
altitudes = ['90m']
regions = ['Reg1', 'Reg2', 'Reg3']
aligned_images_path      = './images/' + captured_region + '/01-aligned'
selected_images_path     = './images/' + captured_region + '/02-selected'
roi_images_path          = './images/' + captured_region + '/03-roi'
calculated_images_path   = './images/' + captured_region + '/04-calculated'
stacked_images_path      = './images/' + captured_region + '/05-stacked'
augmentation_images_path = './images/' + captured_region + '/06-augmentation'
to_classify_images_path  = './images/' + captured_region + '/07-to-classify'
