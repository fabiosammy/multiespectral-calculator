#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rasterio
import numpy as np
import matplotlib.pyplot as plt

class VegetationIndexCalculator:
  @staticmethod
  def exclude_methods():
    return [
      '__doc__', '__init__', '__module__',
      'exclude_methods', 'profile', 'mask',
      'green', 'red', 'red_edge', 'nir',
      'tiff_image_path', 'plotter'
    ]

  def __init__(self, tiff_image_path):
    self.tiff_image_path = tiff_image_path

    with rasterio.open(self.tiff_image_path) as src:
      self.profile = src.profile.copy()
      self.green = src.read(1).astype('f4')
      self.red = src.read(2).astype('f4')
      self.red_edge = src.read(3).astype('f4')
      self.nir = src.read(4).astype('f4')

    # generate mask image from red band
    self.mask = np.copy(self.red)
    self.mask[self.mask > 0.0] = 1.0 # all actual pixels have a value of 1.0
    self.mask[self.mask == 0.0] = 'nan' # border values have no value 'nan'

  def plotter(self, index_name, index):
    plt.figure()
    plt.imshow(index, cmap='RdYlGn')
    plt.colorbar()
    plt.title(index_name)
    plt.xlabel('Column #')
    plt.ylabel('Row #')
    plt.savefig('./plots/' + index_name + '.png')

  def ndvi(self):
    return (self.nir - self.red) / (self.nir + self.red)

  def atsavi(self):
    return 1.22 * ((self.nir-1.22*self.red-0.03) / (1.22*self.nir+self.red_edge-1.22*0.03+0.08*(1+1.22**2)))

  def ari(self):
    return (1/self.green) - (1/self.red)

  def avi(self):
    return 2.0*self.nir-self.red

  def arvi2(self):
    return -0.18+1.17*( (self.nir-self.red) / (self.nir+self.red) )

  def bri(self):
    return ((1.0/self.green) - (1.0/self.red_edge)) / (self.nir)

  # CARI is not clearly defined
  def cari(self):
    temp_a = (self.red_edge-self.green)/150.0
    temp_b = (self.green - (((self.red_edge-self.green)/150.0 )*550.0))
    return  (self.red_edge/self.red) * ( (np.sqrt( ( temp_a * 670.0 + self.red + temp_b )**2 ) ) / (np.sqrt(temp_a**2 + 1)) )

  def cari2(self):
    temp_a = (self.red_edge-self.green)/150.0
    return (self.red_edge/self.red) * ( np.absolute((temp_a*self.red+self.red)) / (np.sqrt(temp_a**2 + 1)) )

  def ccci(self):
    return ( (self.nir-self.red_edge)/(self.nir+self.red_edge) ) / ( (self.nir-self.red)/(self.nir+self.red) )

  def chlgreen(self):
    return (self.nir/self.green)**(-1)

  def chlrededge(self):
    return (self.nir/self.red_edge)**(-1)

  def cigreen(self):
    return (self.nir/self.green)-1.0

  def cirededge(self):
    return (self.nir/self.red_edge)-1.0

  def ctvi(self):
    return ((self.ndvi()+0.5)/(np.absolute(self.ndvi()+0.5)))+np.sqrt(np.absolute(self.ndvi()+0.5))

  def cvi(self):
    return self.nir*(self.red/self.green**2)

  def datt1(self):
    return (self.nir-self.red_edge)/(self.nir-self.red)

  def datt4(self):
    return self.red/(self.green*self.red_edge)

  def ddn(self):
    return 2*(self.red_edge-self.nir-self.nir)

  def diff1(self):
    return self.nir-self.green

  def diff2(self):
    return self.nir-self.red

  def dvimss(self):
    return 2.4*self.nir-self.red

  def evi2(self):
    return 2.4*( (self.nir-self.red) / (self.nir+self.red+1.0) )

  def evi22(self):
    return 2.5*( (self.nir-self.red) / (self.nir+2.4*self.red+1.0) )

  def fe3(self):
    return self.red/self.green

  def gemi(self):
    n_temp = ( 2*(self.nir**2 - self.red**2) + 1.5*self.nir+0.5*self.red ) / (self.nir+self.red+0.5)
    return (n_temp*(1-0.25*n_temp) - ( (self.red-0.125) / (1-self.red) ))

  def gndvi(self):
    return (self.nir-self.green) / (self.nir+self.green)

  def gosavi(self):
    return ((self.nir-self.green)/(self.nir+self.green+0.5))*(1+0.5)

  def grndvi(self):
    return (self.nir-(self.green+self.red)) / (self.nir+(self.green+self.red))

  # https://www.harrisgeospatial.com/docs/BroadbandGreenness.html
  def lai(self):
    return 3.618*self.evi22()-0.118

  def lci(self):
    return (self.nir-self.red_edge)/(self.nir-self.red)

  def logr(self):
    return np.log(self.nir/self.red)

  def maccioni(self):
    return (self.nir-self.red_edge)/(self.nir-self.red)

  def mari(self):
    return (self.green**(-1) - self.red_edge**(-1))*self.nir

  def mcari(self):
    return ((self.red_edge-self.red) - 0.2*(self.red_edge-self.green))*(self.red_edge/self.red)

  def mcari1(self):
    return 1.2* (2.5*(self.nir-self.red) - 1.3*(self.nir-self.green))

  def mcari2(self):
    return 1.5 * ( ( 1.2*(self.nir-self.green) - 2.5*(self.red-self.green) )/( np.sqrt( (2*self.nir+1)**2 - (6*self.nir-5*np.sqrt(self.red)) -0.5)))

  def msavi(self):
    return (2*self.nir+1-np.sqrt( (2*self.nir+1)**2 - 8*(self.nir-self.red))) / 2

  def msr670(self):
    return ((self.nir/self.red)-1) / (np.sqrt(((self.nir/self.red)-1)))

  def mtvi2(self):
    return 1.5 * ( ( 2.5*(self.nir-self.green) - 1.3*(self.red-self.green) )/( np.sqrt( (2*self.nir+1)**2 - (6*self.nir-5*np.sqrt(self.red)) -0.5)))

  def mgvi(self):
    return -0.386*self.green-0.530*self.red+0.535*self.red_edge+0.532*self.nir

  def mnsi(self):
    return 0.404*self.green-0.039*self.red-0.505*self.red_edge+0.762*self.nir

  def msbi(self):
    return 0.406*self.green+0.600*self.red+0.645*self.red_edge+0.243*self.nir

  def myvi(self):
    return 0.723*self.green-0.597*self.red+0.206*self.red_edge-0.278*self.nir

  def ndre(self):
    return (self.nir-self.red_edge) / (self.nir+self.red_edge)

  def ngrdi(self):
    return (self.green-self.red_edge) / (self.green+self.red_edge)

  def nli(self):
    return (self.nir**2 - self.red) / (self.nir**2 + self.red)

  def normg(self):
    return self.green/(self.nir+self.red+self.green)

  def normnir(self):
    return self.nir/(self.nir+self.red+self.green)

  def normr(self):
    return self.red/(self.nir+self.red+self.green)

  def osavi1(self):
    return (1 + 0.16) * (self.nir - self.red)/(self.nir + self.red + 0.16)

  def osavi2(self):
    return (1 + 0.16) * (self.nir - self.red_edge)/(self.nir + self.red_edge + 0.16)

  def pvr(self):
    return (self.green-self.red) / (self.green+self.red)

  def rdvi(self):
    return (self.nir-self.red) / (self.nir+self.red)**0.5

  def rededge2(self):
    return (self.nir-self.red_edge) / (self.nir+self.red_edge)

  # L = 0.5 muss nachrecherchiert werden (huete 1989)
  def savi(self):
    return ((self.nir-self.red) / (self.nir+self.red+0.5))*(1+0.5)

  def sbl(self):
    return self.nir- 2.4*self.red

  def spvi(self):
    return 0.4*( 3.7*(self.nir-self.red) - 1.2*np.absolute(self.green-self.red) )

  def tcari(self):
    return 3*( (self.red_edge-self.red) -0.2*(self.red_edge-self.green) *(self.red_edge/self.red))

  def tcari2(self):
    return 3*( (self.nir-self.red_edge) -0.2*(self.nir-self.green) *(self.nir/self.red_edge))

  def tcari_osavi(self):
    return self.tcari()/self.osavi1()

  def tci(self):
    return 1.2*(self.red_edge-self.green) -1.5*(self.red-self.green)+np.sqrt(self.red_edge/self.red)

  def tvi(self):
    return np.sqrt(((self.nir-self.red) / (self.nir+self.red))+0.5)

  def tc_gvimss(self):
    return -0.283*self.green-0.660*self.red+0.577*self.red_edge+0.388*self.nir

  def tc_nsimss(self):
    return -0.016*self.green+0.131*self.red-0.425*self.red_edge+0.882*self.nir

  def tc_sbimss(self):
    return 0.332*self.green+0.603*self.red+0.675*self.red_edge+0.262*self.nir

  def tc_yvimss(self):
    return -0.899*self.green+0.428*self.red+0.076*self.red_edge-0.041*self.nir

  def varirededge(self):
    return (self.red_edge-self.red) / (self.red_edge+self.red)

  def wdrvi(self):
    return (0.1*self.nir-self.red)/(0.1*self.nir+self.red)

  def mcari_mtvi2(self):
    return self.mcari()/self.mtvi2()

  def mcari_osavi(self):
    return self.mcari()/self.osavi2()
