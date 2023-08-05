Changes
*******

Release 0.5.0 (released 06-Aug-2015)
====================================

New features
------------
* New task types: Event, Lock, Semaphore, BoundedSemaphore from the threading
  module.
* Changed examples to work with incompatible changes.
* Added examples for synchronization objects from the threading module.

Incompatible changes
--------------------
* task method: now there is only one target arguments. If target requires more
  than one argument, pass them as a tuple.

Fixes
-----
* Methods task_info and runs_left now return correct data when called from
  outside the inquired task.

Documentation
-------------
* Added new task types.


Release 0.4.0 (released 04-Jul-2015)
====================================

New features
------------
* New timing generator 'uniform': run tasks with a random period with uniform
  distribution.
* Timing generators 'aligned' and 'now' accept fractional periods.
* Updated timecap.py example for 'uniform' timing generator.

Internals
---------
* Refactored method 'aligned': timing computation as closure.

Fixes
-----
* Eliminated period drift from 'now' timing generator.

Documentation
-------------
* Added 'uniform' timing generator.


Release 0.3.0 (released 18-May-2015)
====================================

New features
------------
* Task run timing changed to timing generators.
* New timing generator 'aligned': run tasks periodically aligned to a reference
  time.
* New timing generator 'now': run task periodically with immediate start.
* New method runs_left: return the remaining number of times the task will be
  run. If the task is run forever return -1.
* New example (timecap.py): show different timing capabilities.

Incompatible changes
--------------------
* task method: now all arguments have defaults and timing argument must be one
  of the timing generators.
* task_info method: now returns the count of task run times and a tuple with
  all the arguments given at the call of 'task' method.

Internals
---------
* Refactored RunTask init argument 'phase' to 'epoch'.
* _time method changed to work with both normal system time and scaled and
  shifted system time.
* _run method: refactored 'task' to 'target' and changed for timing generators.

Fixes
-----
* Eliminated tick drift from tasks run time.

Documentation
-------------
* Added timing generators and runs_left method.
* Added new timecap.py example.



Release 0.2.0 (released 29-Apr-2015)
====================================

New features
------------
* Run time speed: set the scheduling time flowing speed with respect to system
  time.
* Run time phase: add an offset to the scheduling time.
* Method task_info, if task has a finite run count, it returns also the
  current run number. Otherwise, it returns -1.
* Extended example to show counted runs and RunTask stopping. 

Incompatible changes
--------------------
* RunTask class, removed time argument. 
* Method task_data changed name to task_info.

Internals
---------
* New method _time, run time computation.
* Method _set, removed, partially replaced by method _time.

Fixes
-----
* Method stop, errata call to _set, corrige call to set.

Documentation
-------------
* Updated to 0.2.0


Release 0.1.0 (released 16-Feb-2015)
====================================

Changes
-------
* First release.
