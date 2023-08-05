
===========
time2words
===========
Module for converting numerical representation of time to text.

Currently this works only for relative time and the output shows an aproximation. E.g. "about five and a half months".

Including precise time and time of day is work in progress.


======
Usage
======

::

    from time2words import relative_time_to_text
    relative_time_to_text(years=5, months=8, days=5) # -> "less than six years"
