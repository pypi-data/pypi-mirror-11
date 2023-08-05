
.. role:: red

.. raw:: html

    <style> .red {color: red; font-weight: bold} </style>



=====================================
RunTask, Coherent Time Task Scheduler
=====================================

Introduction
============

**RunTask** is a python module implementing a coherent time task scheduler
in a very simple way. The tasks can be python callables (functions, methods)
or synchronization objects from the threading module (Event, Lock, Semaphore,
BoundedSemaphore).
The execution order of all controlled tasks is stricktly
predictable and execution times are aligned to given reference times.
The scheduling time can be speed up or slow down with respect to the system
time.
It can be also moved forward and backward by an offset addition. This can useful
for debugging events with periods that are too long or too short to be seen in
a comfortable way.

An example. Suppose to have tasks A, B that need to be run at the beginning
of each minute, in that order. In addition, suppose to have tasks C, D that
need to be run at the begining of each second, in that order. Moreover, since
the beginning of each minute is coincident with the beginning of a second, it is
wanted that the task group A, B is run before the task group C, D.
RunTask is designed to fulfill all these kind of requirements.

This is the documentation for version |version|.

RunTask is released under the GNU General Public License.

At present, version |version|, RunTask is in alpha status. Any debugging aid is
welcome.

For any question, suggestion, contribution contact the author Fabrizio Pollastri <f.pollastri_a_t_inrim.it>.

Features
========

* Tasks can be callables with theirs arguments or event, lock, semaphore,
  bounded semaphore from the threading module.
* Task execution timing can be choosen among different schemes:
  fixed period, random period, aligned to time origin or unaligned (immediate
  execution). Periodic executions can be forever or for a given number
  of runs, at least one (single shot).
* The speed and the offset of the scheduling time can be adjusted with respect
  to the system time.
* Each task execution time is computed from the scheduling time, so 
  the phase between different execution periods can be easily controlled.
* When a task execution time is delayed by cpu load more then the task period,
  that execution is skipped.
* All controlled tasks are run within the same thread, so with respect to each
  other, they are thread safe.
* Tasks having the same execution time are grouped by run period and
  executed from longest to shortest period. Within each group, tasks are
  executed following the task registration order.
* Any number of *RunTask* instances can be alive in the same program.

Caveat
======

*RunTask* is not a preemptive scheduler, so all tasks are run sequentially
when their run time is reached.
 
Since all tasks are run within the same thread, all tasks must be
non-blocking.

The tasks controlled by RunTask are thread safe with respect to each other.
Since, RunTask is instantiated by a main program, the controlled tasks
are NOT thread safe with respect to the main program.

At present, *RunTask* has a static design: all task must be registered at
program beginning and cannot be changed during execution.

Each task target can be registered only one time.

Threads in python can be run only serially, so they do not benefit from
multiprocessor architectures.

Requirements
============

To run the code, **Python 2.6 or later** must
already be installed.  The latest release is recommended.  Python is
available from http://www.python.org/.


Installation
============

1. Open a shell.

2. Get root privileges and install the package. Command::

    pip install runtask
