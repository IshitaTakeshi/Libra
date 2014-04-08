import numpy as np
import wx

from wx.lib import scrolledpanel as scrolled

class Size(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = np.float64((width, height))


image_size = Size(100, 100)
scrolled_panel_size = Size(2000, 2000)
MAX_MAGNIFICATION = 20000
DEFAULT_MAGNIFICATION = 400
MIN_MAGNIFICATION = 20

#Controller
class ButtonsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#ededed')
        
        close_button = wx.Button(parent=self, label='close')
        save_button = wx.Button(parent=self, label='save')
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(close_button)
        vbox.Add(save_button)
    
        self.SetSizer(vbox)


#Controller
class MagnificationPanel(wx.Panel):
    def __init__(self, parent, changed_listener):
        wx.Panel.__init__(self, parent)
        slider = wx.Slider(parent=self, size=(200, -1), 
                           style=wx.SL_HORIZONTAL,
                           minValue=MIN_MAGNIFICATION, 
                           maxValue=MAX_MAGNIFICATION,
                           value=DEFAULT_MAGNIFICATION)

        slider.Bind(wx.EVT_SCROLL, changed_listener)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(slider, 0, wx.EXPAND)
        self.SetSizer(box)

        self.SetBackgroundColour('#FF00000')


#TODO scroll manually when images are appeared
class ScrolledPanel(wx.Panel):
    def __init__(self, parent, size, positions):
        wx.Panel.__init__(self, parent=parent, size=size)
        
        self.scrolled_panel = scrolled.ScrolledPanel(self, \
                        style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.scrolled_panel.SetAutoLayout(True)
        self.scrolled_panel.SetupScrolling()
        
        self.image_view_panel = ImageViewPanel(self.scrolled_panel, 
                                               size, positions)
        
        self.autosizer = wx.FlexGridSizer(cols=2)
        self.autosizer.SetFlexibleDirection(wx.VERTICAL)
        self.autosizer.Add(self.image_view_panel)
        self.scrolled_panel.SetSizer(self.autosizer)

        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(self.scrolled_panel, 1, wx.EXPAND)
        self.SetSizer(panel_sizer)

    def on_slider_scrolled(self, event):
        self.image_view_panel.on_slider_scrolled(event)


class PositionManager(object):
    def __init__(self, panel_center, position):
        self.__panel_center = panel_center
        self.__position = position

    def _slide_to_center(self, position):
        return position + self.__panel_center - (image_size.size/2)

    def get_zoomed(self, magnification):
        return self._slide_to_center(self.__position*magnification)


class BitmapManager(object):
    def __init__(self, imagepath, shape):
        image = wx.Image(imagepath)
        self.__bitmap = image.ConvertToBitmap() 
        self.__bitmap = self._resize(self.__bitmap, shape)

    def get(self):
        return self.__bitmap

    def _resize(self, bitmap, shape):
        x, y = shape
        width_old, height_old = bitmap.GetSize()
        if(x is not None and y is not None): 
            width  = x
            height = y
        elif(x is not None and y is None):
            width  = x
            height = int(x * (float(height_old) / width_old))    
        elif(x is None and y is not None):
            width  = int(y * (float(width_old) / height_old))
            height = y
        else:
            width = width_old
            height = height_old 

        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.BitmapFromImage(image)
        return bitmap


class ImagesManager(object):
    def __init__(self, positions, panel_center, shape):
        self.__magnification = DEFAULT_MAGNIFICATION

        self.__managers = []
        for imagepath, position in positions:
            bitmap_manager = BitmapManager(imagepath, shape)
            position_manager = PositionManager(panel_center, position)
            self.__managers.append((bitmap_manager, position_manager))

    def __iter__(self):
        b = []
        for bitmap_manager, position_manager in self.__managers:
            bitmap = bitmap_manager.get()
            position = position_manager.get_zoomed(self.__magnification)
            b.append((bitmap, position))
        return iter(b)

    def _clamp(self, x): 
        return max(MIN_MAGNIFICATION, min(MAX_MAGNIFICATION, x))
    
    def update_magnification(self, magnification):
        self.__magnification = self._clamp(magnification) 


class ImageViewPanel(wx.Panel):
    def __init__(self, parent, size, positions):
        wx.Panel.__init__(self, parent=parent, size=size)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        center = self._get_center()
        self.__manager = ImagesManager(positions, center, (100, None))
        
    def _get_center(self):
        size = self.GetSize()
        center = np.float64(size)/2
        return center

    def draw(self): 
        dc = wx.PaintDC(self)
        dc.Clear()
       
        for bitmap, position in self.__manager:
            x, y = position
            dc.DrawBitmap(bitmap, x, y, True)
            #wx.StaticBitmap(self, pos=position, bitmap=bitmap)
        
    def on_slider_scrolled(self, event):
        print("on_slider_scrolled")
        magnification = event.GetEventObject().GetValue()
        self.__manager.update_magnification(magnification)
        self.draw()

    def on_paint(self, event):
        print("on_paint")
        self.draw() 


class TopFrame(wx.Frame):
    def __init__(self, parent, title, positions, size=(640, 480)):
        wx.Frame.__init__(self, parent=parent, title=title, size=size)

        #self.scroll = wx.ScrolledWindow(self)
        buttons_panel = ButtonsPanel(self)
        scrolled_panel = ScrolledPanel(self, scrolled_panel_size.size, 
                                       positions)
        magnification_panel = \
                MagnificationPanel(self, scrolled_panel.on_slider_scrolled)
   
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(magnification_panel, 0, wx.EXPAND)
        vbox.Add(scrolled_panel, 1, wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(buttons_panel, 0, wx.EXPAND)
        hbox.Add(vbox, 1, wx.EXPAND)
        self.SetSizer(hbox) 


def show(positions):
    app = wx.App()
    frame = TopFrame(parent=None, title="Libra", positions=positions)
    frame.Show()

    """
    for i in range(10):
        manager = PositionsManager(positions, (0, 0))
        for imagepath, position in manager.get_zoomed_positions():
            print(imagepath, position)
    """
    app.MainLoop()
