mplfastaxes
===========

I have observed that the amount of time to draw a figure with a plot depends
heavily on the number of tick marks on the axes.  This appears to be a major
driver of perceived refresh performance on interactive graphics in PySide (for
example).  Somewhat tangentially this makes log axes appear to perform slowly,
but I think that is merely a side-effect of the fact that log axes come with
minor tick marks by default.

This repository has a prototype optimization by using a single Line2D for all
the tick marks of each type (tick1, tick2, minor, major).

The table here is output by test\_agg\_speed.py.

```
func      :    std  fast
vanilla   :   0.41  0.23 ( 1.8x faster) Identical:  True
hexplot   :   1.96  1.02 ( 1.9x faster) Identical:  True
log       :   1.52  0.40 ( 3.8x faster) Identical:  True
manyticks :   1.46  0.26 ( 5.6x faster) Identical:  True
tickless  :   0.06  0.06 ( 1.0x faster) Identical:  True
```
