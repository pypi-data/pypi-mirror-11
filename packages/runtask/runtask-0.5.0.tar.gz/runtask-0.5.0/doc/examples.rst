==============
Usage examples
==============

Using the system time
=====================

Simple example
--------------
This simple example is based on the the execution of 3 tasks. The task #0 is
run every 5 seconds, at second beginning, forever. The task #1
is run every second, at the middle of second, forever. The task #2 is run
every second, at the middle of second, for 5 times.
Each task printouts its task id, nominal runtime and delay of real runtime
from nominal runtime, the difference runtime - system time. Task #2 prints
also the run number.
Since all these tasks make the same output, they all can be inplemented by only
one function, the "task" function.

.. literalinclude:: ../examples/example.py
    :linenos:
    :language: python
    :lines: 30-

This an excerpt from example output. Task with 5 second period has id=0.
Tasks with 1 second period have respectively id=1 and id=2.
 
.. literalinclude:: ../examples/example.out
    :linenos:

It is to be noted that the difference sys-runtime that is the difference
between the system time at task call and the nominal run time is always
below 0.2 ms. This difference measures the scheduling overhead introduced
by RunTask


Capabilities of the periodic timing
-----------------------------------
This example shows almost all capabilities of the periodic timing.
Task #0 is run 15 second after the beginning of each minute, forever.
Task #1 is run with period 19/3, phase=0.1, forever.
Task #2 is run immediately every 5 seconds.
Task #3 is run immediately with period 19/3, forever.
Task #4 is run randomly with uniform distribution, period min 8 seconds
and max 16 seconds, forever.

.. literalinclude:: ../examples/timecap.py
    :linenos:
    :language: python
    :lines: 30-

This an excerpt from example output.
 
.. literalinclude:: ../examples/timecap.out
    :linenos:

Since this example runs for one minute, task #0 appears only one time in the
example output.

Since the scheduler time has tick=0.01, the effective run time of each
scheduled task must be a tick multiple. Under some conditions, this can
produce a delay between the nominal runtime computed by the time generator
and the effective runtime. This effect can be seen for tasks #1, #3 and #4
where the nominal run time is rounded to the nearest and greather tick multiple.


Threading event
---------------
This example shows as a Event object from the threading module can be used
to schedule the execution of a loop in the main program.
The loop is run every second for 10 times.

.. literalinclude:: ../examples/event.py
    :linenos:
    :language: python
    :lines: 30-

This an excerpt from example output.
 
.. literalinclude:: ../examples/event.out
    :linenos:


Threading lock
--------------
This example shows as a Lock object from the threading module can be used
to schedule the execution of a loop in the main program.
The loop is run every second for 10 times.

.. literalinclude:: ../examples/lock.py
    :linenos:
    :language: python
    :lines: 30-

This an excerpt from example output.
 
.. literalinclude:: ../examples/lock.out
    :linenos:


Threading semaphore
-------------------
This example shows as a Semaphore object from the threading module can be used
to schedule the execution of a loop in the main program.
The loop is run every second for 10 times.

.. literalinclude:: ../examples/semaphore.py
    :linenos:
    :language: python
    :lines: 30-

This an excerpt from example output.
 
.. literalinclude:: ../examples/semaphore.out
    :linenos:

