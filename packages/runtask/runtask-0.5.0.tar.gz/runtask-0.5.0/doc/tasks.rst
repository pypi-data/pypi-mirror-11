
.. role:: red

.. raw:: html

    <style> .red {color: red; font-weight: bold} </style>



=====
Tasks
=====

*RunTask* support several types of tasks. When the runtime comes for a task,
*RunTask* takes action on the task according to its type as explained below.

Callable
========

If the task is a callable, a python function or a class method, when its
runtime comes, *RunTask* calls it passing the arguments given at the task
registration. For example, if the task is a python function defined as::

    def myfunc(x,y,operator='add'):
        if operator == 'add':
            return x + y
        it operator == 'sub':
            return x - y
        else:
            raise Exception('error')

the task registration is::

    sch.task(myfunc,((X,Y),{'operator': 'add'}),sch.aligned())

where *sch* is the current instance of *RunTask*, *X* and *Y* are the actual
values of the positional arguments and 'add' is the actual value of a keyword
argument.
Both positional and keyword arguments must be enclosed by parentesis.
As timing generator is choosen 'aligned'.


Event
=====

If the task is an Event synchronization primitive from the threading module,
when its runtime comes, *Runtask* sets or clears the Event flag according
to the second argument given at the task registration. If it is false, the
flag is cleared. If it is true, the flag is set. For example, if an event
is defined as::

    import threading as tg
    ...
    event = tg.Event()

and the task registration is::

    sch.task(event,True,sch.aligned())

where *sch* is the current instance of *RunTask* and *True* tells to *RunTask*
to set the event flag when the runtime comes.
As timing generator is choosen 'aligned'.
Then in the same thread or in any other thread as it is needed, the program
execution can wait for the event flag to be set with the following statement::

    event.wait()


Lock
====

If the task is a Lock synchronization primitive from the threading module,
when its runtime comes, *Runtask* acquires or releases the Lock according
to the second argument given at the task registration. If it is false, the
lock is released. If it is true, the lock is acquired. For example, if a lock
is defined as::

    import threading as tg
    ...
    lock = tg.Lock()
    lock.acquire()

and the task registration is::

    sch.task(lock,False,sch.aligned())

where *sch* is the current instance of *RunTask* and *False* tells to *RunTask*
to release the lock when the runtime comes.
As timing generator is choosen 'aligned'.
Then in the same thread or in any other thread as it is needed, the program
execution can wait for the lock to be released with the following statement::

    lock.acquire()


Semaphore
=========

If the task is a Semaphore synchronization primitive from the threading module,
when its runtime comes, *Runtask* acquires or releases the Semaphore according
to the second argument given at the task registration. If it is false, the
semaphore is released. If it is true, the semaphore is acquired. For example,
if a semaphore is defined as::

    import threading as tg
    ...
    semaphore = tg.Semaphore()
    semaphore.acquire()

and the task registration is::

    sch.task(semaphore,False,sch.aligned())

where *sch* is the current instance of *RunTask* and *False* tells to *RunTask*
to release the semaphore when the runtime comes.
As timing generator is choosen 'aligned'.
Then in the same thread or in any other thread as it is needed, the program
execution can wait for the lock to be released with the following statement::

    semaphore.acquire()


