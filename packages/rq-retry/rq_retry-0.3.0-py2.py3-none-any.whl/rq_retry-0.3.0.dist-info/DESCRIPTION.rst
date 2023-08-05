
|Build Status| |Coverage Status| |Downloads|

RQ Retry
========

`RQ Retry`_ is a package that adds retry functionality to the `RQ`_
queueing system. It can retry failed jobs immediately or optionally
schedule them to retry after a delay using `RQ Scheduler`_.

Installation
============

.. code::

    pip install rq-retry
    pip install rq-scheduler # optional

Usage
=====

Run worker process:

.. code::

    rqworker -w rq_retry.RetryWorker
    rqscheduler # optional

`See Documentation for details`_

.. _See Documentation for details: https://github.com/mgk/rq-retry/blob/master/README.md
.. _RQ Retry: https://github.com/mgk/rq-retry/blob/master/README.md
.. _RQ: http://python-rq.org/
.. _RQ Scheduler: https://github.com/ui/rq-scheduler

.. |Build Status| image:: https://travis-ci.org/mgk/rq-retry.svg?branch=master
   :target: https://travis-ci.org/mgk/rq-retry
.. |Coverage Status| image:: https://coveralls.io/repos/mgk/rq-retry/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/mgk/rq-retry?branch=master
.. |Downloads| image:: https://img.shields.io/pypi/dm/rq-retry.svg
   :target: https://pypi.python.org/pypi/rq-retry


