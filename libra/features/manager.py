from libra.features import extractor, calculator

HISTOGRAM = "histogram"
#SURF = "surf"


class FeaturesManager(object):
    def __init__(self, feature_type, imagepaths):
        self.__manager = FeatureTypeManager(feature_type)
        self.__extractor = self.__manager.get_feature_extractor()
        self.__features = self.__extractor.extract_features(imagepaths)
    
    def calculate_positions(self):
        """Returns a Positions object"""
        distance_calculator = self.__manager.get_calculator()
        return calculator.ImagePositions(self.__features, distance_calculator)


class FeatureTypeManager(object):
    #make this class clean later
    def __init__(self, feature_type):
        #if feature_type is invalid)
        #    raise ValueError("Invalid feature type")
        self.__feature_type = feature_type

    def get_feature_extractor(self):
        """Returns an Extractor object"""
        if(self.__feature_type == HISTOGRAM):
            return extractor.HistogramExtractor()
        #if(self.__feature_type == feature_types.SURF):
        #    return SurfExtractor(imagepath).extract()
   
    def get_calculator(self):
        """Returns a function to calculate distances"""
        if(self.__feature_type == HISTOGRAM):
            return calculator.euclid

        #if(self.__feature_type == feature_types.SURF):
        #    return SurfExtractor(imagepath).extract()
