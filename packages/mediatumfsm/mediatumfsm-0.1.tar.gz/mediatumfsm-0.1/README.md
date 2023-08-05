mediaTUM FSM Library
====================

Declarative finite state machine library inspired by [akka FSM](http://doc.akka.io/docs/akka/snapshot/scala/fsm.html)
and [erlang gen_fsm](http://www.erlang.org/doc/design_principles/fsm.html).
This library works with Python 2.7 and Python 3.2+


Installation
------------

With `pip` from source:

    pip install git+git://mediatumdev.ub.tum.de/mediatum-fsm

This installs the `mediatumfsm` package and its dependency `pydot2`, if not already installed.

Running Tests
-------------

From the base directory, for example:

    py.test