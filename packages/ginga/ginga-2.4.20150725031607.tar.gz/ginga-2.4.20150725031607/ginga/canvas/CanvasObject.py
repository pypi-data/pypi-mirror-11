#
# CanvasObject.py -- classes for shapes drawn on ginga canvases.
#
# Eric Jeschke (eric@naoj.org)
#
# Copyright (c) Eric R. Jeschke.  All rights reserved.
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
import math
import numpy
# for BezierCurve
from collections import OrderedDict

from ginga.misc import Callback, Bunch
from ginga.misc.ParamSet import Param
from ginga.util import wcs
from ginga import trcalc, Mixins, colors
from ginga.util.six.moves import map, filter

from .CompoundMixin import CompoundMixin
from .CanvasMixin import CanvasMixin
from .DrawingMixin import DrawingMixin
from . import coordmap

colors_plus_none = [ None ] + colors.get_colors()

class CanvasObjectError(Exception):
    pass

class CanvasObjectBase(Callback.Callbacks):
    """This is the abstract base class for a CanvasObject.  A CanvasObject
    is an item that can be placed on a ImageViewCanvas.

    This class defines common methods used by all such objects.
    """

    def __init__(self, **kwdargs):
        if not hasattr(self, 'cb'):
            Callback.Callbacks.__init__(self)
        self.editing = False
        self.cap = 'ball'
        self.cap_radius = 4
        self.editable = True
        self.coord = 'data'
        self.ref_obj = None
        self.__dict__.update(kwdargs)
        self.data = None
        # default mapping is to data coordinates
        self.crdmap = None

        # For callbacks
        for name in ('modified', ):
            self.enable_callback(name)

    def initialize(self, tag, viewer, logger):
        self.tag = tag
        self.viewer = viewer
        self.logger = logger
        if self.crdmap is None:
            if self.coord == 'offset':
                self.crdmap = coordmap.OffsetMapper(viewer, self.ref_obj)
            else:
                self.crdmap = viewer.get_coordmap(self.coord)

    def is_editing(self):
        return self.editing

    def set_edit(self, tf):
        if not self.editable:
            raise ValueError("Object is not editable")
        self.editing = tf
        # TODO: force redraw here to show edit nodes?

    def set_data(self, **kwdargs):
        if self.data is None:
            self.data = Bunch.Bunch(kwdargs)
        else:
            self.data.update(kwdargs)

    def get_data(self, *args):
        if len(args) == 0:
            return self.data
        elif len(args) == 1:
            return self.data[args[0]]
        elif len(args) == 2:
            try:
                return self.data[args[0]]
            except KeyError:
                return args[1]
        else:
            raise CanvasObjectError("method get_data() takes at most 2 arguments")

    def use_coordmap(self, mapobj):
        self.crdmap = mapobj

    def canvascoords(self, viewer, x, y, center=True):
        # if object has a valid coordinate map, use it
        crdmap = self.crdmap
        if crdmap is None:
            # otherwise get viewer's default one
            crdmap = viewer.get_coordmap('data')

        # convert coordinates to data coordinates
        data_x, data_y = crdmap.to_data(x, y)

        # finally, convert to viewer's canvas coordinates
        return viewer.get_canvas_xy(data_x, data_y, center=center)

    ## def canvascoords(self, viewer, x, y, center=True):
    ##     crdmap = viewer.get_coordmap(self.coord)

    ##     # convert coordinates to data coordinates
    ##     data_x, data_y = crdmap.to_data(x, y)

    ##     # finally, convert to viewer's canvas coordinates
    ##     return viewer.get_canvas_xy(data_x, data_y, center=center)

    def is_compound(self):
        return False

    def contains_arr(self, x_arr, y_arr):
        contains = numpy.array([False] * len(x_arr))
        return contains

    def contains(self, x, y):
        return False

    def select_contains(self, viewer, x, y):
        return self.contains(x, y)

    def draw_arrowhead(self, cr, x1, y1, x2, y2):
        i1, j1, i2, j2 = self.calcVertexes(x1, y1, x2, y2)

        alpha = getattr(self, 'alpha', 1.0)
        cr.set_fill(self.color, alpha=alpha)
        cr.draw_polygon(((x2, y2), (i1, j1), (i2, j2)))
        cr.set_fill(None)

    def draw_caps(self, cr, cap, points, radius=None, isedit=False):
        i = 0
        for cx, cy in points:
            if radius is None:
                radius = self.cap_radius
            alpha = getattr(self, 'alpha', 1.0)
            if cap == 'ball':
                # Draw move control point in a different color than the others
                # (move cp is always cp #0)
                if (i == 0) and isedit:
                    # TODO: configurable
                    color = 'orangered'
                else:
                    color = self.color

                cr.set_fill(color, alpha=alpha)
                cr.draw_circle(cx, cy, radius)
                #cr.set_fill(self, None)
            i += 1

    def draw_edit(self, cr, viewer):
        cpoints = self.get_cpoints(viewer, points=self.get_edit_points())
        self.draw_caps(cr, 'ball', cpoints, isedit=True)

    def calc_radius(self, viewer, x1, y1, radius):
        # scale radius
        cx1, cy1 = self.canvascoords(viewer, x1, y1)
        cx2, cy2 = self.canvascoords(viewer, x1, y1 + radius)
        # TODO: the accuracy of this calculation of radius might be improved?
        cradius = math.sqrt(abs(cy2 - cy1)**2 + abs(cx2 - cx1)**2)
        return (cx1, cy1, cradius)

    def calcVertexes(self, start_cx, start_cy, end_cx, end_cy,
                     arrow_length=10, arrow_degrees=0.35):

        angle = math.atan2(end_cy - start_cy, end_cx - start_cx) + math.pi

        cx1 = end_cx + arrow_length * math.cos(angle - arrow_degrees);
        cy1 = end_cy + arrow_length * math.sin(angle - arrow_degrees);
        cx2 = end_cx + arrow_length * math.cos(angle + arrow_degrees);
        cy2 = end_cy + arrow_length * math.sin(angle + arrow_degrees);

        return (cx1, cy1, cx2, cy2)

    def swapxy(self, x1, y1, x2, y2):
        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1
        return (x1, y1, x2, y2)

    def scale_font(self, viewer):
        zoomlevel = viewer.get_zoom()
        if zoomlevel >= -4:
            return 14
        elif zoomlevel >= -6:
            return 12
        elif zoomlevel >= -8:
            return 10
        else:
            return 8

    def rotate(self, theta, xoff=0, yoff=0):
        if hasattr(self, 'x'):
            self.x, self.y = self.crdmap.rotate_pt(self.x, self.y, theta,
                                                   xoff=xoff, yoff=yoff)
        elif hasattr(self, 'x1'):
            self.x1, self.y1 = self.crdmap.rotate_pt(self.x1, self.y1, theta,
                                                     xoff=xoff, yoff=yoff)
            self.x2, self.y2 = self.crdmap.rotate_pt(self.x2, self.y2, theta,
                                                     xoff=xoff, yoff=yoff)
        elif hasattr(self, 'points'):
            self.points = list(map(
                lambda p: self.crdmap.rotate_pt(p[0], p[1], theta,
                                                xoff=xoff, yoff=yoff),
                self.points))

    def rotate_by(self, theta_deg):
        ref_x, ref_y = self.get_reference_pt()
        self.rotate(theta_deg, xoff=ref_x, yoff=ref_y)

    def move_delta(self, xoff, yoff):
        if hasattr(self, 'x'):
            self.x, self.y = self.crdmap.offset_pt((self.x, self.y), xoff, yoff)

        elif hasattr(self, 'x1'):
            self.x1, self.y1 = self.crdmap.offset_pt((self.x1, self.y1), xoff, yoff)
            self.x2, self.y2 = self.crdmap.offset_pt((self.x2, self.y2), xoff, yoff)

        elif hasattr(self, 'points'):
            for i in range(len(self.points)):
                self.points[i] = self.crdmap.offset_pt(self.points[i], xoff, yoff)

    def move_to(self, xdst, ydst):
        x, y = self.get_reference_pt()
        return self.move_delta(xdst - x, ydst - y)

    def get_num_points(self):
        if hasattr(self, 'x'):
            return 1
        elif hasattr(self, 'x1'):
            return 2
        elif hasattr(self, 'points'):
            return(len(self.points))
        else:
            return 0

    def set_point_by_index(self, i, pt):
        if hasattr(self, 'points'):
            self.points[i] = pt
        elif i == 0:
            if hasattr(self, 'x'):
                self.x, self.y = pt
            elif hasattr(self, 'x1'):
                self.x1, self.y1 = pt
        elif i == 1:
            self.x2, self.y2 = pt
        else:
            raise ValueError("No point corresponding to index %d" % (i))

    def get_point_by_index(self, i):
        if hasattr(self, 'points'):
            return self.points[i]
        elif i == 0:
            if hasattr(self, 'x'):
                return self.x, self.y
            elif hasattr(self, 'x1'):
                return self.x1, self.y1
        elif i == 1:
            return self.x2, self.y2
        else:
            raise ValueError("No point corresponding to index %d" % (i))

    def scale_by(self, scale_x, scale_y):
        if hasattr(self, 'radius'):
            self.radius *= max(scale_x, scale_y)

        elif hasattr(self, 'xradius'):
            self.xradius *= scale_x
            self.yradius *= scale_y

        elif hasattr(self, 'x1'):
            ctr_x, ctr_y = self.get_center_pt()
            pts = [(self.x1, self.y1), (self.x2, self.y2)]
            P = numpy.array(pts)
            P[:, 0] = (P[:, 0] - ctr_x) * scale_x + ctr_x
            P[:, 1] = (P[:, 1] - ctr_y) * scale_y + ctr_y
            self.x1, self.y1 = P[0, 0], P[0, 1]
            self.x2, self.y2 = P[1, 0], P[1, 1]

        elif hasattr(self, 'points'):
            ctr_x, ctr_y = self.get_center_pt()
            P = numpy.array(self.points)
            P[:, 0] = (P[:, 0] - ctr_x) * scale_x + ctr_x
            P[:, 1] = (P[:, 1] - ctr_y) * scale_y + ctr_y
            self.points = list(P)

    def convert_mapper(self, tomap):
        """
        Converts our object from using one coordinate map to another.

        NOTE: This is currently NOT WORKING, because radii are not
        converted correctly.
        """
        frommap = self.crdmap
        if frommap == tomap:
            return

        # convert radii
        if hasattr(self, 'radius'):
            xc, yc = self.get_center_pt()
            # get data coordinates of a point radius away from center
            # under current coordmap
            x1, y1 = frommap.to_data(xc, yc)
            x2, y2 = frommap.to_data(xc + self.radius, yc)
            x3, y3 = frommap.to_data(xc, yc + self.radius)
            # now convert these data coords to native coords in tomap
            nx1, ny1 = tomap.data_to(x1, y1)
            nx2, ny2 = tomap.data_to(x2, y2)
            nx3, ny3 = tomap.data_to(x3, y3)
            # recalculate radius using new coords
            self.radius = math.sqrt((nx2 - nx1)**2 + (ny3 - ny1)**2)

        elif hasattr(self, 'xradius'):
            # similar to above case, but there are 2 radii
            xc, yc = self.get_center_pt()
            x1, y1 = frommap.to_data(xc, yc)
            x2, y2 = frommap.to_data(xc + self.xradius, yc)
            x3, y3 = frommap.to_data(xc, yc + self.yradius)
            nx1, ny1 = tomap.data_to(x1, y1)
            nx2, ny2 = tomap.data_to(x2, y2)
            nx3, ny3 = tomap.data_to(x3, y3)
            self.xradius = math.fabs(nx2 - nx1)
            self.yradius = math.fabs(ny3 - ny1)

        # convert points
        for i in range(self.get_num_points()):
            # convert each point by going to data coords under old map
            # and then to native coords in the new map
            x, y = self.get_point_by_index(i)
            data_x, data_y = frommap.to_data(x, y)
            new_x, new_y = tomap.data_to(data_x, data_y)
            self.set_point_by_index(i, (new_x, new_y))

        # set our map to the new map
        self.crdmap = tomap

    # TODO: move these into utility module?
    #####
    def point_within_radius(self, a_arr, b_arr, x, y, canvas_radius,
                            scale_x=1.0, scale_y=1.0):
        """Point (a, b) and point (x, y) are in data coordinates.
        Return True if point (a, b) is within the circle defined by
        a center at point (x, y) and within canvas_radius.
        """
        dx = numpy.fabs(x - a_arr) * scale_x
        dy = numpy.fabs(y - b_arr) * scale_y
        new_radius = numpy.sqrt(dx**2 + dy**2)
        res = (new_radius <= canvas_radius)
        return res

    def within_radius(self, viewer, a_arr, b_arr, x, y, canvas_radius):
        """Point (a, b) and point (x, y) are in data coordinates.
        Return True if point (a, b) is within the circle defined by
        a center at point (x, y) and within canvas_radius.
        The distance between points is scaled by the canvas scale.
        """
        scale_x, scale_y = viewer.get_scale_xy()
        return self.point_within_radius(a_arr, b_arr, x, y, canvas_radius,
                                        scale_x=scale_x, scale_y=scale_y)

    def get_pt(self, viewer, points, x, y, canvas_radius=None):
        if canvas_radius is None:
            canvas_radius = self.cap_radius

        if hasattr(self, 'rot_deg'):
            # rotate point back to cartesian alignment for test
            ctr_x, ctr_y = self.crdmap.to_data(*self.get_center_pt())
            xp, yp = trcalc.rotate_pt(x, y, -self.rot_deg,
                                      xoff=ctr_x, yoff=ctr_y)
        else:
            xp, yp = x, y

        # TODO: do this using numpy array()
        for i in range(len(points)):
            a, b = points[i]
            if self.within_radius(viewer, xp, yp, a, b, canvas_radius):
                return i
        return None

    def point_within_line(self, a_arr, b_arr, x1, y1, x2, y2,
                          canvas_radius):
        # TODO: is there an algorithm with the cross and dot products
        # that is more efficient?
        r = canvas_radius
        xmin, xmax = min(x1, x2) - r, max(x1, x2) + r
        ymin, ymax = min(y1, y2) - r, max(y1, y2) + r
        div = numpy.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        d = numpy.fabs((x2 - x1)*(y1 - b_arr) - (x1 - a_arr)*(y2 - y1)) / div

        ## contains = (xmin <= a_arr <= xmax) and (ymin <= b_arr <= ymax) and \
        ##            (d <= canvas_radius)
        contains = numpy.logical_and(
            numpy.logical_and(xmin <= a_arr, a_arr <= xmax),
            numpy.logical_and(d <= canvas_radius,
                              numpy.logical_and(ymin <= b_arr, b_arr <= ymax)))
        return contains

    def within_line(self, viewer, a_arr, b_arr, x1, y1, x2, y2,
                    canvas_radius):
        """Point (a, b) and points (x1, y1), (x2, y2) are in data coordinates.
        Return True if point (a, b) is within the line defined by
        a line from (x1, y1) to (x2, y2) and within canvas_radius.
        The distance between points is scaled by the canvas scale.
        """
        scale_x, scale_y = viewer.get_scale_xy()
        new_radius = canvas_radius * 1.0 / min(scale_x, scale_y)
        return self.point_within_line(a_arr, b_arr, x1, y1, x2, y2,
                                         new_radius)

    #####

    def get_points(self):
        return []

    def get_center_pt(self):
        # default is geometric average of points
        P = numpy.array(self.get_points())
        x = P[:, 0]
        y = P[:, 1]
        Cx = numpy.sum(x) / float(len(x))
        Cy = numpy.sum(y) / float(len(y))
        return (Cx, Cy)

    def get_reference_pt(self):
        return self.get_center_pt()

    def get_cpoints(self, viewer, points=None):
        if points is None:
            points = self.get_points()
        if hasattr(self, 'rot_deg') and self.rot_deg != 0.0:
            # rotate vertices according to rotation
            x, y = self.get_center_pt()
            rpoints = tuple(map(lambda p: self.crdmap.rotate_pt(p[0], p[1],
                                                                self.rot_deg,
                                                                xoff=x, yoff=y),
                                points))
        else:
            rpoints = points
        cpoints = tuple(map(lambda p: self.canvascoords(viewer, p[0], p[1]),
                            rpoints))
        return cpoints


#
#   ==== BASE CLASSES FOR GRAPHICS OBJECTS ====
#
class Text(CanvasObjectBase):
    """Draws text on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates in the data space
    text: the text to draw
    Optional parameters for fontsize, color, etc.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            Param(name='x', type=float, default=0.0, argpos=0,
                  description="X coordinate of lower left of text"),
            Param(name='y', type=float, default=0.0, argpos=1,
                  description="Y coordinate of lower left of text"),
            Param(name='text', type=str, default='EDIT ME',
                  description="Text to display"),
            Param(name='font', type=str, default='Sans Serif',
                  description="Font family for text"),
            Param(name='fontsize', type=int, default=None,
                  min=8, max=72,
                  description="Font size of text (default: vary by scale)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='yellow',
                  description="Color of text"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of text"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            ]

    def __init__(self, x, y, text='EDIT ME',
                 font='Sans Serif', fontsize=None,
                 color='yellow', alpha=1.0, showcap=False, **kwdargs):
        self.kind = 'text'
        super(Text, self).__init__(color=color, alpha=alpha,
                                       x=x, y=y, font=font, fontsize=fontsize,
                                       text=text, showcap=showcap, **kwdargs)

    def get_center_pt(self):
        return (self.x, self.y)

    def select_contains(self, viewer, x, y):
        return self.within_radius(viewer, x, y, self.x, self.y,
                                  self.cap_radius)

    def get_points(self):
        return [self.get_center_pt()]

    def set_edit_point(self, i, pt):
        if i == 0:
            self.set_point_by_index(i, pt)
        else:
            raise ValueError("No point corresponding to index %d" % (i))

    def get_edit_points(self):
        # TODO: edit point for scaling or rotating?
        return [(self.x, self.y)]

    def draw(self, viewer):
        cr = viewer.renderer.setup_cr(self)
        cr.set_font_from_shape(self)

        cx, cy = self.canvascoords(viewer, self.x, self.y)
        cr.draw_text(cx, cy, self.text)

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, ((cx, cy), ))


class PolygonMixin(object):
    """Mixin for polygon-based objects.
    """

    def get_center_pt(self):
        P = numpy.array(self.points + [self.points[0]])
        x = P[:, 0]
        y = P[:, 1]

        a = x[:-1] * y[1:]
        b = y[:-1] * x[1:]
        A = numpy.sum(a - b) / 2.

        cx = x[:-1] + x[1:]
        cy = y[:-1] + y[1:]

        Cx = numpy.sum(cx * (a - b)) / (6. * A)
        Cy = numpy.sum(cy * (a - b)) / (6. * A)
        return (Cx, Cy)

    def get_points(self):
        return self.points

    def get_llur(self):
        points = numpy.array(list(map(lambda pt: self.crdmap.to_data(pt[0], pt[1]),
                                 self.get_points())))
        t_ = points.T
        x1, y1 = t_[0].min(), t_[1].min()
        x2, y2 = t_[0].max(), t_[1].max()
        return (x1, y1, x2, y2)

    def contains_arr(self, x_arr, y_arr):
        # NOTE: we use a version of the ray casting algorithm
        # See: http://alienryderflex.com/polygon/
        xi = x_arr.reshape(-1)
        yi = y_arr.reshape(-1)
        xa, ya = numpy.meshgrid(xi, yi)

        result = numpy.empty(ya.shape, dtype=numpy.bool)
        result.fill(False)

        xj, yj = self.crdmap.to_data(*self.points[-1])
        for point in self.points:
            xi, yi = self.crdmap.to_data(*point)
            tf = numpy.logical_and(
                numpy.logical_or(numpy.logical_and(yi < ya, yj >= ya),
                                 numpy.logical_and(yj < ya, yi >= ya)),
                numpy.logical_or(xi <= xa, xj <= xa))
            # TODO: get a divide by zero here for some elements whose tf=False
            # Need to figure out a way to conditionally do those w/tf=True
            cross = (xi + (ya - yi).astype(numpy.float)/(yj - yi)*(xj - xi)) < xa
            result[tf == True] ^= cross[tf == True]
            xj, yj = xi, yi

        return result

    def contains(self, xp, yp):
        x_arr, y_arr = numpy.array([xp]), numpy.array([yp])
        res = self.contains_arr(x_arr, y_arr)
        return res[0]

    def set_edit_point(self, i, pt):
        if i == 0:
            x, y = pt
            self.move_to(x, y)
        elif i-1 < len(self.points):
            self.set_point_by_index(i-1, pt)
        else:
            raise ValueError("No point corresponding to index %d" % (i))

    def get_edit_points(self):
        return [self.get_center_pt()] + self.points


class Polygon(PolygonMixin, CanvasObjectBase):
    """Draws a polygon on a ImageViewCanvas.
    Parameters are:
    List of (x, y) points in the polygon.  The last one is assumed to
    be connected to the first.
    Optional parameters for linesize, color, etc.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            ## Param(name='points', type=list, default=[], argpos=0,
            ##       description="points making up polygon"),
            Param(name='linewidth', type=int, default=1,
                  min=1, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='yellow',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='fill', type=_bool,
                  default=False, valid=[False, True],
                  description="Fill the interior"),
            Param(name='fillcolor', default=None,
                  valid=colors_plus_none, type=_color,
                  description="Color of fill"),
            Param(name='fillalpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of fill"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            ]

    def __init__(self, points, color='red',
                 linewidth=1, linestyle='solid', showcap=False,
                 fill=False, fillcolor=None, alpha=1.0,
                 fillalpha=1.0, **kwdargs):
        self.kind = 'polygon'

        CanvasObjectBase.__init__(self, points=points, color=color,
                                  linewidth=linewidth, showcap=showcap,
                                  linestyle=linestyle, alpha=alpha,
                                  fill=fill, fillcolor=fillcolor,
                                  fillalpha=fillalpha, **kwdargs)
        PolygonMixin.__init__(self)

        assert len(points) > 2, \
               ValueError("Polygons need at least 3 points")

    def draw(self, viewer):
        cr = viewer.renderer.setup_cr(self)

        cpoints = self.get_cpoints(viewer)
        cr.draw_polygon(cpoints)

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, cpoints)


class Path(PolygonMixin, CanvasObjectBase):
    """Draws a path on a ImageViewCanvas.
    Parameters are:
    List of (x, y) points in the polygon.
    Optional parameters for linesize, color, etc.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            Param(name='coord', type=str, default='data',
                  valid=['data', 'wcs'],
                  description="Set type of coordinates"),
            ## Param(name='points', type=list, default=[], argpos=0,
            ##       description="points making up polygon"),
            Param(name='linewidth', type=int, default=1,
                  min=1, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='yellow',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            ]

    def __init__(self, points, color='red',
                 linewidth=1, linestyle='solid', showcap=False,
                 alpha=1.0, **kwdargs):
        self.kind = 'path'

        CanvasObjectBase.__init__(self, points=points, color=color,
                                  linewidth=linewidth, showcap=showcap,
                                  linestyle=linestyle, alpha=alpha,
                                  **kwdargs)
        PolygonMixin.__init__(self)

    def contains_arr_points(self, x_arr, y_arr, points, radius=1.0):
        # This code is split out of contains_arr() so that it can
        # be called from BezierCurve with a different set of points
        x1, y1 = self.crdmap.to_data(*points[0])
        contains = None
        for point in points[1:]:
            x2, y2 = self.crdmap.to_data(*point)
            res = self.point_within_line(x_arr, y_arr, x1, y1, x2, y2,
                                         radius)
            if contains is None:
                contains = res
            else:
                contains = numpy.logical_or(contains, res)
            x1, y1 = x2, y2
        return contains

    def contains_arr(self, x_arr, y_arr, radius=1.0):
        return self.contains_arr_points(x_arr, y_arr, self.points,
                                        radius=radius)

    def contains(self, data_x, data_y):
        x_arr, y_arr = numpy.array([data_x]), numpy.array([data_y])
        res = self.contains_arr(x_arr, y_arr)
        return res[0]

    def select_contains_points(self, viewer, points, data_x, data_y):
        # This code is split out of contains_arr() so that it can
        # be called from BezierCurve with a different set of points
        x1, y1 = self.crdmap.to_data(*points[0])
        for point in points[1:]:
            x2, y2 = self.crdmap.to_data(*point)
            if self.within_line(viewer, data_x, data_y, x1, y1, x2, y2,
                                self.cap_radius):

                return True
            x1, y1 = x2, y2
        return False

    def select_contains(self, viewer, data_x, data_y):
        return self.select_contains_points(viewer, self.points,
                                           data_x, data_y)

    def get_center_pt(self):
        # default is geometric average of points
        P = numpy.array(self.get_points())
        x = P[:, 0]
        y = P[:, 1]
        Cx = numpy.sum(x) / float(len(x))
        Cy = numpy.sum(y) / float(len(y))
        return (Cx, Cy)

    def draw(self, viewer):
        cpoints = self.get_cpoints(viewer, points=self.points)

        cr = viewer.renderer.setup_cr(self)
        cr.draw_path(cpoints)

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, cpoints)


class FreePolygon(Polygon):
    pass


class FreePath(Path):
    pass


class BezierCurve(Path):
    """Draws a Bezier Curve on a ImageViewCanvas.
    Parameters are:
    List of (x, y) points in the curve.
    Optional parameters for linesize, color, etc.

    TODO: need to implement contains(), which means figuring out whether a
    point lies on a bezier curve.
        See http://polymathprogrammer.com/2012/04/03/does-point-lie-on-bezier-curve/
    """

    def __init__(self, points, color='red',
                 linewidth=1, linestyle='solid', showcap=False,
                 alpha=1.0, **kwdargs):
        self.kind = 'beziercurve'

        CanvasObjectBase.__init__(self, points=points, color=color,
                                  linewidth=linewidth, showcap=showcap,
                                  linestyle=linestyle, alpha=alpha,
                                  **kwdargs)
        PolygonMixin.__init__(self)

    def calc_bezier_curve_range(self, steps, points):
        """Hacky method to get an ordered set of points that are on the
        Bezier curve.  This is used by some backends (which don't support
        drawing cubic Bezier curves) to render the curve using paths.
        """
        n = len(points) - 1
        fact_n = math.factorial(n)

        # press OrderedDict into use as an OrderedSet of points
        d = OrderedDict()

        m = float(steps - 1)

        # TODO: optomize this code as much as possible
        for i in range(steps):
            #t = i / float(steps - 1)
            t = i / m

            # optomize a call to calculate the bezier point
            #x, y = bezier(t, points)
            x = y = 0
            for j, pos in enumerate(points):
                #bern = bernstein(t, j, n)
                bin = fact_n / float(math.factorial(j) * math.factorial(n - j))
                bern = bin * (t ** j) * ((1 - t) ** (n - j))
                x += pos[0] * bern
                y += pos[1] * bern

            # convert to integer data coordinates and remove duplicates
            d[int(round(x)), int(round(y))] = None

        return list(d.keys())

    def get_points_on_curve(self, image):
        points = list(map(lambda pt: self.crdmap.to_data(pt[0], pt[1]),
                                      self.points))
        # use maximum dimension of image to estimate a reasonable number
        # of intermediate points
        steps = max(*image.get_size())
        return self.calc_bezier_curve_range(steps, points)

    def select_contains(self, viewer, data_x, data_y):
        image = viewer.get_image()
        points = self.get_points_on_curve(image)
        return self.select_contains_points(viewer, points, data_x, data_y)

    # TODO: this probably belongs somewhere else
    def get_pixels_on_curve(self, image):
        data = image.get_data()
        wd, ht = image.get_size()
        res = [ data[y, x] if 0 <= x < wd and 0 <= y < ht else numpy.NaN
                for x, y in self.get_points_on_curve(image) ]
        return res

    def draw(self, viewer):
        cpoints = self.get_cpoints(viewer, points=self.points)

        cr = viewer.renderer.setup_cr(self)
        if len(cpoints) < 4:
            # until we have 4 points, we cannot draw a quadradic bezier curve
            cr.draw_path(cpoints)
        else:
            if hasattr(cr, 'draw_bezier_curve'):
                cr.draw_bezier_curve(cpoints)
            else:
                # No Bezier support in this backend, so calculate intermediate
                # points and draw a path
                steps = max(*viewer.get_window_size())
                ipoints = self.calc_bezier_curve_range(steps, cpoints)
                cr.draw_path(ipoints)

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, cpoints)


class OnePointTwoRadiusMixin(object):

    def get_center_pt(self):
        return (self.x, self.y)

    def set_edit_point(self, i, pt):
        if i == 0:
            self.set_point_by_index(i, pt)
        elif i == 1:
            x, y = pt
            self.xradius = abs(x - self.x)
        elif i == 2:
            x, y = pt
            self.yradius = abs(y - self.y)
        elif i == 3:
            x, y = pt
            self.xradius, self.yradius = abs(x - self.x), abs(y - self.y)
        else:
            raise ValueError("No point corresponding to index %d" % (i))

    def get_edit_points(self):
        return [(self.x, self.y),    # location
                (self.x + self.xradius, self.y),  # adj xradius
                (self.x, self.y + self.yradius),  # adj yradius
                (self.x + self.xradius, self.y + self.yradius)]   # adj both

    def rotate_by(self, theta_deg):
        new_rot = math.fmod(self.rot_deg + theta_deg, 360.0)
        self.rot_deg = new_rot
        return new_rot

    def get_llur(self):
        xd, yd = self.crdmap.to_data(self.x, self.y)
        points = ((self.x - self.xradius, self.y - self.yradius),
                  (self.x + self.xradius, self.y - self.yradius),
                  (self.x + self.xradius, self.y + self.yradius),
                  (self.x - self.xradius, self.y + self.yradius))
        mpts = numpy.array(
            list(map(lambda pt: trcalc.rotate_pt(pt[0], pt[1], self.rot_deg,
                                                 xoff=xd, yoff=yd),
                     map(lambda pt: self.crdmap.to_data(pt[0], pt[1]),
                         points))))
        t_ = mpts.T
        x1, y1 = t_[0].min(), t_[1].min()
        x2, y2 = t_[0].max(), t_[1].max()
        return (x1, y1, x2, y2)


class Box(OnePointTwoRadiusMixin, CanvasObjectBase):
    """Draws a box on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of the center in the data space
    xradius, yradius: radii based on the number of pixels in data space
    Optional parameters for linesize, color, etc.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            Param(name='x', type=float, default=0.0, argpos=0,
                  description="X coordinate of center of object"),
            Param(name='y', type=float, default=0.0, argpos=1,
                  description="Y coordinate of center of object"),
            Param(name='xradius', type=float, default=1.0,  argpos=2,
                  min=0.0,
                  description="X radius of object"),
            Param(name='yradius', type=float, default=1.0,  argpos=3,
                  min=0.0,
                  description="Y radius of object"),
            Param(name='linewidth', type=int, default=1,
                  min=1, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='yellow',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='fill', type=_bool,
                  default=False, valid=[False, True],
                  description="Fill the interior"),
            Param(name='fillcolor', default=None,
                  valid=colors_plus_none, type=_color,
                  description="Color of fill"),
            Param(name='fillalpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of fill"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            Param(name='rot_deg', type=float, default=0.0,
                  min=-359.999, max=359.999, widget='spinfloat', incr=1.0,
                  description="Rotation about center of object"),
            ]

    def __init__(self, x, y, xradius, yradius, color='red',
                 linewidth=1, linestyle='solid', showcap=False,
                 fill=False, fillcolor=None, alpha=1.0, fillalpha=1.0,
                 rot_deg=0.0, **kwdargs):
        CanvasObjectBase.__init__(self, color=color,
                                  linewidth=linewidth, showcap=showcap,
                                  linestyle=linestyle,
                                  fill=fill, fillcolor=fillcolor,
                                  alpha=alpha, fillalpha=fillalpha,
                                  x=x, y=y, xradius=xradius,
                                  yradius=yradius, rot_deg=rot_deg,
                                  **kwdargs)
        OnePointTwoRadiusMixin.__init__(self)
        self.kind = 'box'

    def get_points(self):
        points = ((self.x - self.xradius, self.y - self.yradius),
                  (self.x + self.xradius, self.y - self.yradius),
                  (self.x + self.xradius, self.y + self.yradius),
                  (self.x - self.xradius, self.y + self.yradius))
        return points

    def contains_arr(self, x_arr, y_arr):
        x1, y1 = self.crdmap.to_data(self.x - self.xradius,
                                     self.y - self.yradius)
        x2, y2 = self.crdmap.to_data(self.x + self.xradius,
                                     self.y + self.yradius)

        # rotate point back to cartesian alignment for test
        xd, yd = self.crdmap.to_data(self.x, self.y)
        xa, ya = trcalc.rotate_pt(x_arr, y_arr, -self.rot_deg,
                                  xoff=xd, yoff=yd)

        contains = numpy.logical_and(
            numpy.logical_and(min(x1, x2) <= xa, xa <= max(x1, x2)),
            numpy.logical_and(min(y1, y2) <= ya, ya <= max(y1, y2)))
        return contains

    def contains(self, data_x, data_y):
        x_arr, y_arr = numpy.array([data_x]), numpy.array([data_y])
        res = self.contains_arr(x_arr, y_arr)
        return res[0]

    def draw(self, viewer):
        cpoints = self.get_cpoints(viewer)

        cr = viewer.renderer.setup_cr(self)
        cr.draw_polygon(cpoints)

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, cpoints)


class Ellipse(OnePointTwoRadiusMixin, CanvasObjectBase):
    """Draws an ellipse on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of the center in the data space
    xradius, yradius: radii based on the number of pixels in data space
    Optional parameters for linesize, color, etc.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            Param(name='x', type=float, default=0.0, argpos=0,
                  description="X coordinate of center of object"),
            Param(name='y', type=float, default=0.0, argpos=1,
                  description="Y coordinate of center of object"),
            Param(name='xradius', type=float, default=1.0,  argpos=2,
                  min=0.0,
                  description="X radius of object"),
            Param(name='yradius', type=float, default=1.0,  argpos=3,
                  min=0.0,
                  description="Y radius of object"),
            Param(name='linewidth', type=int, default=1,
                  min=1, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='yellow',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='fill', type=_bool,
                  default=False, valid=[False, True],
                  description="Fill the interior"),
            Param(name='fillcolor', default=None,
                  valid=colors_plus_none, type=_color,
                  description="Color of fill"),
            Param(name='fillalpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of fill"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            Param(name='rot_deg', type=float, default=0.0,
                  min=-359.999, max=359.999, widget='spinfloat', incr=1.0,
                  description="Rotation about center of object"),
            ]

    def __init__(self, x, y, xradius, yradius, color='yellow',
                 linewidth=1, linestyle='solid', showcap=False,
                 fill=False, fillcolor=None, alpha=1.0, fillalpha=1.0,
                 rot_deg=0.0, **kwdargs):
        CanvasObjectBase.__init__(self, color=color,
                                  linewidth=linewidth, showcap=showcap,
                                  linestyle=linestyle,
                                  fill=fill, fillcolor=fillcolor,
                                  alpha=alpha, fillalpha=fillalpha,
                                  x=x, y=y, xradius=xradius,
                                  yradius=yradius, rot_deg=rot_deg,
                                  **kwdargs)
        OnePointTwoRadiusMixin.__init__(self)
        self.kind = 'ellipse'

    def get_points(self):
        return [self.get_center_pt()]

    def contains_arr(self, x_arr, y_arr):
        # coerce args to floats
        x_arr = x_arr.astype(numpy.float)
        y_arr = y_arr.astype(numpy.float)

        # rotate point back to cartesian alignment for test
        xd, yd = self.crdmap.to_data(self.x, self.y)
        xa, ya = trcalc.rotate_pt(x_arr, y_arr, -self.rot_deg,
                                  xoff=xd, yoff=yd)

        # need to recalculate radius in case of wcs coords
        x2, y2 = self.crdmap.to_data(self.x + self.xradius,
                                     self.y + self.yradius)
        xradius = max(x2, xd) - min(x2, xd)
        yradius = max(y2, yd) - min(y2, yd)

        # See http://math.stackexchange.com/questions/76457/check-if-a-point-is-within-an-ellipse
        res = (((xa - xd) ** 2) / xradius ** 2 +
               ((ya - yd) ** 2) / yradius ** 2)
        contains = (res <= 1.0)
        return contains

    def contains(self, data_x, data_y):
        x_arr, y_arr = numpy.array([data_x]), numpy.array([data_y])
        res = self.contains_arr(x_arr, y_arr)
        return res[0]

    def get_bezier_pts(self, kappa=0.5522848):
        """Used by drawing subclasses to draw the ellipse."""

        mx, my = self.x, self.y
        xs, ys = mx - self.xradius, my - self.yradius
        ox, oy = self.xradius * kappa, self.yradius * kappa
        xe, ye = mx + self.xradius, my + self.yradius

        pts = [(xs, my),
               (xs, my - oy), (mx - ox, ys), (mx, ys),
               (mx + ox, ys), (xe, my - oy), (xe, my),
               (xe, my + oy), (mx + ox, ye), (mx, ye),
               (mx - ox, ye), (xs, my + oy), (xs, my)]
        return pts

    def draw(self, viewer):
        cr = viewer.renderer.setup_cr(self)

        if hasattr(cr, 'draw_ellipse_bezier'):
            cp = self.get_cpoints(viewer, points=self.get_bezier_pts())
            cr.draw_ellipse_bezier(cp)
        else:
            cpoints = self.get_cpoints(viewer, points=self.get_edit_points())
            cx, cy = cpoints[0]
            cxradius = abs(cpoints[1][0] - cx)
            cyradius = abs(cpoints[2][1] - cy)
            cr.draw_ellipse(cx, cy, cxradius, cyradius, self.rot_deg)

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            cpoints = self.get_cpoints(viewer)
            self.draw_caps(cr, self.cap, cpoints)


class Triangle(OnePointTwoRadiusMixin, CanvasObjectBase):
    """Draws a triangle on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of the center in the data space
    xradius, yradius: radii based on the number of pixels in data space
    Optional parameters for linesize, color, etc.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            Param(name='x', type=float, default=0.0, argpos=0,
                  description="X coordinate of center of object"),
            Param(name='y', type=float, default=0.0, argpos=1,
                  description="Y coordinate of center of object"),
            Param(name='xradius', type=float, default=1.0,  argpos=2,
                  min=0.0,
                  description="X radius of object"),
            Param(name='yradius', type=float, default=1.0,  argpos=3,
                  min=0.0,
                  description="Y radius of object"),
            Param(name='linewidth', type=int, default=1,
                  min=1, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='yellow',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='fill', type=_bool,
                  default=False, valid=[False, True],
                  description="Fill the interior"),
            Param(name='fillcolor', default=None,
                  valid=colors_plus_none, type=_color,
                  description="Color of fill"),
            Param(name='fillalpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of fill"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            Param(name='rot_deg', type=float, default=0.0,
                  min=-359.999, max=359.999, widget='spinfloat', incr=1.0,
                  description="Rotation about center of object"),
            ]

    def __init__(self, x, y, xradius, yradius, color='pink',
                 linewidth=1, linestyle='solid', showcap=False,
                 fill=False, fillcolor=None, alpha=1.0, fillalpha=1.0,
                 rot_deg=0.0, **kwdargs):
        self.kind='triangle'
        CanvasObjectBase.__init__(self, color=color, alpha=alpha,
                                  linewidth=linewidth, showcap=showcap,
                                  linestyle=linestyle,
                                  fill=fill, fillcolor=fillcolor,
                                  fillalpha=fillalpha,
                                  x=x, y=y, xradius=xradius,
                                  yradius=yradius, rot_deg=rot_deg,
                                  **kwdargs)
        OnePointTwoRadiusMixin.__init__(self)

    def get_points(self):
        return [(self.x - 2*self.xradius, self.y - self.yradius),
                (self.x + 2*self.xradius, self.y - self.yradius),
                (self.x, self.y + self.yradius)]


    def get_llur(self):
        xd, yd = self.crdmap.to_data(self.x, self.y)
        points = ((self.x - self.xradius*2, self.y - self.yradius),
                  (self.x + self.xradius*2, self.y - self.yradius),
                  (self.x + self.xradius*2, self.y + self.yradius),
                  (self.x - self.xradius*2, self.y + self.yradius))
        mpts = numpy.array(
            list(map(lambda pt: trcalc.rotate_pt(pt[0], pt[1], self.rot_deg,
                                                 xoff=xd, yoff=yd),
                     map(lambda pt: self.crdmap.to_data(pt[0], pt[1]),
                         points))))
        t_ = mpts.T
        x1, y1 = t_[0].min(), t_[1].min()
        x2, y2 = t_[0].max(), t_[1].max()
        return (x1, y1, x2, y2)

    def contains_arr(self, x_arr, y_arr):
        # is this the same as self.x, self.y ?
        ctr_x, ctr_y = self.get_center_pt()
        xd, yd = self.crdmap.to_data(ctr_x, ctr_y)
        # rotate point back to cartesian alignment for test
        xa, ya = trcalc.rotate_pt(x_arr, y_arr, -self.rot_deg,
                                  xoff=xd, yoff=yd)

        (x1, y1), (x2, y2), (x3, y3) = self.get_points()
        x1, y1 = self.crdmap.to_data(x1, y1)
        x2, y2 = self.crdmap.to_data(x2, y2)
        x3, y3 = self.crdmap.to_data(x3, y3)

        # coerce args to floats
        x_arr = x_arr.astype(numpy.float)
        y_arr = y_arr.astype(numpy.float)

        # barycentric coordinate test
        denominator = float((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
        a = ((y2 - y3)*(xa - x3) + (x3 - x2)*(ya - y3)) / denominator
        b = ((y3 - y1)*(xa - x3) + (x1 - x3)*(ya - y3)) / denominator
        c = 1.0 - a - b

        #tf = (0.0 <= a <= 1.0 and 0.0 <= b <= 1.0 and 0.0 <= c <= 1.0)
        contains = numpy.logical_and(
            numpy.logical_and(0.0 <= a, a <= 1.0),
            numpy.logical_and(numpy.logical_and(0.0 <= b, b <= 1.0),
                              numpy.logical_and(0.0 <= c, c <= 1.0)))
        return contains

    def contains(self, data_x, data_y):
        x_arr, y_arr = numpy.array([data_x]), numpy.array([data_y])
        res = self.contains_arr(x_arr, y_arr)
        return res[0]

    def draw(self, viewer):
        cpoints = self.get_cpoints(viewer)

        cr = viewer.renderer.setup_cr(self)
        cr.draw_polygon(cpoints)

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, cpoints)


class OnePointOneRadiusMixin(object):

    def get_center_pt(self):
        return (self.x, self.y)

    def get_points(self):
        return [(self.x, self.y)]

    def set_edit_point(self, i, pt):
        if i == 0:
            self.set_point_by_index(i, pt)
        elif i == 1:
            x, y = pt
            self.radius = math.sqrt(abs(x - self.x)**2 +
                                    abs(y - self.y)**2 )
        else:
            raise ValueError("No point corresponding to index %d" % (i))

    def get_edit_points(self):
        return [(self.x, self.y),
                (self.x + self.radius, self.y)]

    def rotate_by(self, theta_deg):
        pass


class Circle(OnePointOneRadiusMixin, CanvasObjectBase):
    """Draws a circle on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of the center in the data space
    radius: radius based on the number of pixels in data space
    Optional parameters for linesize, color, etc.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            Param(name='x', type=float, default=0.0, argpos=0,
                  description="X coordinate of center of object"),
            Param(name='y', type=float, default=0.0, argpos=1,
                  description="Y coordinate of center of object"),
            Param(name='radius', type=float, default=1.0,  argpos=2,
                  min=0.0,
                  description="Radius of object"),
            Param(name='linewidth', type=int, default=1,
                  min=1, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='yellow',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='fill', type=_bool,
                  default=False, valid=[False, True],
                  description="Fill the interior"),
            Param(name='fillcolor', default=None,
                  valid=colors_plus_none, type=_color,
                  description="Color of fill"),
            Param(name='fillalpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of fill"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            ]

    def __init__(self, x, y, radius, color='yellow',
                 linewidth=1, linestyle='solid', showcap=False,
                 fill=False, fillcolor=None, alpha=1.0, fillalpha=1.0,
                 **kwdargs):
        CanvasObjectBase.__init__(self, color=color,
                                  linewidth=linewidth, showcap=showcap,
                                  linestyle=linestyle,
                                  fill=fill, fillcolor=fillcolor,
                                  alpha=alpha, fillalpha=fillalpha,
                                  x=x, y=y, radius=radius, **kwdargs)
        OnePointOneRadiusMixin.__init__(self)
        self.kind = 'circle'

    def contains_arr(self, x_arr, y_arr):
        xd, yd = self.crdmap.to_data(self.x, self.y)

        # need to recalculate radius in case of wcs coords
        x2, y2 = self.crdmap.to_data(self.x + self.radius, self.y)
        x3, y3 = self.crdmap.to_data(self.x, self.y + self.radius)
        xradius = max(x2, xd) - min(x2, xd)
        yradius = max(y3, yd) - min(y3, yd)

        # need to make sure to coerce these to floats or it won't work
        x_arr = x_arr.astype(numpy.float)
        y_arr = y_arr.astype(numpy.float)

        # See http://math.stackexchange.com/questions/76457/check-if-a-point-is-within-an-ellipse
        res = (((x_arr - xd) ** 2) / xradius ** 2 +
               ((y_arr - yd) ** 2) / yradius ** 2)
        contains = (res <= 1.0)
        return contains

    def contains(self, data_x, data_y):
        x_arr, y_arr = numpy.array([data_x]), numpy.array([data_y])
        res = self.contains_arr(x_arr, y_arr)
        return res[0]

    def get_llur(self):
        x1, y1 = self.crdmap.to_data(self.x - self.radius,
                                     self.y - self.radius)
        x2, y2 = self.crdmap.to_data(self.x + self.radius,
                                     self.y + self.radius)
        return self.swapxy(x1, y1, x2, y2)

    def draw(self, viewer):
        cx, cy, cradius = self.calc_radius(viewer, self.x, self.y,
                                           self.radius)
        cr = viewer.renderer.setup_cr(self)
        cr.draw_circle(cx, cy, cradius)

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, ((cx, cy), ))


class Point(OnePointOneRadiusMixin, CanvasObjectBase):
    """Draws a point on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of the center in the data space
    radius: radius based on the number of pixels in data space
    Optional parameters for linesize, color, style, etc.
    Currently the only styles are 'cross' and 'plus'.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            Param(name='x', type=float, default=0.0, argpos=0,
                  description="X coordinate of center of object"),
            Param(name='y', type=float, default=0.0, argpos=1,
                  description="Y coordinate of center of object"),
            Param(name='radius', type=float, default=1.0,  argpos=2,
                  min=0.0,
                  description="Radius of object"),
            Param(name='style', type=str, default='cross',
                  valid=['cross', 'plus'],
                  description="Style of point (default 'cross')"),
            Param(name='linewidth', type=int, default=1,
                  min=1, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='yellow',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            ]

    def __init__(self, x, y, radius, style='cross', color='yellow',
                 linewidth=1, linestyle='solid', alpha=1.0, showcap=False,
                 **kwdargs):
        self.kind = 'point'
        CanvasObjectBase.__init__(self, color=color, alpha=alpha,
                                  linewidth=linewidth,
                                  linestyle=linestyle,
                                  x=x, y=y, radius=radius,
                                  showcap=showcap, style=style,
                                  **kwdargs)
        OnePointOneRadiusMixin.__init__(self)

    def contains_arr(self, x_arr, y_arr, radius=2.0):
        xd, yd = self.crdmap.to_data(self.x, self.y)
        contains = self.point_within_radius(x_arr, y_arr, xd, yd,
                                            radius)
        return contains

    def contains(self, data_x, data_y, radius=1):
        x_arr, y_arr = numpy.array([data_x]), numpy.array([data_y])
        res = self.contains_arr(x_arr, y_arr, radius=radius)
        return res[0]

    def select_contains(self, viewer, data_x, data_y):
        xd, yd = self.crdmap.to_data(self.x, self.y)
        return self.within_radius(viewer, data_x, data_y, xd, yd,
                                  self.cap_radius)

    def get_llur(self):
        x, y = self.crdmap.to_data(self.x, self.y)
        return (x-0.5, y-0.5, x+0.5, y+0.5)

    def get_edit_points(self):
        return [(self.x, self.y),
                # TODO: account for point style
                (self.x + self.radius, self.y + self.radius)]

    def draw(self, viewer):
        cx, cy, cradius = self.calc_radius(viewer, self.x, self.y,
                                           self.radius)
        cx1, cy1 = cx - cradius, cy - cradius
        cx2, cy2 = cx + cradius, cy + cradius

        cr = viewer.renderer.setup_cr(self)

        if self.style == 'cross':
            cr.draw_line(cx1, cy1, cx2, cy2)
            cr.draw_line(cx1, cy2, cx2, cy1)
        else:
            cr.draw_line(cx1, cy, cx2, cy)
            cr.draw_line(cx, cy1, cx, cy2)

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, ((cx, cy), ))


class TwoPointMixin(object):

    def get_center_pt(self):
        return ((self.x1 + self.x2) / 2., (self.y1 + self.y2) / 2.)

    def set_edit_point(self, i, pt):
        if i == 0:
            x, y = pt
            self.move_to(x, y)
        else:
            self.set_point_by_index(i-1, pt)

    def get_edit_points(self):
        return [self.get_center_pt(),
                (self.x1, self.y1), (self.x2, self.y2)]

    def get_llur(self):
        x1, y1 = self.crdmap.to_data(self.x1, self.y1)
        x2, y2 = self.crdmap.to_data(self.x2, self.y2)
        return self.swapxy(x1, y1, x2, y2)


class Rectangle(TwoPointMixin, CanvasObjectBase):
    """Draws a rectangle on a ImageViewCanvas.
    Parameters are:
    x1, y1: 0-based coordinates of one corner in the data space
    x2, y2: 0-based coordinates of the opposing corner in the data space
    Optional parameters for linesize, color, etc.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            Param(name='x1', type=float, default=0.0, argpos=0,
                  description="First X coordinate of object"),
            Param(name='y1', type=float, default=0.0, argpos=1,
                  description="First Y coordinate of object"),
            Param(name='x2', type=float, default=0.0, argpos=2,
                  description="Second X coordinate of object"),
            Param(name='y2', type=float, default=0.0, argpos=3,
                  description="Second Y coordinate of object"),
            Param(name='linewidth', type=int, default=1,
                  min=1, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='yellow',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='fill', type=_bool,
                  default=False, valid=[False, True],
                  description="Fill the interior"),
            Param(name='fillcolor', default=None,
                  valid=colors_plus_none, type=_color,
                  description="Color of fill"),
            Param(name='fillalpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of fill"),
            Param(name='drawdims', type=_bool,
                  default=False, valid=[False, True],
                  description="Annotate with dimensions of object"),
            Param(name='font', type=str, default='Sans Serif',
                  description="Font family for text"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            ]

    def __init__(self, x1, y1, x2, y2, color='red',
                 linewidth=1, linestyle='solid', showcap=False,
                 fill=False, fillcolor=None, alpha=1.0,
                 drawdims=False, font='Sans Serif', fillalpha=1.0,
                 **kwdargs):
        self.kind = 'rectangle'

        CanvasObjectBase.__init__(self, color=color,
                                  x1=x1, y1=y1, x2=x2, y2=y2,
                                  linewidth=linewidth, showcap=showcap,
                                  linestyle=linestyle,
                                  fill=fill, fillcolor=fillcolor,
                                  alpha=alpha, fillalpha=fillalpha,
                                  drawdims=drawdims, font=font,
                                  **kwdargs)
        TwoPointMixin.__init__(self)

    def get_points(self):
        points = [(self.x1, self.y1), (self.x2, self.y1),
                  (self.x2, self.y2), (self.x1, self.y2)]
        return points

    def contains_arr(self, x_arr, y_arr):
        x1, y1, x2, y2 = self.get_llur()

        contains = numpy.logical_and(
            numpy.logical_and(x1 <= x_arr, x_arr <= x2),
            numpy.logical_and(y1 <= y_arr, y_arr <= y2))
        return contains

    def contains(self, data_x, data_y):
        x1, y1, x2, y2 = self.get_llur()

        if (x1 <= data_x <= x2) and (y1 <= data_y <= y2):
            return True
        return False

    # TO BE DEPRECATED?
    def move_point(self):
        return self.get_center_pt()

    def draw(self, viewer):
        cr = viewer.renderer.setup_cr(self)

        cpoints = self.get_cpoints(viewer,
                                   points=((self.x1, self.y1),
                                           (self.x2, self.y1),
                                           (self.x2, self.y2),
                                           (self.x1, self.y2)))
        cr.draw_polygon(cpoints)

        if self.drawdims:
            fontsize = self.scale_font(viewer)
            cr.set_font(self.font, fontsize)

            cx1, cy1 = cpoints[0]
            cx2, cy2 = cpoints[2]

            # draw label on X dimension
            cx = cx1 + (cx2 - cx1) // 2
            cy = cy2 + -4
            cr.draw_text(cx, cy, "%d" % abs(self.x2 - self.x1))

            # draw label on Y dimension
            cy = cy1 + (cy2 - cy1) // 2
            cx = cx2 + 4
            cr.draw_text(cx, cy, "%d" % abs(self.y2 - self.y1))

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, cpoints)

class Square(Rectangle):
    pass

class Line(TwoPointMixin, CanvasObjectBase):
    """Draws a line on a ImageViewCanvas.
    Parameters are:
    x1, y1: 0-based coordinates of one end in the data space
    x2, y2: 0-based coordinates of the opposing end in the data space
    Optional parameters for linesize, color, etc.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            Param(name='x1', type=float, default=0.0, argpos=0,
                  description="First X coordinate of object"),
            Param(name='y1', type=float, default=0.0, argpos=1,
                  description="First Y coordinate of object"),
            Param(name='x2', type=float, default=0.0, argpos=2,
                  description="Second X coordinate of object"),
            Param(name='y2', type=float, default=0.0, argpos=3,
                  description="Second Y coordinate of object"),
            Param(name='linewidth', type=int, default=1,
                  min=1, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default solid)"),
            Param(name='arrow', type=str, default='none',
                  valid=['start', 'end', 'both', 'none'],
                  description="Arrows at ends (default: none)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='yellow',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            ]

    def __init__(self, x1, y1, x2, y2, color='red',
                 linewidth=1, linestyle='solid', alpha=1.0,
                 arrow=None, showcap=False, **kwdargs):
        self.kind = 'line'
        CanvasObjectBase.__init__(self, color=color, alpha=alpha,
                                  linewidth=linewidth, showcap=showcap,
                                  linestyle=linestyle, arrow=arrow,
                                  x1=x1, y1=y1, x2=x2, y2=y2,
                                  **kwdargs)
        TwoPointMixin.__init__(self)

    def get_points(self):
        return [(self.x1, self.y1), (self.x2, self.y2)]

    def contains_arr(self, x_arr, y_arr, radius=1.0):
        x1, y1 = self.crdmap.to_data(self.x1, self.y1)
        x2, y2 = self.crdmap.to_data(self.x2, self.y2)
        contains = self.point_within_line(x_arr, y_arr, x1, y1, x2, y2,
                                          radius)
        return contains

    def contains(self, data_x, data_y, radius=1.0):
        x_arr, y_arr = numpy.array([data_x]), numpy.array([data_y])
        res = self.contains_arr(x_arr, y_arr, radius=radius)
        return res[0]

    def select_contains(self, viewer, data_x, data_y):
        x1, y1 = self.crdmap.to_data(self.x1, self.y1)
        x2, y2 = self.crdmap.to_data(self.x2, self.y2)
        return self.within_line(viewer, data_x, data_y, x1, y1, x2, y2,
                                self.cap_radius)

    def draw(self, viewer):
        cx1, cy1 = self.canvascoords(viewer, self.x1, self.y1)
        cx2, cy2 = self.canvascoords(viewer, self.x2, self.y2)

        cr = viewer.renderer.setup_cr(self)
        cr.draw_line(cx1, cy1, cx2, cy2)

        if self.arrow == 'end':
            self.draw_arrowhead(cr, cx1, cy1, cx2, cy2)
            caps = [(cx1, cy1)]
        elif self.arrow == 'start':
            self.draw_arrowhead(cr, cx2, cy2, cx1, cy1)
            caps = [(cx2, cy2)]
        elif self.arrow == 'both':
            self.draw_arrowhead(cr, cx2, cy2, cx1, cy1)
            self.draw_arrowhead(cr, cx1, cy1, cx2, cy2)
            caps = []
        else:
            caps = [(cx1, cy1), (cx2, cy2)]

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, caps)


class RightTriangle(TwoPointMixin, CanvasObjectBase):
    """Draws a right triangle on a ImageViewCanvas.
    Parameters are:
    x1, y1: 0-based coordinates of one end of the diagonal in the data space
    x2, y2: 0-based coordinates of the opposite end of the diagonal
    Optional parameters for linesize, color, etc.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            Param(name='x1', type=float, default=0.0, argpos=0,
                  description="First X coordinate of object"),
            Param(name='y1', type=float, default=0.0, argpos=1,
                  description="First Y coordinate of object"),
            Param(name='x2', type=float, default=0.0, argpos=2,
                  description="Second X coordinate of object"),
            Param(name='y2', type=float, default=0.0, argpos=3,
                  description="Second Y coordinate of object"),
            Param(name='linewidth', type=int, default=1,
                  min=1, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='yellow',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='fill', type=_bool,
                  default=False, valid=[False, True],
                  description="Fill the interior"),
            Param(name='fillcolor', default=None,
                  valid=colors_plus_none, type=_color,
                  description="Color of fill"),
            Param(name='fillalpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of fill"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            ]

    def __init__(self, x1, y1, x2, y2, color='pink',
                 linewidth=1, linestyle='solid', showcap=False,
                 fill=False, fillcolor=None, alpha=1.0, fillalpha=1.0,
                 **kwdargs):
        self.kind='righttriangle'
        CanvasObjectBase.__init__(self, color=color, alpha=alpha,
                                  linewidth=linewidth, showcap=showcap,
                                  linestyle=linestyle,
                                  fill=fill, fillcolor=fillcolor,
                                  fillalpha=fillalpha,
                                  x1=x1, y1=y1, x2=x2, y2=y2,
                                  **kwdargs)
        TwoPointMixin.__init__(self)

    def get_points(self):
        return [(self.x1, self.y1), (self.x2, self.y2)]

    def contains_arr(self, x_arr, y_arr):

        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        x3, y3 = self.x2, self.y1
        x1, y1 = self.crdmap.to_data(x1, y1)
        x2, y2 = self.crdmap.to_data(x2, y2)
        x3, y3 = self.crdmap.to_data(x3, y3)

        # coerce args to floats
        x_arr = x_arr.astype(numpy.float)
        y_arr = y_arr.astype(numpy.float)

        # barycentric coordinate test
        denominator = float((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
        a = ((y2 - y3)*(x_arr - x3) + (x3 - x2)*(y_arr - y3)) / denominator
        b = ((y3 - y1)*(x_arr - x3) + (x1 - x3)*(y_arr - y3)) / denominator
        c = 1.0 - a - b

        #tf = (0.0 <= a <= 1.0 and 0.0 <= b <= 1.0 and 0.0 <= c <= 1.0)
        contains = numpy.logical_and(
            numpy.logical_and(0.0 <= a, a <= 1.0),
            numpy.logical_and(numpy.logical_and(0.0 <= b, b <= 1.0),
                              numpy.logical_and(0.0 <= c, c <= 1.0)))
        return contains

    def contains(self, data_x, data_y):
        x_arr, y_arr = numpy.array([data_x]), numpy.array([data_y])
        res = self.contains_arr(x_arr, y_arr)
        return res[0]
        ## x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        ## x3, y3 = self.x2, self.y1

        ## x1, y1 = self.crdmap.to_data(x1, y1)
        ## x2, y2 = self.crdmap.to_data(x2, y2)
        ## x3, y3 = self.crdmap.to_data(x3, y3)

        ## barycentric coordinate test
        ## denominator = ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
        ## a = ((y2 - y3)*(data_x - x3) + (x3 - x2)*(data_y - y3)) / denominator
        ## b = ((y3 - y1)*(data_x - x3) + (x1 - x3)*(data_y - y3)) / denominator
        ## c = 1.0 - a - b

        ## tf = (0.0 <= a <= 1.0 and 0.0 <= b <= 1.0 and 0.0 <= c <= 1.0)
        ## return tf

    def draw(self, viewer):
        cpoints = self.get_cpoints(viewer,
                                   points=((self.x1, self.y1),
                                           (self.x2, self.y2),
                                           (self.x2, self.y1)))
        cr = viewer.renderer.setup_cr(self)
        cr.draw_polygon(cpoints)

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, cpoints)


class Compass(OnePointOneRadiusMixin, CanvasObjectBase):
    """Draws a WCS compass on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of the center in the data space
    radius: radius of the compass arms, in data units
    Optional parameters for linesize, color, etc.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data'],
            ##       description="Set type of coordinates"),
            Param(name='x', type=float, default=0.0, argpos=0,
                  description="X coordinate of center of object"),
            Param(name='y', type=float, default=0.0, argpos=1,
                  description="Y coordinate of center of object"),
            Param(name='radius', type=float, default=1.0,  argpos=2,
                  min=0.0,
                  description="Radius of object"),
            Param(name='linewidth', type=int, default=1,
                  min=1, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='skyblue',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='font', type=str, default='Sans Serif',
                  description="Font family for text"),
            Param(name='fontsize', type=int, default=None,
                  min=8, max=72,
                  description="Font size of text (default: vary by scale)"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            ]

    def __init__(self, x, y, radius, color='skyblue',
                 linewidth=1, fontsize=None, font='Sans Serif',
                 alpha=1.0, linestyle='solid', showcap=True, **kwdargs):
        self.kind = 'compass'
        CanvasObjectBase.__init__(self, color=color, alpha=alpha,
                                  linewidth=linewidth, showcap=showcap,
                                  linestyle=linestyle,
                                  x=x, y=y, radius=radius,
                                  font=font, fontsize=fontsize,
                                  **kwdargs)
        OnePointOneRadiusMixin.__init__(self)

    def get_points(self):
        image = self.viewer.get_image()
        x, y, xn, yn, xe, ye = image.calc_compass_radius(self.x,
                                                         self.y,
                                                         self.radius)
        return [(x, y), (xn, yn), (xe, ye)]

    def get_edit_points(self):
        return self.get_points()

    def set_edit_point(self, i, pt):
        if i == 0:
            self.set_point_by_index(i, pt)
        elif i in (1, 2):
            x, y = pt
            self.radius = max(abs(x - self.x), abs(y - self.y))
        else:
            raise ValueError("No point corresponding to index %d" % (i))

    def select_contains(self, viewer, data_x, data_y):
        xd, yd = self.crdmap.to_data(self.x, self.y)
        return self.within_radius(viewer, data_x, data_y, xd, yd,
                                  self.cap_radius)

    def draw(self, viewer):
        (cx1, cy1), (cx2, cy2), (cx3, cy3) = self.get_cpoints(viewer)
        cr = viewer.renderer.setup_cr(self)
        cr.set_font_from_shape(self)

        # draw North line and arrowhead
        cr.draw_line(cx1, cy1, cx2, cy2)
        self.draw_arrowhead(cr, cx1, cy1, cx2, cy2)

        # draw East line and arrowhead
        cr.draw_line(cx1, cy1, cx3, cy3)
        self.draw_arrowhead(cr, cx1, cy1, cx3, cy3)

        # draw "N" & "E"
        cx, cy = self.get_textpos(cr, 'N', cx1, cy1, cx2, cy2)
        cr.draw_text(cx, cy, 'N')
        cx, cy = self.get_textpos(cr, 'E', cx1, cy1, cx3, cy3)
        cr.draw_text(cx, cy, 'E')

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, ((cx1, cy1), ))

    def get_textpos(self, cr, text, cx1, cy1, cx2, cy2):
        htwd, htht = cr.text_extents(text)
        diag_xoffset = 0
        diag_yoffset = 0
        xplumb_yoffset = 0
        yplumb_xoffset = 0

        diag_yoffset = 14
        if abs(cy1 - cy2) < 5:
            pass
        elif cy1 < cy2:
            xplumb_yoffset = -4
        else:
            xplumb_yoffset = 14
            diag_yoffset = -4

        if abs(cx1 - cx2) < 5:
            diag_xoffset = -(4 + htwd)
        elif (cx1 < cx2):
            diag_xoffset = -(4 + htwd)
            yplumb_xoffset = 4
        else:
            diag_xoffset = 4
            yplumb_xoffset = -(4 + 0)

        xh = min(cx1, cx2); y = cy1 + xplumb_yoffset
        xh += (max(cx1, cx2) - xh) // 2
        yh = min(cy1, cy2); x = cx2 + yplumb_xoffset
        yh += (max(cy1, cy2) - yh) // 2

        xd = xh + diag_xoffset
        yd = yh + diag_yoffset
        return (xd, yd)


class Ruler(TwoPointMixin, CanvasObjectBase):
    """Draws a WCS ruler (like a right triangle) on a ImageViewCanvas.
    Parameters are:
    x1, y1: 0-based coordinates of one end of the diagonal in the data space
    x2, y2: 0-based coordinates of the opposite end of the diagonal
    Optional parameters for linesize, color, etc.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            Param(name='x1', type=float, default=0.0, argpos=0,
                  description="First X coordinate of object"),
            Param(name='y1', type=float, default=0.0, argpos=1,
                  description="First Y coordinate of object"),
            Param(name='x2', type=float, default=0.0, argpos=2,
                  description="Second X coordinate of object"),
            Param(name='y2', type=float, default=0.0, argpos=3,
                  description="Second Y coordinate of object"),
            Param(name='linewidth', type=int, default=1,
                  min=1, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default: solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='lightgreen',
                  description="Color of outline"),
            Param(name='showplumb', type=_bool,
                  default=True, valid=[False, True],
                  description="Show plumb lines for the ruler"),
            Param(name='color2',
                  valid=colors_plus_none, type=_color, default='yellow',
                  description="Second color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='units', type=str, default='arcmin',
                  valid=['arcmin', 'pixels'],
                  description="Units for text distance (default: arcmin)"),
            Param(name='font', type=str, default='Sans Serif',
                  description="Font family for text"),
            Param(name='fontsize', type=int, default=None,
                  min=8, max=72,
                  description="Font size of text (default: vary by scale)"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            ]

    def __init__(self, x1, y1, x2, y2, color='green', color2='yellow',
                 alpha=1.0, linewidth=1, linestyle='solid',
                 showcap=True, showplumb=True, units='arcmin',
                 font='Sans Serif', fontsize=None, **kwdargs):
        self.kind = 'ruler'
        CanvasObjectBase.__init__(self, color=color, color2=color2,
                                  alpha=alpha, units=units,
                                  showplumb=showplumb,
                                  linewidth=linewidth, showcap=showcap,
                                  linestyle=linestyle,
                                  x1=x1, y1=y1, x2=x2, y2=y2,
                                  font=font, fontsize=fontsize,
                                  **kwdargs)
        TwoPointMixin.__init__(self)

    def get_points(self):
        return [(self.x1, self.y1), (self.x2, self.y2)]

    def select_contains(self, viewer, data_x, data_y):
        x1, y1 = self.crdmap.to_data(self.x1, self.y1)
        x2, y2 = self.crdmap.to_data(self.x2, self.y2)
        return self.within_line(viewer, data_x, data_y, x1, y1, x2, y2,
                                self.cap_radius)

    def get_ruler_distances(self, viewer):
        mode = self.units.lower()
        try:
            image = viewer.get_image()
            if mode == 'arcmin':
                # Calculate RA and DEC for the three points
                # origination point
                ra_org, dec_org = image.pixtoradec(self.x1, self.y1)

                # destination point
                ra_dst, dec_dst = image.pixtoradec(self.x2, self.y2)

                # "heel" point making a right triangle
                ra_heel, dec_heel = image.pixtoradec(self.x2, self.y1)

                text_h = wcs.get_starsep_RaDecDeg(ra_org, dec_org,
                                                  ra_dst, dec_dst)
                text_x = wcs.get_starsep_RaDecDeg(ra_org, dec_org,
                                                  ra_heel, dec_heel)
                text_y = wcs.get_starsep_RaDecDeg(ra_heel, dec_heel,
                                                  ra_dst, dec_dst)
            else:
                dx = abs(self.x2 - self.x1)
                dy = abs(self.y2 - self.y1)
                dh = math.sqrt(dx**2 + dy**2)
                text_x = str(dx)
                text_y = str(dy)
                text_h = ("%.3f" % dh)

        except Exception as e:
            text_h = 'BAD WCS'
            text_x = 'BAD WCS'
            text_y = 'BAD WCS'

        return (text_x, text_y, text_h)

    def draw(self, viewer):
        cx1, cy1 = self.canvascoords(viewer, self.x1, self.y1)
        cx2, cy2 = self.canvascoords(viewer, self.x2, self.y2)

        text_x, text_y, text_h = self.get_ruler_distances(viewer)

        cr = viewer.renderer.setup_cr(self)
        cr.set_font_from_shape(self)

        cr.draw_line(cx1, cy1, cx2, cy2)
        self.draw_arrowhead(cr, cx1, cy1, cx2, cy2)
        self.draw_arrowhead(cr, cx2, cy2, cx1, cy1)

        # calculate offsets and positions for drawing labels
        # try not to cover anything up
        xtwd, xtht = cr.text_extents(text_x)
        ytwd, ytht = cr.text_extents(text_y)
        htwd, htht = cr.text_extents(text_h)

        diag_xoffset = 0
        diag_yoffset = 0
        xplumb_yoffset = 0
        yplumb_xoffset = 0

        diag_yoffset = 14
        if abs(cy1 - cy2) < 5:
            show_angle = 0
        elif cy1 < cy2:
            xplumb_yoffset = -4
        else:
            xplumb_yoffset = 14
            diag_yoffset = -4

        if abs(cx1 - cx2) < 5:
            diag_xoffset = -(4 + htwd)
            show_angle = 0
        elif (cx1 < cx2):
            diag_xoffset = -(4 + htwd)
            yplumb_xoffset = 4
        else:
            diag_xoffset = 4
            yplumb_xoffset = -(4 + ytwd)

        xh = min(cx1, cx2); y = cy1 + xplumb_yoffset
        xh += (max(cx1, cx2) - xh) // 2
        yh = min(cy1, cy2); x = cx2 + yplumb_xoffset
        yh += (max(cy1, cy2) - yh) // 2

        xd = xh + diag_xoffset
        yd = yh + diag_yoffset
        cr.draw_text(xd, yd, text_h)

        if self.showplumb:
            if self.color2:
                alpha = getattr(self, 'alpha', 1.0)
                cr.set_line(self.color2, alpha=alpha, style='dash')

            # draw X plumb line
            cr.draw_line(cx1, cy1, cx2, cy1)

            # draw Y plumb line
            cr.draw_line(cx2, cy1, cx2, cy2)

            # draw X plum line label
            xh -= xtwd // 2
            cr.draw_text(xh, y, text_x)

            # draw Y plum line label
            cr.draw_text(x, yh, text_y)

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, ((cx2, cy1), ))


class Image(CanvasObjectBase):
    """Draws an image on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of one corner in the data space
    image: the image, which must be an RGBImage object
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data'],
            ##       description="Set type of coordinates"),
            Param(name='x', type=float, default=0.0, argpos=0,
                  description="X coordinate of corner of object"),
            Param(name='y', type=float, default=0.0, argpos=1,
                  description="Y coordinate of corner of object"),
            ## Param(name='image', type=?, argpos=2,
            ##       description="Image to be displayed on canvas"),
            Param(name='scale_x', type=float, default=1.0,
                  description="Scaling factor for X dimension of object"),
            Param(name='scale_y', type=float, default=1.0,
                  description="Scaling factor for Y dimension of object"),
            Param(name='interpolation', type=str, default='basic',
                  description="Interpolation method for scaling pixels"),
            Param(name='linewidth', type=int, default=0,
                  min=0, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default: solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='lightgreen',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            ## Param(name='flipy', type=_bool,
            ##       default=True, valid=[False, True],
            ##       description="Flip image in Y direction"),
            Param(name='optimize', type=_bool,
                  default=True, valid=[False, True],
                  description="Optimize rendering for this object"),
            ]

    def __init__(self, x, y, image, alpha=1.0, scale_x=1.0, scale_y=1.0,
                 interpolation='basic',
                 linewidth=0, linestyle='solid', color='lightgreen',
                 showcap=False, flipy=False, optimize=True,
                 **kwdargs):
        self.kind = 'image'
        super(Image, self).__init__(x=x, y=y, image=image, alpha=alpha,
                                        scale_x=scale_x, scale_y=scale_y,
                                        interpolation=interpolation,
                                        linewidth=linewidth, linestyle=linestyle,
                                        color=color, showcap=showcap,
                                        flipy=flipy, optimize=optimize,
                                        **kwdargs)

        self._drawn = False
        # these hold intermediate step results. Depending on value of
        # `whence` they may not need to be recomputed.
        self._cutout = None
        # calculated location of overlay on canvas
        self._cvs_x = 0
        self._cvs_y = 0
        self._zorder = 0
        # images are not editable by default
        self.editable = False

    def get_zorder(self):
        return self._zorder

    def set_zorder(self, zorder, redraw=True):
        self._zorder = zorder
        self.viewer.reorder_layers()
        if redraw:
            self.viewer.redraw(whence=2)

    def draw(self, viewer):
        if not self._drawn:
            self._drawn = True
            viewer.redraw(whence=2)

        cpoints = self.get_cpoints(viewer)
        cr = viewer.renderer.setup_cr(self)

        # draw optional border
        if self.linewidth > 0:
            cr.draw_polygon(cpoints)

        if self.editing:
            self.draw_edit(cr, viewer)
        elif self.showcap:
            self.draw_caps(cr, self.cap, cpoints)


    def draw_image(self, viewer, dstarr, whence=0.0):
        #print("redraw whence=%f" % (whence))
        dst_order = viewer.get_rgb_order()
        image_order = self.image.get_order()

        if (whence <= 0.0) or (self._cutout is None) or (not self.optimize):
            # get extent of our data coverage in the window
            ((x0, y0), (x1, y1), (x2, y2), (x3, y3)) = viewer.get_pan_rect()
            xmin = int(min(x0, x1, x2, x3))
            ymin = int(min(y0, y1, y2, y3))
            xmax = int(max(x0, x1, x2, x3))
            ymax = int(max(y0, y1, y2, y3))

            # destination location in data_coords
            #dst_x, dst_y = self.x, self.y + ht
            dst_x, dst_y = self.x, self.y

            a1, b1, a2, b2 = 0, 0, self.image.width, self.image.height

            # calculate the cutout that we can make and scale to merge
            # onto the final image--by only cutting out what is necessary
            # this speeds scaling greatly at zoomed in sizes
            dst_x, dst_y, a1, b1, a2, b2 = \
                   trcalc.calc_image_merge_clip(xmin, ymin, xmax, ymax,
                                                dst_x, dst_y, a1, b1, a2, b2)

            # is image completely off the screen?
            if (a2 - a1 <= 0) or (b2 - b1 <= 0):
                # no overlay needed
                #print "no overlay needed"
                return

            # cutout and scale the piece appropriately by the viewer scale
            scale_x, scale_y = viewer.get_scale_xy()
            # scale additionally by our scale
            _scale_x, _scale_y = scale_x * self.scale_x, scale_y * self.scale_y

            res = self.image.get_scaled_cutout(a1, b1, a2, b2,
                                               _scale_x, _scale_y,
                                               #flipy=self.flipy,
                                               method=self.interpolation)

            # don't ask for an alpha channel from overlaid image if it
            # doesn't have one
            dst_order = viewer.get_rgb_order()
            image_order = self.image.get_order()
            ## if ('A' in dst_order) and not ('A' in image_order):
            ##     dst_order = dst_order.replace('A', '')

            ## if dst_order != image_order:
            ##     # reorder result to match desired rgb_order by backend
            ##     self._cutout = trcalc.reorder_image(dst_order, res.data,
            ##                                         image_order)
            ## else:
            ##     self._cutout = res.data
            self._cutout = res.data

            # calculate our offset from the pan position
            pan_x, pan_y = viewer.get_pan()
            pan_off = viewer.data_off
            pan_x, pan_y = pan_x + pan_off, pan_y + pan_off
            #print "pan x,y=%f,%f" % (pan_x, pan_y)
            off_x, off_y = dst_x - pan_x, dst_y - pan_y
            # scale offset
            off_x *= scale_x
            off_y *= scale_y
            #print "off_x,y=%f,%f" % (off_x, off_y)

            # dst position in the pre-transformed array should be calculated
            # from the center of the array plus offsets
            ht, wd, dp = dstarr.shape
            self._cvs_x = int(round(wd / 2.0  + off_x))
            self._cvs_y = int(round(ht / 2.0  + off_y))

        # composite the image into the destination array at the
        # calculated position
        trcalc.overlay_image(dstarr, self._cvs_x, self._cvs_y, self._cutout,
                             dst_order=dst_order, src_order=image_order,
                             alpha=self.alpha, flipy=False)

    def _reset_optimize(self):
        self._drawn = False
        self._cutout = None

    def set_image(self, image):
        self.image = image
        self._reset_optimize()

    def get_scaled_wdht(self):
        width = int(self.image.width * self.scale_x)
        height = int(self.image.height * self.scale_y)
        return (width, height)

    def get_coords(self):
        x1, y1 = self.x, self.y
        wd, ht = self.get_scaled_wdht()
        x2, y2 = x1 + wd, y1 + ht
        return (x1, y1, x2, y2)

    def get_center_pt(self):
        wd, ht = self.get_scaled_wdht()
        return (self.x + wd / 2.0, self.y + ht / 2.0)

    def get_points(self):
        x1, y1, x2, y2 = self.get_coords()
        return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

    def contains(self, data_x, data_y):
        width, height = self.get_scaled_wdht()
        x2, y2 = self.x + width, self.y + height
        if ((self.x <= data_x < x2) and (self.y <= data_y < y2)):
            return True
        return False

    def rotate(self, theta, xoff=0, yoff=0):
        raise ValueError("Images cannot be rotated")

    def set_edit_point(self, i, pt):
        if i == 0:
            x, y = pt
            self.move_to(x, y)
        elif i == 1:
            x, y = pt
            self.scale_x = abs(x - self.x) / float(self.image.width)
        elif i == 2:
            x, y = pt
            self.scale_y = abs(y - self.y) / float(self.image.height)
        elif i == 3:
            x, y = pt
            self.scale_x = abs(x - self.x) / float(self.image.width)
            self.scale_y = abs(y - self.y) / float(self.image.height)
        else:
            raise ValueError("No point corresponding to index %d" % (i))

        self._reset_optimize()

    def get_edit_points(self):
        width, height = self.get_scaled_wdht()
        return [self.get_center_pt(),    # location
                (self.x + width, self.y + height / 2.),
                (self.x + width / 2., self.y + height),
                (self.x + width, self.y + height)
                ]

    def scale_by(self, scale_x, scale_y):
        self.scale_x *= scale_x
        self.scale_y *= scale_y
        self._reset_optimize()

    def set_scale(self, scale_x, scale_y):
        self.scale_x = scale_x
        self.scale_y = scale_y
        self._reset_optimize()

    def set_origin(self, x, y):
        self.x, self.y = x, y
        self._reset_optomize()


class NormImage(Image):
    """Draws an image on a ImageViewCanvas.

    Parameters are:
    x, y: 0-based coordinates of one corner in the data space
    image: the image, which must be an RGBImage object
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data'],
            ##       description="Set type of coordinates"),
            Param(name='x', type=float, default=0.0, argpos=0,
                  description="X coordinate of corner of object"),
            Param(name='y', type=float, default=0.0, argpos=1,
                  description="Y coordinate of corner of object"),
            ## Param(name='image', type=?, argpos=2,
            ##       description="Image to be displayed on canvas"),
            Param(name='scale_x', type=float, default=1.0,
                  description="Scaling factor for X dimension of object"),
            Param(name='scale_y', type=float, default=1.0,
                  description="Scaling factor for Y dimension of object"),
            Param(name='interpolation', type=str, default='basic',
                  description="Interpolation method for scaling pixels"),
            Param(name='linewidth', type=int, default=0,
                  min=0, max=20, widget='spinbutton', incr=1,
                  description="Width of outline"),
            Param(name='linestyle', type=str, default='solid',
                  valid=['solid', 'dash'],
                  description="Style of outline (default: solid)"),
            Param(name='color',
                  valid=colors_plus_none, type=_color, default='lightgreen',
                  description="Color of outline"),
            Param(name='alpha', type=float, default=1.0,
                  min=0.0, max=1.0, widget='spinfloat', incr=0.05,
                  description="Opacity of outline"),
            Param(name='showcap', type=_bool,
                  default=False, valid=[False, True],
                  description="Show caps for this object"),
            ## Param(name='flipy', type=_bool,
            ##       default=True, valid=[False, True],
            ##       description="Flip image in Y direction"),
            Param(name='optimize', type=_bool,
                  default=True, valid=[False, True],
                  description="Optimize rendering for this object"),
            ## Param(name='rgbmap', type=?,
            ##       description="RGB mapper for the image"),
            ## Param(name='autocuts', type=?,
            ##       description="Cuts manager for the image"),
            ]

    def __init__(self, x, y, image, alpha=1.0, scale_x=1.0, scale_y=1.0,
                 interpolation='basic',
                 linewidth=0, linestyle='solid', color='lightgreen', showcap=False,
                 optimize=True, rgbmap=None, autocuts=None, **kwdargs):
        self.kind = 'normimage'
        super(NormImage, self).__init__(x=x, y=y, image=image, alpha=alpha,
                                            scale_x=scale_x, scale_y=scale_y,
                                            interpolation=interpolation,
                                            linewidth=linewidth, linestyle=linestyle,
                                            color=color,
                                            showcap=showcap, optimize=optimize,
                                            **kwdargs)
        self.rgbmap = rgbmap
        self.autocuts = autocuts

        # these hold intermediate step results. Depending on value of
        # `whence` they may not need to be recomputed.
        self._prergb = None
        self._rgbarr = None

    def draw_image(self, viewer, dstarr, whence=0.0):
        #print("redraw whence=%f" % (whence))

        if (whence <= 0.0) or (self._cutout is None) or (not self.optimize):
            # get extent of our data coverage in the window
            ((x0, y0), (x1, y1), (x2, y2), (x3, y3)) = viewer.get_pan_rect()
            xmin = int(min(x0, x1, x2, x3))
            ymin = int(min(y0, y1, y2, y3))
            xmax = int(max(x0, x1, x2, x3))
            ymax = int(max(y0, y1, y2, y3))

            # destination location in data_coords
            dst_x, dst_y = self.x, self.y

            a1, b1, a2, b2 = 0, 0, self.image.width, self.image.height

            # calculate the cutout that we can make and scale to merge
            # onto the final image--by only cutting out what is necessary
            # this speeds scaling greatly at zoomed in sizes
            dst_x, dst_y, a1, b1, a2, b2 = \
                   trcalc.calc_image_merge_clip(xmin, ymin, xmax, ymax,
                                                dst_x, dst_y, a1, b1, a2, b2)

            # is image completely off the screen?
            if (a2 - a1 <= 0) or (b2 - b1 <= 0):
                # no overlay needed
                #print "no overlay needed"
                return

            # cutout and scale the piece appropriately by viewer scale
            scale_x, scale_y = viewer.get_scale_xy()
            # scale additionally by our scale
            _scale_x, _scale_y = scale_x * self.scale_x, scale_y * self.scale_y

            res = self.image.get_scaled_cutout(a1, b1, a2, b2,
                                               _scale_x, _scale_y,
                                               method=self.interpolation)
            self._cutout = res.data

            # calculate our offset from the pan position
            pan_x, pan_y = viewer.get_pan()
            pan_off = viewer.data_off
            pan_x, pan_y = pan_x + pan_off, pan_y + pan_off
            #print "pan x,y=%f,%f" % (pan_x, pan_y)
            off_x, off_y = dst_x - pan_x, dst_y - pan_y
            # scale offset
            off_x *= scale_x
            off_y *= scale_y
            #print "off_x,y=%f,%f" % (off_x, off_y)

            # dst position in the pre-transformed array should be calculated
            # from the center of the array plus offsets
            ht, wd, dp = dstarr.shape
            self._cvs_x = int(round(wd / 2.0  + off_x))
            self._cvs_y = int(round(ht / 2.0  + off_y))

        if self.rgbmap is not None:
            rgbmap = self.rgbmap
        else:
            rgbmap = viewer.get_rgbmap()

        if (whence <= 1.0) or (self._prergb is None) or (not self.optimize):
            # apply visual changes prior to color mapping (cut levels, etc)
            vmax = rgbmap.get_hash_size() - 1
            newdata = self.apply_visuals(viewer, self._cutout, 0, vmax)

            # result becomes an index array fed to the RGB mapper
            if not numpy.issubdtype(newdata.dtype, numpy.dtype('uint')):
                newdata = newdata.astype(numpy.uint)
            idx = newdata

            self.logger.debug("shape of index is %s" % (str(idx.shape)))
            self._prergb = idx

        dst_order = viewer.get_rgb_order()
        image_order = self.image.get_order()
        get_order = dst_order
        if ('A' in dst_order) and not ('A' in image_order):
            get_order = dst_order.replace('A', '')

        if (whence <= 2.5) or (self._rgbarr is None) or (not self.optimize):
            # get RGB mapped array
            rgbobj = rgbmap.get_rgbarray(self._prergb, order=dst_order,
                                         image_order=image_order)
            self._rgbarr = rgbobj.get_array(get_order)

        # composite the image into the destination array at the
        # calculated position
        trcalc.overlay_image(dstarr, self._cvs_x, self._cvs_y, self._rgbarr,
                             dst_order=dst_order, src_order=get_order,
                             alpha=self.alpha, flipy=False)

    def apply_visuals(self, viewer, data, vmin, vmax):
        if self.autocuts is not None:
            autocuts = self.autocuts
        else:
            autocuts = viewer.autocuts

        # Apply cut levels
        loval, hival = viewer.t_['cuts']
        newdata = autocuts.cut_levels(data, loval, hival,
                                      vmin=vmin, vmax=vmax)
        return newdata

    def _reset_optimize(self):
        super(NormImage, self)._reset_optimize()
        self._prergb = None
        self._rgbarr = None

    def set_image(self, image):
        self.image = image
        self._reset_optimize()

    def scale_by(self, scale_x, scale_y):
        #print("scaling image")
        self.scale_x *= scale_x
        self.scale_y *= scale_y
        self._reset_optimize()
        #print("image scale_x=%f scale_y=%f" % (self.scale_x, self.scale_y))


class CompoundObject(CompoundMixin, CanvasObjectBase):
    """Compound object on a ImageViewCanvas.
    Parameters are:
    the child objects making up the compound object.  Objects are drawn
    in the order listed.
    Example:
      CompoundObject(Point(x, y, radius, ...),
      Circle(x, y, radius, ...))
    This makes a point inside a circle.
    """

    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            ]

    def __init__(self, *objects):
        CanvasObjectBase.__init__(self)
        CompoundMixin.__init__(self)
        self.kind = 'compound'
        self.objects = list(objects)
        self.editable = False


class Canvas(CanvasMixin, CompoundObject, CanvasObjectBase):
    @classmethod
    def get_params_metadata(cls):
        return [
            ## Param(name='coord', type=str, default='data',
            ##       valid=['data', 'wcs'],
            ##       description="Set type of coordinates"),
            ]

    def __init__(self, *objects):
        CanvasObjectBase.__init__(self)
        CompoundObject.__init__(self, *objects)
        CanvasMixin.__init__(self)
        self.kind = 'canvas'
        self.editable = False


class DrawingCanvas(DrawingMixin, CanvasMixin, CompoundMixin,
                    CanvasObjectBase, Mixins.UIMixin):
    def __init__(self):
        CanvasObjectBase.__init__(self)
        CompoundMixin.__init__(self)
        CanvasMixin.__init__(self)
        Mixins.UIMixin.__init__(self)
        DrawingMixin.__init__(self)
        self.kind = 'drawingcanvas'
        self.editable = False

drawCatalog = dict(text=Text, rectangle=Rectangle, circle=Circle,
                   line=Line, point=Point, polygon=Polygon,
                   freepolygon=FreePolygon, path=Path, freepath=FreePath,
                   righttriangle=RightTriangle, triangle=Triangle,
                   ellipse=Ellipse, square=Square, beziercurve=BezierCurve,
                   box=Box, ruler=Ruler, compass=Compass,
                   compoundobject=CompoundObject, canvas=Canvas,
                   drawingcanvas=DrawingCanvas,
                   image=Image, normimage=NormImage)


# funky boolean converter
_bool = lambda st: str(st).lower() == 'true'

# color converter
_color = lambda name: name

# END
