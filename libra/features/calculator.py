import numpy as np

def euclid(p1, p2):
    return np.linalg.norm(p2-p1)


class ImagePositions(object):
    """This class has a list of positions of each image on a screen 
       calculated by Multi Dimensional Scaling."""
    def __init__(self, features, distance):
        """
        Parameters 
            features: A Features object.
            distance: A function pointer to define the distance between
            features.
        """
        self.__distance = distance
        imagepaths, feature_arrays = features.get_feature_arrays()
        distances = self._distances(feature_arrays)
        positions = self._calculate_mds_positions(distances)
        self.__positions = zip(imagepaths, positions)

    def __str__(self):
        import os
        s = ""
        for imagepath, position in self.__positions:
            s += "{} is at {}\n".format(imagepath.get_basename(), position)
        return s

    def __iter__(self):
        """
        Returns an iterator which its element contains an image path and
        its position.
        imagepath: str
        position: numpy.ndarray
        """
        p = [(path.get_str_path(), pos) for path, pos in self.__positions]
        return iter(p)

    def _distances(self, arrays):
        lenarrays = len(arrays)
        distances = np.zeros((lenarrays, lenarrays))
        for i in range(lenarrays):
            for j in range(lenarrays):
                distances[i][j] = self.__distance(arrays[i], arrays[j])
        return distances

    def _calculate_mds_positions(self, similarities):
        from sklearn import manifold
        mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, 
                dissimilarity="precomputed", n_jobs=1)
        positions = mds.fit(similarities).embedding_
        return positions
