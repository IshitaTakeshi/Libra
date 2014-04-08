import os

supported_formats = [
    'pbm', 'pgm', 'ppm', 'tiff', 'jpeg', 'rast', 'bmp','png'
]

def find_imagefiles(dirpath):
    """
    Search all image files in a directory.
    Parameters
        dirpath: str
        A path to a directory.
    Returns
        out: ImagePaths 
        An ImagePaths object
    """

    return Finder().search_imagefiles(dirpath)


class ImagePaths(object):
    def __init__(self):
        self.__imagepaths = []

    def __str__(self):
        s = ""
        for imagepath in self.__imagepaths:
            s += "{}\n".format(imagepath)
        return s
        
    def __iter__(self):
        return iter(self.__imagepaths)

    def __getitem__(self, key):
        return self.__imagepaths[key]

    def __len__(self):
        return len(self.__imagepaths)

    def append(self, imagepath):
        self.__imagepaths.append(imagepath)


class ImagePath(object):
    def __init__(self, imagepath):
        """
        Parameters
            imagepath: str
            A path to an imagefile
        """
        self.__imagepath = imagepath

    def __str__(self):
        return self.__imagepath

    def get_str_path(self):
        return self.__imagepath

    def read_image(self):
        """Returns an image in numpy.ndarray"""
        import cv2
        return cv2.imread(self.__imagepath)

    def get_basename(self):
        return os.path.basename(self.__imagepath)


class Finder(object):
    def __init__(self):
        pass
     
    def _isimagefile(self, filepath):
        import imghdr
        image_format = imghdr.what(filepath)
        return image_format in supported_formats

    def _list_all_files(self, root_dirpath):
        paths = []
        for dirpath, dirname, filenames in os.walk(root_dirpath):
            paths += [os.path.join(dirpath, f) for f in filenames]
        return paths

    def search_imagefiles(self, dirpath):
        """Search all image files in a directory."""
        imagepaths = ImagePaths()
        for filepath in self._list_all_files(dirpath):
            if(self._isimagefile(filepath)):
                imagepaths.append(ImagePath(filepath))
        return imagepaths
