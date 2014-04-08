

class Features(object):
    def __init__(self):
        self.__features = []

    def append(self, feature):
        self.__features.append(feature)

    def get_feature_arrays(self):
        """Returns a list imagepaths and a list of features"""
        imagepaths = []
        feature_arrays = []
        for f in self.__features:
            imagepaths.append(f.get_imagepath())
            feature_arrays.append(f.get_feature())
        return imagepaths, feature_arrays


class Feature(object):
    def __init__(self, imagepath, feature):
        self.__imagepath = imagepath
        self.__feature = feature

    def get_imagepath(self):
        #returns str
        return self.__imagepath

    def get_feature(self):
        #returns numpy.ndarray
        return self.__feature


class Extractor(object):
    def extract_features(obj, imagepaths):
        """Returns a list of Feature objects"""
        features = Features()
        for imagepath in imagepaths:
            #call a child class's method 
            feature = obj.extract(imagepath)
            features.append(feature)
        return features


class HistogramExtractor(Extractor):
    def __init__(self):
        pass

    def extract_features(self, imagepaths):
        return Extractor.extract_features(self, imagepaths)

    def extract(self, imagepath): 
        """Returns a Feature object"""
        import numpy as np
        import cv2
        image = imagepath.read_image()
        histogram = np.array([]) 
        for channel in cv2.split(image):
            h, bins = np.histogram(channel, bins=16, range=(0, 255), 
                                   normed=True)
            histogram = np.append(histogram, h)
        return Feature(imagepath, histogram)

        #histograms = np.array([])
        #for i in range(3):
        #    histogram = cv2.calcHist([image], [i], None, [256], [0,256])
        #    histograms = np.append(histograms, histogram.T[0])
        #return Feature(imagepath, histograms)


#class SurfExtractor(Extractor):
#    def extract_features(self, imagepaths):
#        return Extractor.extract_features(self, imagepaths)
#
#    def extract(self, imagepath):
#        return Feature(imagepath, None)
