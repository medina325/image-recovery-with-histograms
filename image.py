import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from heuristic import DistanceHeuristic as dh

class Image:
  """Represents an image with the properties required for the problem"""
  def __init__(self, filename: str, contents) -> None:
    self.filename = filename
    # self.contents = contents
    self.contents = np.array(contents, np.uint8)
    self.distances = {}

  def class_name(self) -> str:
    return self.filename.split('_')[0]

  def image_name(self) -> str:
    return self.filename.split('_')[1]

  def plot_histograms(self):
    x_axis = np.arange(256)

    def make_subplot(color, sub):
      plt.subplot(*sub)
      plt.bar(x_axis, self.histograms[color], width=0.9, color=color)
      plt.title(f'{color.capitalize()} Channel Histogram')
      plt.ylabel('Frequência')
      plt.xlabel('Valor')

    # plt.hist(x=self.contents[:, :, 1][0], bins='auto', color=color, alpha=0.7, rwidth=0.85)    
    make_subplot('red', (1,3,1))
    make_subplot('green', (1,3,2))
    make_subplot('blue', (1,3,3))
    
    plt.show()

class GrayImage(Image):
  def __init__(self, filename: str, contents) -> None:
    super().__init__(filename, contents)
    self.histograms = self.create_histograms()
    self.pdfs = self.create_pdfs()

  def create_histograms(self) -> dict:
    pixels = self.contents[:, :]
    
    return {
      'gray': np.array([np.sum(pixels == i) for i in range(256)])
    }

  def create_pdfs(self) -> dict:
    """Create Image's PDFs (Probability Density Function)"""
    
    return {
      'gray': self.histograms['gray'] / self.contents.size
    }

  def calc_pdfs_distances(self, img_pdfs, approach) -> None:
    """Calculate Image's PDF's distances to another Image's PDFs"""
    
    if (approach == dh.ED):
      self.distances = dh.euclidian_distance(img_pdfs, self.pdfs, True)
    elif (approach == dh.SC):
      self.distances = dh.square_chi(img_pdfs, self.pdfs, True)
      

class ColoredImage(Image):
  def __init__(self, filename: str, contents) -> None:
    super().__init__(filename, contents)
    self.histograms = self.create_histograms()
    self.pdfs = self.create_pdfs()

  def create_histograms(self) -> dict:
    # self.histograms['red'][self.contents[:, :, 0][0]] += 1
    # self.histograms['green'][self.contents[:, :, 1][0]] += 1
    # self.histograms['blue'][self.contents[:, :, 2][0]]+= 1
    red_pixels = self.contents[:, :, 0][0]
    green_pixels = self.contents[:, :, 1][0]
    blue_pixels = self.contents[:, :, 2][0]

    return {
      'red': np.array([np.sum(red_pixels == i) for i in range(256)]),
      'green': np.array([np.sum(green_pixels == i) for i in range(256)]),
      'blue': np.array([np.sum(blue_pixels == i) for i in range(256)])
    }

  def create_pdfs(self) -> dict:
    """Create Image's PDFs (Probability Density Function)"""

    img_size = self.contents.size

    return {
      'red': self.histograms['red'] / img_size,
      'green': self.histograms['green'] / img_size,
      'blue': self.histograms['blue'] / img_size
    }
  
  def calc_pdfs_distances(self, img_pdfs, approach) -> None:
    """Calculate Image's PDF's distances to another Image's PDFs"""
    
    if (approach == dh.ED):
      self.distances = dh.euclidian_distance(img_pdfs, self.pdfs, False)
    elif (approach == dh.SC):
      self.distances = dh.square_chi(img_pdfs, self.pdfs, False)
