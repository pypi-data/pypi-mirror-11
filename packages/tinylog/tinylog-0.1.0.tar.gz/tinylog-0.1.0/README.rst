tinylog
=======

Just a tiny logger. Nothing more, nothing less.

Installation
------------

Through PyPI::

    $ pip install tinylog

...or from the project root directory::

    $ python setup.py install

Usage
-----

Example usage::

    # Basic usage, with console logging
    
    >> from tinylog import Logger
    >> log = Logger(console='stdout', info='~/test.log')
    >> log.debug('Foo!')
    2015-09-09T23:40:42.817421 [DEBUG] Foo!
    >>log.info('Bar!')
    2015-09-09T23:40:48.865398 [INFO] Bar!
    >> log.critical('Situation critical!')
    2015-09-09T23:40:58.369778 [CRITICAL] Situation critical!
    >> exit()

    $ cat ~/test.log 
    2015-09-09T23:40:48.865398 [INFO] Bar!
    2015-09-09T23:40:58.369778 [CRITICAL] Situation critical!

    # With separated debug and error logs, and custom format
    
    >> from tinylog import Logger
    >> log = Logger(debug='~/debug.log', error='~/error.log', fmt='{unixtimestamp}:{level}:{message}\n')
    >> log.debug('Debug message')
    >> log.info('Info message')
    >> log.warning('Warning message')
    >> log.error('Error message!')
    >> log.critical('Critical error!')
    >> exit()

    $ cat ~/debug.log 
    1441867497:DEBUG:Debug message
    1441867501:INFO:Info message
    1441867506:WARNING:Warning message
    1441867512:ERROR:Error message!
    1441867531:CRITICAL:Critical error!

    $ cat ~/error.log 
    1441867512:ERROR:Error message!
    1441867531:CRITICAL:Critical error!

To disable logging, set the environment variable "PRODUCTION", or use a variable
you pick by instanciating Logger with it, like deactivation_var="PRODUCTION"::

    $ cat my_program.py
    from tinylog import Logger
    log = Logger(deactivation_var='FOOBAR', console='stdout')
    log.info('foo')

    $ python my_program.py
    2015-09-09T23:57:50.008624 [INFO] foo

    $ FOOBAR=1 python my_program.py
    <empty>

Release Notes
-------------

:0.0.1:
    Project created
