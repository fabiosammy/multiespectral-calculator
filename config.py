#!/usr/bin/env python2
# coding: utf-8

csv_database = 'amostras-table-database.csv'

# Images ./images/agudos/sequoia/<altitude>/[Reg1, Reg2, Reg3]/*.TIFF
# Fazer o stacking com correções de alinhamento em ./images/agudos/01-stacked/<altitude>/[Reg1, Reg2, Reg3]/
# Copiar selecionadas para ./images/agudos/02-selected/<altitude>/<amostra-id>/
# Fazer recortes em ./images/agudos/03-roi/<altitude>/amostra-id/<roi-counter>.TIF
# Calcular os indices e criar a stack em ./images/agudos/04-calculated/<altitude>/amostra-id/<roi-counter>.TIF
# Criar a augmentation base em ./images/agudos/05-augmentation/<altitude>/amostra-id/<roi-counter>.TIF
# Criar as classes em ./images/agudos/06-to-classify/<class-agrupation>/<new-counter>.TIF

images_path = './images/agudos/sequoia/'
# altitudes = ['10m', '30m', '60m', '90m']
altitudes = ['90m']
regions = ['Reg1', 'Reg2', 'Reg3']
stacked_images_path = './images/agudos/01-stacked'
selected_images_path = './images/agudos/02-selected'
roi_images_path = './images/agudos/03-roi'
calculated_images_path = './images/agudos/04-calculated'
augmentation_images_path = './images/agudos/05-calculated'
to_classify_images_path = './images/agudos/06-to-classify'
