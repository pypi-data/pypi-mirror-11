#
# ImageViewCanvasAgg.py -- A FITS image widget with canvas drawing in Agg
#
# Eric Jeschke (eric@naoj.org)
#
# Copyright (c) Eric R. Jeschke.  All rights reserved.
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
from ginga.aggw import ImageViewAgg
from ginga.canvas.mixins import DrawingMixin, CanvasMixin, CompoundMixin


class ImageViewCanvasError(ImageViewAgg.ImageViewAggError):
    pass

class ImageViewCanvas(ImageViewAgg.ImageViewAgg,
                      DrawingMixin, CanvasMixin, CompoundMixin):

    def __init__(self, logger=None, rgbmap=None, settings=None,
                 bindmap=None, bindings=None):
        ImageViewAgg.ImageViewAgg.__init__(self, logger=logger,
                                           rgbmap=rgbmap,
                                           settings=settings)
        CompoundMixin.__init__(self)
        CanvasMixin.__init__(self)
        DrawingMixin.__init__(self)

        for name in ('modified', ):
            self.enable_callback(name)

        #self.canvas.add(self)
        self.set_canvas(self)

        self.setSurface(self)

        # override
        self.defer_redraw = False

    def update_canvas(self, whence=3):
        self.logger.debug("updating canvas")
        self.redraw(whence=whence)

    def redraw_data(self, whence=0):
        super(ImageViewCanvas, self).redraw_data(whence=whence)

        if not self.surface:
            return
        self.draw(self)

    # subclass needs to implement these to avoid warning messages
    def reschedule_redraw(self, time_sec):
        pass

    def update_image(self):
        pass

    # METHODS THAT WERE IN IPG

    def add_canvas(self, tag=None):
        # add a canvas to the view
        DrawingCanvas = self.getDrawClass('drawingcanvas')
        canvas = DrawingCanvas()
        # enable drawing on the canvas
        canvas.enable_draw(True)
        canvas.ui_setActive(True)
        canvas.setSurface(self)
        # add the canvas to the view.
        self.add(canvas, tag=tag)
        return canvas

    def show(self):
        from IPython.display import Image
        return Image(data=bytes(self.get_rgb_image_as_bytes(format='png')),
                     format='png', embed=True)

#END
