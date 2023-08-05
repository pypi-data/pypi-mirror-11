
.. role:: red

.. raw:: html

    <style> .red {color: red; font-weight: bold} </style>



================
Execution timing
================


Scheduling time
===============

*RunTask* executes a given task when the scheduling time reaches the next
run time computed for that task. The scheduling time is derived from the
system time applying the following formulas

  scheduling_time_continuous = system_time * speed + epoch

  scheduling_time = scheduling_time_continuous - scheduling_time_continuous%tick

If speed = 1. and epoch = 0. , the scheduling time has the same time scale
of the system time. If speed is increased above 1., scheduling time runs
faster, this can be useful for debugging or demos of tasks having long run
periods. The opposite, if speed is decreased below 1.. The epoch parameter
allows to shift the scheduling time in the future or in the past for the
same pourposes as above.

To have a more ordered and efficient task execution, the scheduling time
is designed to be discrete with elementary increments of the tick quantity,
as it can be seen from the second formula. Also the system time has a minimum
increment tick, but this quantity is generally far lower (generally 1
microsecond) than the scheduling time tick. So, the system time can be
considered continuous with respect to the scheduling time.
In any case, there are no computational constraints on the scheduling time
tick value and it can be lowered above 0.0 at will.


Timing generators
=================

The run time of each task controlled by **RunTask** is given by a "timing
generator". Timing generators are special methods of the *RunTask* class.
Three timing generators are available at present, each one implementing a
different scheduling scheme.

**aligned**, this time generator schedules the first task execution at the
first occurrence of an integer multiple of a given period from the origin
of the scheduling time plus an optional time phase.
The next executions are run at regular intervals from the first one with the
same fixed period.
For example, if the execution period is 1 second and the phase is 0, the
task is run every second and each execution occurs aligned to a second
boundary.

**now**, this time generator schedules the first task execution immediately
(as soon as possible during RunTask execution). The next executions are run
at regular intervals of time from the first one with a given fixed period.
For example, if the execution period is 1 second and phase is 0 and the
first task run occurs at 01:23:45.678, the next run is at 01:23:46.678
and so on. 

**uniform**, this time generator schedules the task execution with a random
sequence of time periods having a uniform distribution between a minimum and
a maximum given values. The first task execution is scheduled at the first
occurrence of an integer multiple of the first value of the random sequence
from the origin of the scheduling time. Each next execution time is computed
by adding to the previous execution time the next time period from the random
sequence. For example, let the random sequence be 1, 4.345, 6.4467, ... The
first task execution occurs to the first occurence of a second boundary, for
example let it be 01:23:45.000. Then the second execution will occur at
01:23:49.345. The third execution will occur at 01:23:55.7917 and so on.

For each task controlled by *RunTask*, one timing generator can be specified.


Run time computation
====================

All timing generators compute the next task execution time referred to a
continuous scheduling time: the **nominal run time**. The scheduling time
of *RunTask* is discrete, as seen above, with minimum increments of the tick
quantity and the task is run when the last increment of the scheduling time
reaches or exceeds the nominal run time. This is the **effective run time**
of the task. So there is a difference between the nominal run time and the
effective run time that is always less or equal to the tick of the scheduling
time.

A special attention is given to avoid computational drifts for timing
generators that execute a task at fixed periods (*aligned* and *now*).
The sequence of the nominal execution times is not computed by the cumulative
summation of the fixed period, since the floating representation of time
suffers of numerical rounding errors that cumulate on the summation.


Fractional periods
==================

There are cases in which the fixed execution period comes out from an integer
division of an integer frequency (i.e. a counter dividing a frequency).
Generally the division produces a float result with conversion errors. To
exactly represent such kind of period, the timing generators with fixed
periods (*aligned* and *now*) accept a **fractional period** written as a
tuple of two elements: numerator, denominator. In such a case, the
computation of the *nominal run time* is carried out without fractional
approximations.
