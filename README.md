mplfastaxes
===========

I have observed that the amount of time to draw a figure with a plot depends
heavily on the number of tick marks on the axes.  This appears to be a major
driver of perceived refresh performance on interactive graphics in PySide (for
example).  Somewhat tangentially this makes log axes appear to perform slowly,
but I think that is merely a side-effect of the fact that log axes come with
minor tick marks by default.

The motivation for the large\_grid example comes from
https://gist.github.com/btel/a6b97e50e0f26a1a5eaa

This repository has a prototype optimization by using a single Line2D for all
the tick marks of each type (tick1, tick2, minor, major).

The table here is output by test\_agg\_speed.py.

```
func      :    std( make)  fast( make)
vanilla   :   0.05( 0.06)  0.04( 0.01) ( 1.5x faster) Identical:  True
labeled   :   0.07( 0.05)  0.06( 0.01) ( 1.3x faster) Identical:  True
t_labels  :   0.04( 0.06)  0.03( 0.02) ( 1.7x faster) Identical:  True
hexplot   :   0.25( 0.34)  0.16( 0.03) ( 1.5x faster) Identical:  True
large_grid:   1.52(22.35)  1.01( 2.32) ( 1.5x faster) Identical:  True
log       :   0.20( 0.13)  0.06( 0.01) ( 3.5x faster) Identical:  True
tight     :   0.07( 0.05)  0.05( 0.01) ( 1.3x faster) Identical:  True
tightlog  :   0.18( 0.06)  0.04( 0.01) ( 4.3x faster) Identical:  True
manyticks :   0.20( 0.05)  0.04( 0.01) ( 5.0x faster) Identical:  True
tickless  :   0.01( 0.06)  0.01( 0.01) ( 1.1x faster) Identical:  False
```
