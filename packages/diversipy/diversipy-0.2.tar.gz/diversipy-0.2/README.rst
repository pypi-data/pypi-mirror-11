
diversipy has been tested with Python 2.7 and 3.4. The recommended version is
Python 3.x, because compatibility is reached by avoiding usage of xrange. So,
the code has a higher memory consumption under Python 2. Furthermore, note
that all members of __future__ and future_builtins are imported.



Changes
=======

0.2
---
* psa_partition and psa_select now raise exceptions when num_clusters or
  num_selected_points are <= 0
* Added functions select_greedy_maximin and select_greedy_maxisum in module
  subset.

0.1.1
-----
* Fixed bug in installation script

0.1
---
* Initial version
