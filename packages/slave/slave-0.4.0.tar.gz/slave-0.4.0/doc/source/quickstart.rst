.. _quickstart:

Quickstart
==========

Using slave is easy. The following example shows how device drivers are used.
We are going to implement a short measurement script, which initializes a
Stanford Research SR830 lock-in amplifier and performs a measurement.

The first step is to initialize a transport to the lock-in amplifier. Here we
are using `pyvisa`_ to establish a :abbr:`GPIB (General Purpose Interface Bus)`
transport with the device at primary address 8.

::

    from slave.transport import visa
    transport = visa('GPIB::08')

Slave does not communicate directly with the device. It uses an object referred
to as :class:`~.Transport` object for the low level communication (see
:ref:`transport_layer` for a detailed explanation).

In the next step, we construct a :class:`~.slave.sr830.SR830` instance and
inject the `pyvisa`_ transport.

::

    from slave.srs import SR830

    lockin = SR830(transport)

This creates a fully functional, high level interface to the lock-in amplifier.
Before we start the actual measurement, we're going to configure the lock-in.

::

    lockin.frequency = 22.08  # Set the internal frequency generator to 22.08 Hz
    lockin.amplitude = 5.0    # Use an amplitude of 5 V
    lockin.reserve = 'high'

And finally measure 60 times, waiting one second between each measurement, and
print the result.

::

    import time

    for i in range(60):
        print lockin.x
        time.sleep(1)

Putting it all together, we get a small 13 line script, capable of performing a
complete measurement.

.. literalinclude:: ../../examples/quickstart.py

.. _pyvisa: http://pyvisa.sourceforge.net/
