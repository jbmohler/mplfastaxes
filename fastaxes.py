import numpy
import matplotlib
from matplotlib import rcParams
import matplotlib.font_manager as font_manager
import matplotlib.artist as martist
import matplotlib.axes as maxes
import matplotlib.axis as maxis
import matplotlib.lines as mlines
import matplotlib.text as mtext
import matplotlib.ticker as mticker

class Props(object):
    def __init__(self):
        self.texts = []

    def _construct_tick_label(self, index, vert, horiz):
        if not hasattr(self, '_font_props'):
            self._font_props = font_manager.FontProperties(size=self._labelsize)
        if len(self.texts) <= index:
            t = mtext.Text(
                    x=0, y=0,
                    fontproperties=self._font_props,
                    color=self._labelcolor,
                    verticalalignment=vert,
                    horizontalalignment=horiz)
            self.texts.append(t)
        else:
            t = self.texts[index]
        return t

def tick_props(name, axes, major):
    props = Props()

    if major:
        size = rcParams['%s.major.size' % name]
    else:
        size = rcParams['%s.minor.size' % name]
    props._size = size

    if major:
        width = rcParams['%s.major.width' % name]
    else:
        width = rcParams['%s.minor.width' % name]
    props._width = width

    props._tickdir = rcParams['%s.direction' % name]

    color = rcParams['%s.color' % name]
    props._color = color

    if major:
        pad = rcParams['%s.major.pad' % name]
    else:
        pad = rcParams['%s.minor.pad' % name]
    props._base_pad = pad

    labelcolor = rcParams['%s.color' % name]
    props._labelcolor = labelcolor

    labelsize = rcParams['%s.labelsize' % name]
    props._labelsize = labelsize

    if major:
        zorder = mlines.Line2D.zorder + 0.01
    else:
        zorder = mlines.Line2D.zorder
    props._zorder = zorder
    return props

class FastAxisMixin(object):
    def _construct_tick_group(self, props):
        tickline = mlines.Line2D(xdata=(), ydata=(),
                   color=props._color,
                   linestyle='None',
                   marker=props._tickmarkers[0],
                   markersize=props._size,
                   markeredgewidth=props._width,
                   zorder=props._zorder)
        tickline.set_axes(self.axes)
        return tickline

    def iter_tick_groups(self):
        transfactory = self.axes.get_xaxis_transform if self.axis_name == 'x' else self.axes.get_yaxis_transform

        # minor tick marks
        locations = self.get_minor_locator()()
        if len(locations) > 0:
            ones = numpy.empty_like(locations)
            ones.fill(1.)
            zeros = numpy.zeros_like(locations)
            if not hasattr(self, '_minor_tick_props'):
                self._minor_tick_props = self.tick_props(major=False)

                tickline = self._construct_tick_group(self._minor_tick_props)
                tickline.set_transform(transfactory(which='tick1'))
                self._minor_tick1 = tickline
                tickline = self._construct_tick_group(self._minor_tick_props)
                tickline.set_transform(transfactory(which='tick2'))
                tickline.set_marker(self._minor_tick_props._tickmarkers[1])
                self._minor_tick2 = tickline

            if self.axis_name == 'x':
                xdata, ydata = locations, zeros
            else:
                xdata, ydata = zeros, locations
            self._minor_tick1.set_xdata(xdata)
            self._minor_tick1.set_ydata(ydata)

            if self.axis_name == 'x':
                xdata, ydata = locations, ones
            else:
                xdata, ydata = ones, locations
            self._minor_tick2.set_xdata(xdata)
            self._minor_tick2.set_ydata(ydata)

            yield locations, [self._minor_tick1, self._minor_tick2], self._minor_tick_props, self.minor.formatter

        # major tick marks
        locations = self.get_major_locator()()
        if len(locations) > 0:
            ones = numpy.empty_like(locations)
            ones.fill(1.)
            zeros = numpy.zeros_like(locations)

            if not hasattr(self, '_major_tick_props'):
                self._major_tick_props = self.tick_props(major=True)
                tickline = self._construct_tick_group(self._major_tick_props)
                tickline.set_transform(transfactory(which='tick1'))
                self._major_tick1 = tickline
                tickline = self._construct_tick_group(self._major_tick_props)
                tickline.set_transform(transfactory(which='tick2'))
                tickline.set_marker(self._major_tick_props._tickmarkers[1])
                self._major_tick2 = tickline

            if self.axis_name == 'x':
                xdata, ydata = locations, zeros
            else:
                xdata, ydata = zeros, locations
            self._major_tick1.set_xdata(xdata)
            self._major_tick1.set_ydata(ydata)

            if self.axis_name == 'x':
                xdata, ydata = locations, ones
            else:
                xdata, ydata = ones, locations
            self._major_tick2.set_xdata(xdata)
            self._major_tick2.set_ydata(ydata)

            yield locations, [self._major_tick1, self._major_tick2], self._major_tick_props, self.major.formatter

    @martist.allow_rasterization
    def draw(self, renderer, *args, **kwargs):
        'Draw the axis lines, grid lines, tick lines and labels'

        if not self.get_visible():
            return
        renderer.open_group(__name__)

        for locations, tickbars, props, label_formatter in self.iter_tick_groups():
            for t in tickbars:
                t.draw(renderer)
            if label_formatter != None:
                label_formatter.set_locs(locations)
                for i, val in enumerate(locations):
                    l = label_formatter(val, i)
                    if l == '':
                        continue
                    t = self._construct_tick_label(i, props)
                    f = t.set_y if self.axis_name == 'y' else t.set_x
                    f(val)
                    t.set_text(l)
                    t.draw(renderer)

        renderer.close_group(__name__)

class FastXAxis(FastAxisMixin, maxis.XAxis):
    def _construct_tick_label(self, index, props):
        trans, vert, horiz = self.axes.get_xaxis_text1_transform(props._pad)
        t = props._construct_tick_label(index, vert, horiz)
        t.set_axes(self.axes)
        t.set_figure(self.figure)
        t.set_transform(trans)
        return t

    def tick_props(self, major):
        props = tick_props('xtick', self.axes, major)
        if props._tickdir == 'in':
            props._tickmarkers = (mlines.TICKUP, mlines.TICKDOWN)
            props._pad = props._base_pad
        elif props._tickdir == 'inout':
            props._tickmarkers = ('|', '|')
            props._pad = props._base_pad + props._size / 2.
        else:
            props._tickmarkers = (mlines.TICKDOWN, mlines.TICKUP)
            props._pad = props._base_pad + props._size
        return props

class FastYAxis(FastAxisMixin, maxis.YAxis):
    def _construct_tick_label(self, index, props):
        trans, vert, horiz = self.axes.get_yaxis_text1_transform(props._pad)
        t = props._construct_tick_label(index, vert, horiz)
        t.set_axes(self.axes)
        t.set_figure(self.figure)
        t.set_transform(trans)
        return t

    def tick_props(self, major):
        props = tick_props('ytick', self.axes, major)
        if props._tickdir == 'in':
            props._tickmarkers = (mlines.TICKRIGHT, mlines.TICKLEFT)
            props._pad = props._base_pad
        elif props._tickdir == 'inout':
            props._tickmarkers = ('|', '|')
            props._pad = props._base_pad + props._size / 2.
        else:
            props._tickmarkers = (mlines.TICKLEFT, mlines.TICKRIGHT)
            props._pad = props._base_pad + props._size
        return props

class FastAxes(maxes.Axes):
    name = 'fastticks'

    def _init_axis(self):
        "move this out of __init__ because non-separable axes don't use it"
        self.xaxis = FastXAxis(self)
        self.spines['bottom'].register_axis(self.xaxis)
        self.spines['top'].register_axis(self.xaxis)
        self.yaxis = FastYAxis(self)
        self.spines['left'].register_axis(self.yaxis)
        self.spines['right'].register_axis(self.yaxis)
        self._update_transScale()

import matplotlib.projections as mp
mp.projection_registry.register(FastAxes)
