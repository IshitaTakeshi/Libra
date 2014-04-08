import os
import sys

from libra.files import finder
from libra.features import manager 
from libra.view import view

#home = os.path.expanduser('~')
#dirpath = os.path.join(home, 'Pictures/Miku')
dirpath = sys.argv[1]
imagepaths = finder.find_imagefiles(dirpath)
print(imagepaths)
features_manager = manager.FeaturesManager(manager.HISTOGRAM, imagepaths)
positions = features_manager.calculate_positions()
print(positions)
for imagepath, position in positions:
    print("{} {}".format(imagepath, position))
#view.show(positions)#positions)
view.show(positions)
