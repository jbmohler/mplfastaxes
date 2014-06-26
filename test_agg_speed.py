import os
import time
import tempfile
import datetime
import cProfile
import numpy
import matplotlib
import matplotlib.ticker
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import fastaxes as f

POINTS = 500

def vanilla(proj=None):
    figure = Figure(figsize=(6, 6), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
    ax = figure.add_subplot(1, 1, 1, projection=proj)

    scat = ax.scatter(numpy.arange(POINTS), numpy.sin(numpy.arange(POINTS)))

    return figure

def hexplot(proj=None):
    figure = Figure(figsize=(6, 6), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))

    x = numpy.arange(0, 2*numpy.pi, 0.01)
    y = numpy.sin(x)

    axes = [figure.add_subplot(6, 1, i, projection=proj) for i in range(1, 7)]
    styles = ['r-', 'g-', 'y-', 'm-', 'k-', 'c-']
    lines = [ax.plot(x, y, style)[0] for ax, style in zip(axes, styles)]

    return figure

def log(proj=None):
    figure = Figure(figsize=(6, 6), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))

    x = numpy.exp(numpy.arange(0.0, 2*numpy.pi, 0.1))
    y = numpy.sin(x)

    axes = [figure.add_subplot(2, 1, i, projection=proj) for i in range(1, 3)]
    for ax in axes:
        ax.set_xscale('log')
    lines = [ax.plot(x, y)[0] for ax in axes]

    return figure

def tight(proj=None):
    figure = Figure(figsize=(6, 6), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0), tight_layout=True)
    ax = figure.add_subplot(1, 1, 1, projection=proj)

    scat = ax.scatter(numpy.arange(POINTS), numpy.sin(numpy.arange(POINTS)))

    return figure

def manyticks(proj=None):
    figure = Figure(figsize=(6, 6), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
    ax = figure.add_subplot(1, 1, 1, projection=proj)

    scat = ax.scatter(numpy.arange(POINTS), numpy.sin(numpy.arange(POINTS)))

    ticks = 40
    ax.xaxis.set_minor_locator(matplotlib.ticker.LinearLocator(ticks))
    ax.yaxis.set_minor_locator(matplotlib.ticker.LinearLocator(ticks))

    return figure

def tickless(proj=None):
    figure = Figure(figsize=(6, 6), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
    ax = figure.add_subplot(1, 1, 1, projection=proj)

    scat = ax.scatter(numpy.arange(POINTS), numpy.sin(numpy.arange(POINTS)))

    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    ax.yaxis.set_major_locator(matplotlib.ticker.NullLocator())

    return figure

class Profile(object):
    def __init__(self, label):
        self.label = label
        self.pr = cProfile.Profile()

    def __enter__(self):
        self.pr.enable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pr.disable()
        filename = '{}-{}.prof'.format(self.label, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        self.pr.dump_stats(filename)

def speed(func):
    s_fig = func()
    s_canvas = FigureCanvas(s_fig)
    f_fig = func(proj='fastticks')
    f_canvas = FigureCanvas(f_fig)

    # heat the cache or other first-run issues
    f_canvas.print_to_buffer()
    s_canvas.print_to_buffer()

    start = time.time()
    for i in range(25):
        s_canvas.print_to_buffer()
    s_time = time.time() - start

    start = time.time()
    for i in range(25):
        f_canvas.print_to_buffer()
    f_time = time.time() - start

    with Profile(func.__name__):
        f_canvas.print_to_buffer()

    s_fname = os.path.join('images', '{}.png'.format(func.__name__))
    s_fig.savefig(s_fname)
    f_fname = os.path.join('images', '{}-fast.png'.format(func.__name__))
    f_fig.savefig(f_fname)

    identical = open(s_fname, 'r').read() == open(f_fname, 'r').read()
    print '{:<10s}:  {:>5.2f} {:>5.2f} ({:>4.1f}x faster) Identical:  {}'.format(func.__name__, s_time, f_time, s_time / f_time, identical)

def main():
    print '{:<10s}:  {:>5s} {:>5s}'.format('func', 'std', 'fast')

    speed(vanilla)
    speed(hexplot)
    speed(log)
    #speed(tight)
    speed(manyticks)
    speed(tickless)

if __name__ == '__main__':
    main()
