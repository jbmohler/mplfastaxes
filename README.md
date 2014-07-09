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
vanilla   :   0.09( 0.03)  0.06( 0.00) ( 1.5x faster) Identical:  True
labeled   :   0.12( 0.03)  0.10( 0.00) ( 1.2x faster) Identical:  True
t_labels  :   0.08( 0.04)  0.05( 0.01) ( 1.7x faster) Identical:  True
hexplot   :   0.44( 0.20)  0.29( 0.02) ( 1.5x faster) Identical:  True
large_grid:   2.44(13.54)  2.44(14.05) ( 1.0x faster) Identical:  True
log       :   0.35( 0.08)  0.10( 0.01) ( 3.3x faster) Identical:  True
tight     :   0.12( 0.03)  0.10( 0.01) ( 1.3x faster) Identical:  True
tightlog  :   0.31( 0.04)  0.08( 0.01) ( 4.1x faster) Identical:  True
manyticks :   0.32( 0.03)  0.07( 0.01) ( 4.5x faster) Identical:  True
tickless  :   0.02( 0.04)  0.01( 0.00) ( 1.2x faster) Identical:  True
```
