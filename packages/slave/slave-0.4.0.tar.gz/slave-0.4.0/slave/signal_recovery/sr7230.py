#  -*- coding: utf-8 -*-
#
# Slave, (c) 2014, see AUTHORS.  Licensed under the GNU GPL.
"""Implements the signal recovery sr7230 driver.


The following example shows how to use the fast curve buffer to acquire data.
::

    import time
    from slave.transport import Socket
    from slave.signal_recovery import SR7230

    lockin = SR7230(Socket(address=('192.168.178.1', 50000)))

    lockin.fast_buffer.enabled = True       # Use fast curve buffer.
    lockin.fast_buffer.storage_interval = 8 # Take date every 8 us.
    lockin.fast_buffer.length = 100000      # Store the max number of points
    lockin.take_data()                      # Start data acquisition immediately.

    while lockin.acquisition_status[0] == 'on':
        time.sleep(0.1)

    x, y = lockin.fast_buffer['x'], lockin.fast_buffer['y']

The fast buffer can store just a limited amount of variables. The standard
buffer is a lot more flexible. The following examples shows how to use it to
store the sensitivity, x and y values.

::

    lockin.standard_buffer.enabled = True
    lockin.standard_buffer.definition = 'X', 'Y', 'sensitivity'
    lockin.standard_buffer.storage_interval = 1000
    lockin.standard_buffer.length = 1000
    lockin.take_data()

    while lockin.acquisition_status[0] == 'on':
        time.sleep(0.1)

    # Note: The x and y values are not stored in absolute units. They are in
    # relative units compared to the chosen senitivity.
    sensitivity = sr7230.standard_buffer['sensitivity']
    x = sr7230.standard_buffer['x']
    y = sr7230.standard_buffer['y']

"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import *
import datetime

import numpy as np

from slave.driver import Command, Driver, CommandSequence
from slave.protocol import SignalRecovery
from slave.types import (
    Boolean, Enum, Float, Integer, Register, Set, String, Mapping
)


class SR7230(Driver):
    """Represents a Signal Recovery SR7230 lock-in amplifier.

    :param transport: A transport object.
    :param option: Specifies if an optional card is installed. Valid are `None`
        or '250kHz'. This changes some frequency related limits.

    .. rubric:: Signal Channel

    :ivar current_mode: The current mode, either 'off', 'high bandwidth' or
        'low noise'.
    :ivar voltage_mode: The voltage mode, either 'test', 'A' , '-B' or 'A-B'.
        The 'test' mode corresponds to both inputs grounded.

        .. note:

            The :attr:`~.current_mode` has a higher precedence.
    :ivar demodulator_source: It sets the source of the signal for the second
        stage demodulators in dual reference mode. Valid are 'main', 'adc1'
        and 'tandem'.

        ======== =======================================================
        value    description
        ======== =======================================================
        'main'   The main signal channel adc is used.
        'adc1'   The rear pannel auxiliary input adc1 is used as source.
        'tandem' The demodulator 1 X-channel output is used as source.
        ======== =======================================================

    :ivar fet: The voltage mode input device control. Valid entries are
        'bipolar' and 'fet', where

        * 'bipolar' is a bipolar device with 10kOhm input impedance. It allows
          for the lowest possible voltage noise.

          .. note:: It is not possible to use bipolar and ac coupling together.

        * 'fet' 10MOhm input impedance. It is the default setting.

    :ivar shield: The input connector shield grounding mode. Valid entries
        are 'ground' and 'float'.
    :ivar coupling: The input connector coupling, either 'ac' or 'dc'.
    :ivar sensitivity: The full-scale sensitivity. The valid entries depend on
        the current mode.

        =========  ================  ===========
        'off'      'high bandwidth'  'low noise'
        =========  ================  ===========
        '10 nV'    '10 fA'           ---
        '20 nV'    '20 fA'           ---
        '50 nV'    '50 fA'           ---
        '100 nV'   '100 fA'          ---
        '200 nV'   '200 fA'          '2 fA'
        '500 nV'   '500 fA'          '5 fA'
        '1 uV'     '1 pA'            '10 fA'
        '2 uV'     '2 pA'            '20 fA'
        '5 uV'     '5 pA'            '50 fA'
        '10 uV'    '10 pA'           '100 fA'
        '20 uV'    '20 pA'           '200 fA'
        '50 uV'    '50 pA'           '500 fA'
        '100 uV'   '100 pA'          '1 pA'
        '200 uV'   '200 pA'           2 pA'
        '500 uV'   '500 pA'          '5 pA'
        '1 mV'     '1 nA'            '10 pA'
        '2 mV'     '2 nA'            '20 pA'
        '5 mV'     '5 nA'            '50 pA'
        '10 mV'    '10 nA'           '100 pA'
        '20 mV'    '20 nA'           '200 pA'
        '50 mV'    '50 nA'           '500 pA'
        '100 mV'   '100 nA'          '1 nA'
        '200 mV'   '200 nA'          '2 nA'
        '500 mV'   '500 nA'          '5 nA'
        '1 V'      '1 uA'            '10 nA'
        =========  ================  ===========

    :ivar ac_gain: The gain of the signal channel amplifier. See :attr:`SR7230.AC_GAIN`
        for valid values.
    :ivar ac_gain_auto: A boolean corresponding to the ac gain automatic mode.
        It is `False` if the ac_gain is under manual control, and `True`
        otherwise.
    :ivar line_filter: The line filter configuration.
        *(<filter>, <frequency>)*, where

        * *<filter>* Is the filter mode. Valid entries are `'off'`, `'notch'`,
          `'double'` or `'both'`.
        * *<frequency>* Is the notch filter center frequency, either `'60Hz'`
          or `'50Hz'`.

    .. rubric:: Reference channel

    :ivar reference_mode: The instruments reference mode. Valid are 'single',
        'dual harmonic' and 'dual reference'.
    :ivar reference: The reference input mode, either 'internal', 'ttl' or
        'analog'.
    :ivar internal_reference_channel: In dual reference mode, selects the
        reference channel, which is operated in internal reference mode. Valid
        are 'ch1' or 'ch2'.
    :ivar harmonic: The reference harmonic mode, an integer between 1 and 128
        corresponding to the first to 127 harmonics.
    :ivar trigger_output: Set's the rear pannel trigger output.

        =========== ========================================================
        Value       Description
        =========== ========================================================
        'curve'     A trigger signal is generated by curve buffer triggering
        'reference' A ttl signal at the reference frequency
        =========== ========================================================

    :ivar reference_phase: The phase of the reference signal, a float ranging
        from -360 to 360 corresponding to the angle in degrees with a resolution
        of mili degree.

    :ivar reference_frequency: A float corresponding to the reference frequency
        in Hz. (read only)

        .. note::

            If :attr:`.reference` is not `'internal'` the reference frequency
            value is zero if the reference channel is unlocked.

    :ivar virtual_reference: A boolean enabling/disabling the virtual reference
        mode.

        .. note:

            The :meth:`~.SR7230.seek` method should be used before enabling virtual reference mode.

    .. rubric:: Signal Channel Output Filters

    :ivar noise_measurement: A boolean representing the noise measurement mode.
    :ivar noise_buffer_length: The length of the noise buffer in seconds. Valid
        are 'off', '1 s', '2 s', '3 s' and '4 s'.
    :ivar time_constant: The filter time constant. See :attr:`.TIME_CONSTANT`
        for valid values.

        .. note::

            If :attr:`.noise_measurement` is enabled, only '500 us', '1 ms',
            '2 ms', '5 ms' and '10 ms' are valid.

    :ivar sync: A boolean value, representing the state of the synchronous time
        constant mode.
    :ivar slope: The output lowpass filter slope in dB/octave, either '6 dB',
        '12 dB', '18 dB' or '24 dB'.

        .. note::

            If :attr:¸.noise_measurement` or :attr:`.fastmode` is enabled, only
            '6 dB' and '12 dB' are valid.

    .. rubric:: Signal Channel Output Amplifiers

    :ivar x_offset: The x-channel output offset control.
        *(<enabled>, <range>)*, where

        * *<enabled>* A boolean enabling/disabling the output offset.
        * *<range>* The range of the offset, an integer between -30000 and
          30000 corresponding to +/- 300%.

    :ivar y_offset: The y-channel output offset control.
        *(<enabled>, <range>)*, where

        * *<enabled>* A boolean enabling/disabling the output offset.
        * *<range>* The range of the offset, an integer between -30000 and
          30000 corresponding to +/- 300%.

    :ivar expand: The expansion control, either 'off', 'x', 'y' or 'both'.
    :ivar fastmode: Enables/disables the fastmode of the output filter. In
        normal mode (`False`), the instruments analog outputs are derived from
        the output processor. The update rate is 1 kHz.

        In fastmode, the analog outputs are derived directly from the core FPGA
        running the demodulator algorithms. This increases the update rate to
        1 Mhz for time constants 10 us to 500 ms. It remains at 1 kHz for
        longer time constants.

    .. rubric:: Instrument outputs

    :ivar x: A float representing the X-channel output in either volt or
        ampere. (read only)
    :ivar y: A float representing the Y-channel output in either volt or
        ampere. (read only)
    :ivar xy: X and Y-channel output with the following format *(<x>, <y>)*.
        (read only)
    :ivar r: The signal magnitude, as float. (read only)
    :ivar theta: The signal phase, as float. (read only)
    :ivar r_theta: The magnitude and the signal phase. *(<r>, <theta>)*.
        (read only)
    :ivar ratio: The ratio equivalent to X/ADC1. (read only)
    :ivar log_ratio: The ratio equivalent to log(X/ADC1). (read only)
    :ivar noise: The square root of the noise spectral density measured at the
        Y channel output. (read only)
    :ivar noise_bandwidth: The noise bandwidth. (read only)
    :ivar noise_output: The noise output, the mean absolute value of the Y
        channel. (read only)
    :ivar equation: The equation configuration, a list of two
        :class:`~.Equation` instances.

    .. rubric:: Internal oscillator

    :ivar amplitude: A float between 0. and 5. representing the oscillator
        amplitude in V rms.
    :ivar amplitude_start: Amplitude sweep start value.
    :ivar amplitude_stop: Amplitude sweep end value.
    :ivar amplitude_step: Amplitude sweep amplitude step.
    :ivar frequency: The oscillator frequency in Hz. Valid entries are 0. to
        1.2e5 and a resolution of 1e-3 Hz.
    :ivar frequency_start: The frequency sweep start value.
    :ivar frequency_stop: The frequency sweep stop value.
    :ivar frequency_step: The frequency sweep step size and sweep type.
        *(<step>, <mode>)*, where

        * *<step>* The step size in Hz.
        * *<mode>* The sweep mode, either 'log', 'linear' or 'seek'. In 'seek'
          mode the sweep stops automatically when the signal magnitude exceeds
          50% of full scale. It's most commonly used to set up virtual reference
          mode.

    :ivar sweep_rate: The frequency and amplitude sweep step rate in time per
        step in seconds. Valid entries are 0.001 to 1000. with a resolution of
        0.001.
    :ivar modulation: The state of the oscillator amplitude/frequency
        modulation. Valid are `False`, 'amplitude' and 'frequency'.
    :ivar amplitude_modulation: The amplitude modulation commands, an instance
        of :class:`~.AmplitudeModulation`.
    :ivar frequency_modulation: The frequency modulation commands, an instance
        of :class:`~.FrequencyModulation`.

    .. rubric:: Analog Outputs

    :ivar dac: A sequence of four :class:`~.DAC` instances, representing all
        four analog outpus.

    .. rubric:: Digital I/O

    :ivar digital_ports: The digital port configuration, an instance of
        :class:`~.DigitalPort`.

    .. rubric:: Auxiliary Inputs

    :ivar aux: A :class:`~.CommandSequence` instance, providing access to all
        four analog to digital input channel voltage readings. E.g.::

            # prints voltage reading of first aux input channel.
            print(sr7230.aux[0])

    :ivar aux_trigger_mode: The trigger modes of the auxiliary input channels.
        Valid are 'internal', 'external', 'burst' and 'fast burst'

        ============ ===========================================================
        mode         description
        ============ ===========================================================
        'internal'   The internal
        'external'   The ADC TRIG IN connector is used to trigger readings.
        'burst'      Allows sampling rates of 40 kHz, but only ADC1 and ADC2 can
                     be used.
        'fast burst' Sampling rates up to 200 kHz are possible, but only ADC1
                     can be used.
        ============ ===========================================================

    .. rubric:: Output Data Curve Buffer

    :ivar acquisition_status: The state of the curve acquisition. A tuple
        corresponding to *(<state>, <sweeps>, <status byte>, <points>)*, where

        * *<state>* is the curve acquisition state. Possible values are

          =========================== =================================================
          Value                       Description
          =========================== =================================================
          'off'                       No curve acquisition in progress.
          'on'                        Curve acquisition via :meth:`SR7230.take_data` in
                                      progress.
          'continuous'                Curve acquisition via
                                      :meth:`~.Sr7230.take_data_continuously` in
                                      progress.
          'halted'                    Curve acquisition via :meth:`SR7230.take_data`
                                      in progress but halted.
          'continuous halted'         Curve acquisition via
                                      :meth:`~.Sr7230.take_data_continuously` in
                                      progress but halted.
          'fast acquisition complete' Set when the fast curve acquisition is complete
                                      and the data is ready to be transfered into the
                                      Lock-In's internal memory.
          =========================== =================================================

        * *<sweeps>* the number of sweeps acquired.
        * *<status byte>* the status byte, see :attr:`SR7230.status_byte`.
        * *<points>* The number of points acquired.

    :ivar fast_buffer: An instance of :class:`~.FastBuffer`, representing the
        fast curve buffer related commands.
    :ivar standard_buffer: An instance of :class:`~.FastBuffer`, representing
        the fast curve buffer related commands.
    :ivar trigger_output_event: Defines when a trigger output is generated,
        while buffer acquisition is running and `SR7230.trigger_output` is set
        to 'curve'.

        ======= ======================================
        Value   Description
        ======= ======================================
        'curve' A trigger is generated once per curve.
        'point' A trigger is generated once per point.
        ======= ======================================

    :ivar trigger_output_polarity: The polarity of the trigger output.
        Valid are 'rising', 'falling'.

    .. rubric:: Computer Interfaces

    :ivar baudrate: The baudrate of the rs232 interface. See
        :attr:`~.SR7230.BAUDRATE` for valid values.
    :ivar delimiter: The data delimiter. See :attr:`~.SR7230.DELIMITER` for
        valid values.

        .. note::

            In normal operation, there is no need to change the delimiter
            because the communication is handled by the protocol. If the
            delimiter is changed, the `msg_data_sep` and `resp_data_sep` values
            of the protocol must be changed manually.

    :ivar status: The status byte. (read only)
    :ivar overload_status: The overload status. (read only)
    :ivar ip_address: Four integer values representing the ip address. E.g.
        169.254.0.10 would translate to a tuple (169, 254, 0, 10)

        .. note::

            Setting the IP address sets the gateway and subnet mask to a default
            value. If non default values are required set them afterwards.

    :ivar subnet_mask: A tuple of four ints representing the subnet mask.
    :ivar gateway_address: A tuple of four ints representing the gateway address.


    .. rubric:: Instrument Identification

    :ivar identification: The model number `7230`. (read only)
    :ivar version: The firmware version. (read only)
    :ivar date: The last calibration date. (read only)
    :ivar name: The name of the lock-in amplifier, a string with up 64 chars.

    .. rubric:: Dual Mode

    In dual reference mode, two demodulator stages are used instead of one. The
    standard commands such as `x`, `y` or `sensitivity` won't work. To access
    the parameters of the two stages use the :attr:`~.SR7230.demod`
    attribute instead. E.g.::

        # Set lockin into dual reference mode.
        sr7230.reference_mode = 'dual'
        # get x value of first demod stage (zero index based).
        x = sr7230.demod[0].x
        # set the sensitivity of the second demod stage.
        sr7230.demod[1].sensitivity = '50 nV'

    :ivar demod: A tuple of two :class:`~.Demodulator` instances. The first with
        index 0 represents the first demodulator, the second item with index 1
        represents the second demodulator.

    """
    BAUDRATE = [
        75, 110, 134.5, 150, 300, 600, 1200, 1800,
        2000, 2400, 4800, 9600, 19200, 38400
    ]
    DELIMITER = [chr(13),] + [chr(i) for i in range(32, 126)]
    SENSITIVITY_VOLTAGE = [
        '10 nV', '20 nV', '50 nV', '100 nV', '200 nV', '500 nV', '1 uV',
        '2 uV', '5 uV', '10 uV', '20 uV', '50 uV', '100 uV', '200 uV',
        '500 uV', '1 mV', '2 mV', '5 mV', '10 mV', '20 mV', '50 mV', '100 mV',
        '200 mV', '500 mV', '1 V'
    ]
    SENSITIVITY_CURRENT_HIGHBW = [
        '10 fA', '20 fA', '50 fA', '100 fA', '200 fA', '500 fA', '1 pA',
        '2 pA', '5 pA', '10 pA', '20 pA', '50 pA', '100 pA', '200 pA',
        '500 pA', '1 nA', '2 nA', '5 nA', '10 nA', '20 nA', '50 nA', '100 nA',
        '200 nA', '500 nA', '1 uA'
    ]
    SENSITIVITY_CURRENT_LOWNOISE = [
        '2 fA', '5 fA', '10 fA', '20 fA', '50 fA', '100 fA', '200 fA',
        '500 fA', '1 pA', '2 pA', '5 pA', '10 pA', '20 pA', '50 pA', '100 pA',
        '200 pA', '500 pA', '1 nA', '2 nA', '5 nA', '10 nA'
    ]

    @property
    def SENSITIVITY(self):
        imode = self.current_mode
        if imode == 'off':
            return self.SENSITIVITY_VOLTAGE
        elif imode == 'high bandwidth':
            return self.SENSITIVITY_CURRENT_HIGHBW
        else:
            return self.SENSITIVITY_CURRENT_LOWNOISE

    AC_GAIN = [
        '0 dB', '6 dB', '12 dB', '18 dB', '24 dB', '30 dB', '36 dB', '42 dB',
        '48 dB', '54 dB', '60 dB', '66 dB', '72 dB', '78 dB', '84 dB', '90 dB'
    ]
    TIME_CONSTANT = [
        '10 us', '20 us', '50 us', '100 us', '200 us', '500 us', '1 ms', '2 ms',
        '5 ms', '10 ms', '20 ms', '50 ms', '100 ms', '200 ms', '500 ms', '1 s',
        '2 s', '5 s', '10 s', '20 s', '50 s', '100 s', '200 s', '500 s', '1 ks',
        '2 ks', '5 ks', '10 ks', '20 ks', '50 ks', '100 ks'
    ]
    STATUS_BYTE = {
        0: 'command complete',
        1: 'invalid command',
        2: 'command parameter error',
        3: 'reference unlock',
        4: 'output overload',
        5: 'new adc',
        6: 'input overload',
        7: 'data available',
    }
    OVERLOAD_BYTE = {
        0: 'x1',
        1: 'y1',
        2: 'x2',
        3: 'y2',
        4: 'adc1',
        5: 'adc2',
        6: 'adc3',
        7: 'adc4',
    }
    ACQUISITION_STATUS = {
        'off': '0',
        'on': '1',
        'continuous': '2',
        'halted': '3',
        'continuous halted': '4',
        'fast acquisition complete': '16'
    }

    def __init__(self, transport, option=None):
        protocol = SignalRecovery()
        super(SR7230, self).__init__(transport, protocol)
        self.option = option
        # Signal Channel
        # ==============
        self.current_mode = Command(
            'IMODE',
            'IMODE',
            Enum('off', 'high bandwidth', 'low noise')
        )
        self.voltage_mode = Command(
            'VMODE',
            'VMODE',
            Enum('test', 'A', '-B', 'A-B')
        )
        self.demodulator_source = Command(
            'DEMOD2SRC',
            'DEMOD2SRC',
            Enum('main', 'adc1', 'tandem')
        )
        self.fet = Command('FET', 'FET', Enum('bipolar', 'fet'))
        self.shield = Command('FLOAT', 'FLOAT', Enum('ground', 'float'))
        self.coupling = Command('DCCOUPLE', 'DCCOUPLE', Enum('ac', 'dc'))
        self._voltage_sensitivity = Command(
            'SEN',
            'SEN',
            Enum(*SR7230.SENSITIVITY_VOLTAGE, start=3)
        )
        self._highbandwidth_sensitivity = Command(
            'SEN',
            'SEN',
            Enum(*SR7230.SENSITIVITY_CURRENT_HIGHBW, start=3)
        )
        self._lownoise_sensitivity = Command(
            'SEN',
            'SEN',
            Enum(*SR7230.SENSITIVITY_CURRENT_LOWNOISE, start=7)
        )
        self.ac_gain = Command(
            'ACGAIN',
            'ACGAIN',
            Enum(*SR7230.AC_GAIN)
        )
        self.auto_ac_gain = Command('AUTOMATIC', 'AUTOMATIC', Boolean)
        self.line_filter = Command(
            'LF',
            'LF',
            [Enum('off', 'notch', 'double', 'both'), Enum('60Hz', '50Hz')]
        )
        # Reference Channel
        # =================
        self.reference_mode = Command(
            'REFMODE',
            'REFMODE',
            Enum('single', 'dual harmonic', 'dual reference')
        )
        self.internal_reference_channel = Command(
            'INT',
            'INT',
            Enum('ch1', 'ch2', start=1)
        )
        self.harmonic = Command('REFN', 'REFN', Integer(min=1, max=128))
        self.trigger_output = Command(
            'REFMON',
            'REFMON',
            Enum('curve', 'reference')
        )
        self.reference_phase = Command(
            'REFP.',
            'REFP.',
            Float(min=-360., max=360., fmt='{:.3f}')
        )
        self.reference_frequency = Command(('FRQ.', Float))
        self.virtual_reference = Command(
            'VRLOCK',
            'VRLOCK',
            Boolean
        )
        # Signal Channel Output Filters
        # =============================
        self.noise_measurement = Command(
            'NOISEMODE',
            'NOISEMODE',
            Boolean
        )
        self.noise_buffer_length = Command(
            'NNBUF',
            'NNBUF',
            Enum('off', '1s', '2s', '3s', '4s')
        )
        self.time_constant = Command('TC', 'TC', Enum(*SR7230.TIME_CONSTANT))
        self.sync = Command('SYNC', 'SYNC', Boolean)
        self.slope = Command(
            'SLOPE',
            'SLOPE',
            Enum('6 dB', '12 dB', '18 dB', '24 dB')
        )

        # Signal Channel Output Amplifiers
        # ================================
        self.x_offset = Command(
            'XOF',
            'XOF',
            [Boolean, Integer(min=-30000, max=30000)]
        )
        self.y_offset = Command(
            'YOF',
            'YOF',
            [Boolean, Integer(min=-30000, max=30000)]
        )
        self.expand = Command(
            'EX',
            'EX',
            Enum('off', 'x', 'y', 'both')
        )
        self.fastmode = Command('FASTMODE', 'FASTMODE', Boolean)

        # Intrument Outputs
        # =================
        self.x = Command(('X.', Float))
        self.y = Command(('Y.', Float))
        self.xy = Command(('XY.', [Float, Float]))
        self.r = Command(('MAG.', Float))
        self.theta = Command(('PHA.', Float))
        self.r_theta = Command(('MP.', [Float, Float]))
        self.ratio = Command(('RT.', Float))
        self.log_ratio = Command(('LR.', Float))
        self.noise = Command(('NHZ.', Float))
        self.noise_bandwidth = Command(('ENBW.', Float))
        self.noise_output = Command(('NN.', Float))
        self.equation = [
            Equation(self._transport, self._protocol, 1),
            Equation(self._transport, self._protocol, 2),
        ]

        # Internal oscillator
        # ===================
        self.amplitude = Command('OA.', 'OA.', Float(min=0., max=5.))
        self.amplitude_start = Command(
            'ASTART.',
            'ASTART.',
            Float(min=0., max=5.)
        )
        self.amplitude_stop = Command(
            'ASTOP.',
            'ASTOP.',
           Float(min=0., max=5.)
        )
        self.amplitude_step = Command(
            'ASTEP.',
            'ASTEP.',
            Float(min=0., max=5.)
        )
        fmax = 250e3 if self.option is '250kHz' else 120e3
        self.frequency = Command('OF.', 'OF.', Float(min=0, max=fmax, fmt='{:.3f}'))
        self.frequency_start = Command(
            'FSTART.',
            'FSTART.',
            Float(min=0, max=fmax, fmt='{:.3f}')
        )
        self.frequency_stop = Command(
            'FSTOP.',
            'FSTOP.',
            Float(min=0, max=fmax, fmt='{:.3f}')
        )
        self.frequency_step = Command(
            'FSTEP.',
            'FSTEP.',
            [Float(min=0, max=fmax), Enum('log', 'linear', 'seek')]
        )
        self.sweep_rate = Command(
            'SRATE.',
            'SRATE.',
            Float(min=1e-3, max=1e3)
        )
        self.modulation = Command(
            'MENABLE',
            'MENABLE',
            Enum(False, 'amplitude', 'frequency')
        )
        self.amplitude_modulation = AmplitudeModulation(
            self._transport,
            self._protocol
        )
        self.frequency_modulation = FrequencyModulation(
            self._transport,
            self._protocol
        )
        # Analog Outputs
        # ==============
        self.dac = [DAC(self._transport, self._protocol, i) for i in range(1, 5)]

        # Digital I/O
        # ===========
        self.digital_ports = DigitalPort(self._transport, self._protocol)

        # Auxiliary Inputs
        # ================
        self.aux = CommandSequence(
            self._transport,
            self._protocol,
            [Command(('ADC. {}'.format(i), Float)) for i in range(1, 5)]
        )
        self.aux_trigger_mode = Command(
            'TADC',
            'TADC',
            Enum('internal', 'external', 'fast burst', 'burst')
        )
        # Output Data Curve Buffer
        # ========================
        self.acquisition_status = Command((
            'M',
            [
                Mapping(self.ACQUISITION_STATUS),
                Integer,
                Register(SR7230.STATUS_BYTE),
                Integer
            ]
        ))
        self.fast_buffer = FastBuffer(self._transport, self._protocol)
        self.standard_buffer = StandardBuffer(self._transport, self._protocol)
        self.trigger_output_event = Command(
            'TRIGOUT',
            'TRIGOUT',
            Enum('curve', 'point')
        )
        self.trigger_output_polarity = Command(
            'TRIGOUTPOL',
            'TRIGOUTPOL',
            Enum('rising', 'falling')
        )

        # Computer Interfaces
        # ===================
        self.baud_rate = Command('RS', 'RS', Enum(*SR7230.BAUDRATE))
        self.delimiter = Command(
            'DD',
            'DD',
            Mapping({ord(i): i for i in SR7230.DELIMITER})
        )
        self.status = Command(('ST', Register(SR7230.STATUS_BYTE)))
        self.overload_status = Command(('N', Register(SR7230.OVERLOAD_BYTE)))
        self.ip_address = Command('IPADDR', 'IPADDR', [Integer(0, 256),]*4)
        self.subnet_mask = Command('SNMASK', 'SNMASK', [Integer(0, 256),]*4)
        self.gateway_address = Command('GWADDR', 'GWADDR', [Integer(0, 256),]*4)

        # Instrument Identification
        # =========================
        self.identification = Command(('ID', String))
        self.version = Command(('VER', String))
        self.name = Command('NAME', 'NAME', String(max=64))

        # Dual Mode Command
        # =================
        self.demod = (
            Demodulator(self._transport, self._protocol, 1),
            Demodulator(self._transport, self._protocol, 2),
        )

    @property
    def sensitivity(self):
        imode = self.current_mode
        if imode == 'off':
            return self._voltage_sensitivity
        elif imode == 'high bandwidth':
            return self._highbandwidth_sensitivity
        else:
            return self._lownoise_sensitivity

    @sensitivity.setter
    def sensitivity(self, value):
        imode = self.current_mode
        if imode == 'off':
            self._voltage_sensitivity = value
        elif imode == 'high bandwidth':
            self._highbandwidth_sensitivity = value
        else:
            self._lownoise_sensitivity = value

    @property
    def date(self):
        d = self._query(('DATE', String))
        return datetime.datetime(day=int(d[:2]), month=int(d[2:4]), year=int(d[4:]))

    def auto_sensitivity(self):
        """Triggers the auto sensitivity mode.

        When the auto sensitivity mode is triggered, the SR7225 adjustes the
        sensitivity so that the signal magnitude lies in between 30% and 90%
        of the full scale sensitivity.
        """
        self._write('AS')

    def auto_measure(self):
        """Triggers the auto measure mode."""
        self._write('ASM')

    def auto_phase(self):
        """Triggers the auto phase mode."""
        self._write('AQN')

    def auto_offset(self):
        """Triggers the auto offset mode."""
        self._write('AXO')

    def clear_buffer(self):
        """Initialises the curve buffer and related status variables."""
        self._write('NC')

    def start_asweep(self, start=None, stop=None, step=None):
        """Starts a amplitude sweep.

        :param start: Sets the start frequency.
        :param stop: Sets the target frequency.
        :param step: Sets the frequency step.

        """
        if start:
            self.amplitude_start = start
        if stop:
            self.amplitude_stop = stop
        if step:
            self.amplitude_step = step
        self._write(('SWEEP', Integer), 2)

    def start_afsweep(self):
        """Starts a frequency and amplitude sweep."""
        self._write(('SWEEP', Integer), 3)

    def start_fsweep(self, start=None, stop=None, step=None):
        """Starts a frequency sweep.

        :param start: Sets the start frequency.
        :param stop: Sets the target frequency.
        :param step: Sets the frequency step.

        """
        if start:
            self.frequency_start = start
        if stop:
            self.frequency_stop = stop
        if step:
            self.frequency_step = step
        self._write(('SWEEP', Integer), 1)

    def stop(self):
        """Stops the current sweep."""
        self._write(('SWEEP', Integer), 0)

    def pause_asweep(self):
        """Pauses amplitude sweep."""
        self._write(('SWEEP', Integer), 6)

    def pause_fsweep(self):
        """Pauses frequency sweep."""
        self._write(('SWEEP', Integer), 5)

    def pause_afsweep(self):
        """Pauses dual frequency/amplitude sweep."""
        self._write(('SWEEP', Integer), 7)

    def link_asweep(self):
        """Links amplitude sweep to curve buffer acquisition."""
        self._write(('SWEEP', Integer), 10)

    def link_fsweep(self):
        """Links frequency sweep to curve buffer acquisition."""
        self._write(('SWEEP', Integer), 9)

    def link_afsweep(self):
        """Links dual amplitude/frequency sweep to curve buffer acquisition."""
        self._write(('SWEEP', Integer), 11)

    def take_data(self):
        """Starts data acquisition."""
        self._write('TD')

    def take_data_triggered(self, trigger, edge, stop):
        """Configures data acquisition to start on various trigger conditions.

        :param trigger: The trigger condition, either 'curve' or 'point'.

            ======= =======================================================
            Value   Description
            ======= =======================================================
            'curve' Each trigger signal starts a curve acquisition.
            'point' A point is stored for each trigger signal. The max
                    trigger frequency in this mode is 1 kHz.
            ======= =======================================================

        :param edge: Defines wether a 'rising' or 'falling' edge is interpreted
            as a trigger signal.
        :param stop: The stop condition. Valid are 'buffer', 'halt',
            'rising' and 'falling'.

            ========= ==========================================================
            Value     Description
            ========= ==========================================================
            'buffer'  Data acquisition stops when the number of point
                      specified in :attr:`~.Buffer.length` is acquired.
            'halt'    Data acquisition stops when the halt command is issued.
            'trigger' Takes data for the period of a trigger event. If edge is
                      'rising' then teh acquisition starts on the rising edge of
                      the trigger signal and stops on the falling edge and vice
                      versa
            ========= ==========================================================

        """
        param = {
            ('curve', 'rising', 'buffer'): 0,
            ('point', 'rising', 'buffer'): 1,
            ('curve', 'falling', 'buffer'): 2,
            ('point', 'falling', 'buffer'): 3,
            ('curve', 'rising', 'halt'): 4,
            ('point', 'rising', 'halt'): 5,
            ('curve', 'falling', 'halt'): 6,
            ('point', 'falling', 'halt'): 7,
            ('curve', 'rising', 'trigger'): 8,
            ('curve', 'falling', 'trigger'): 9,
        }
        self._write(('TDT', Integer), param[(trigger, edge, stop)])

    def take_data_continuously(self, stop):
        """Starts continuous data acquisition.

        :param stop: The stop condition. Valid are 'buffer', 'halt',
            'rising' and 'falling'.

            ========= =======================================================
            Value     Description
            ========= =======================================================
            'buffer'  Data acquisition stops when the number of point
                      specified in :attr:`~.Buffer.length` is acquired.
            'halt'    Data acquisition stops when the halt command is issued.
            'rising'  Data acquisition stops on the rising edge of a trigger
                      signal.
            'falling' Data acquisition stops on the falling edge of a trigger
                      signal.
            ========= =======================================================

        .. note:: The internal buffer is used as a circular buffer.

        """
        self._write(('TDC', Enum('halt', 'rising', 'falling')), stop)

    def halt(self):
        """Halts curve acquisition in progress.

        If a sweep is linked to curve buffer acquisition it is halted as well.

        """
        self._write('HC')

    def update_correction(self):
        """Updates all frequency-dependant gain and phase correction
        parameters."""
        self._write('LOCK')

    def factory_defaults(self, full=False):
        """Resets the device to factory defaults.

        :param full: If full is `True`, all settings are returned to factory
            defaults, otherwise the communication settings are not changed.

        """
        self._write(('ADF', Boolean), not full)

    def lock_ip(self):
        """Locks the ip address.

        Only commands of the locked ip are accepted.

        """
        self._write('IPLOCK')

    def unlock_ip(self):
        """Unlocks the ip address."""
        self._write('IPUNLOCK')


class Equation(Driver):
    """The equation commands.

    An equation is defined as::

        (A +/- B) * C
        -------------
              D

    :ivar value: The value of the equation calculation. (read only)
    :ivar define: A tuple defining the equation parameter;
        *(<A>, <op>, <B>, <C>, <D>)* where

        * *<op>* is either '+' or '-'.
        * <A>, <B>, <C>, <D> is one of :attr:`~.Equation.INPUT`.

    :ivar c1: Equation constant c1, a float in the range -30. to 30.
    :ivar c2: Equation constant c2, a float in the range -30. to 30.

    """
    INPUT = [
        'x1', 'y1', 'r', 'theta', 'adc1', 'adc2', 'adc3', 'adc4', 'c1', 'c2',
        '0', '1', 'frequency', 'oscillator', 'x2', 'y2', 'r2', 'theta2'
    ]
    def __init__(self, transport, protocol, idx):
        super(Equation, self).__init__(transport, protocol)
        self.value = Command(('EQU {}'.format(idx), Float))
        self.define = Command(
            'DEFEQU {}'.format(idx),
            'DEFEQU {} '.format(idx),
            [
                Enum(*Equation.INPUT), Enum('-', '+'), Enum(*Equation.INPUT),
                Enum(*Equation.INPUT), Enum(*Equation.INPUT)
            ]
        )
        self.c1 = Command(
            'C1 {}'.format(idx),
            'C1 {} '.format(idx),
            Float(min=-30., max=30.)
        )
        self.c2 = Command(
            'C2 {}'.format(idx),
            'C2 {} '.format(idx),
            Float(min=-30., max=30.)
        )


class AmplitudeModulation(Driver):
    """Represents the amplitude modulation commands.

    :ivar float center: The amplitude modulation center voltage. A floating
        point in the range -10 to 10 in volts.
    :ivar integer depth: The amplitude modulation depth in percent in the range
        0 - 100.
    :ivar int filter: The amplitude modulation filter control. An integer
        in the range 0 - 10, where 0 is the widest bandwidth and 10 is the
        lowest.
    :ivar source: The amplitude modulation source voltage used to modulate the
        oscillator amplitude. Valid are 'adc1' and 'external'.
    :ivar float span: The amplitude modulation span voltage in volts. A float
        in the range -10 to 10.

        .. note:: The sum of center and span voltage can't exceed +/- 10V.

    """
    def __init__(self, transport, protocol):
        super(AmplitudeModulation, self).__init__(transport, protocol)
        self.center = Command(
            'AMCENTERV.',
            'AMCENTERV.',
            Float(min=-10., max=10.)
        )
        self.depth = Command('AMDEPTH', 'AMDEPTH', Integer(min=0, max=101))
        self.filter = Command('AMFILTER', 'AMFILTER', Integer(min=0, max=11))
        self.source = Command('AMSOURCE', 'AMSOURCE', Enum('adc1', 'external'))
        self.span = Command('AMVSPAN.', 'AMVSPAN.', Float(min=-10, max=10))


class FrequencyModulation(Driver):
    """Represents the frequency modulation commands.

    :ivar float center_frequency: The center frequency of the oscillator
        frequency modulation. A float in the range 0. to 120e3 (250e3 if 250
        kHz option is installed).
    :ivar float center_voltage: The center voltage of the oscillator frequency
        modulation. A float in the range -10 to 10.
    :ivar int filter: The amplitude modulation filter control. An integer
        in the range 0 - 10, where 0 is the widest bandwidth and 10 is the
        lowest.
    :ivar float span_frequency: The oscillator frequency modulation span frequency. A
        float in the range 0 up to 60e3 (125e3 if 250kHz option is installed).
    :ivar float span_voltage: The oscillator frequency modulation span voltage.
        A float in the range -10 to 10.

    .. note::

        The center frequency must be larger than the span frequency. Invalid
        values raise a `ValueError`.

    """
    def __init__(self, transport, protocol, option=None):
        super(FrequencyModulation, self).__init__(transport, protocol)
        self._fmax = 250e3 if option is '250kHz' else 120e3
        self.center_voltage = Command(
            'FMCENTERV.',
            'FMCENTERV.',
            Float(min=-10., max=10.)
        )
        self.filter = Command('FMFILTER', 'FMFILTER', Integer(min=0, max=11))
        self.span_voltage = Command(
            'FMSPANV.',
            'FMSPANV.',
            Float(min=-10., max=10.)
        )

    @property
    def center_frequency(self):
        return self._query(('FMCENTERF.', Float))

    @center_frequency.setter
    def center_frequency(self, value):
        span = self.span
        if span > value:
            raise ValueError("Span frequency {} can't exceed center frequency "
                             "{}".format(span, value))
        self._write(('FMCENTERF.', Float(min=0, max=self._fmax)))

    @property
    def span_frequency(self):
        return self._query(('FMSPANF.', Float))

    @span_frequency.setter
    def span_frequency(self, value):
        center_freq = self.center_frequency
        if value > center_freq:
            raise ValueError("Span frequency {} can't exceed center frequency "
                             "{}".format(value, center_freq))
        self._write(('FMSPANF.', Float(min=0, max=self._fmax / 2.)))


class DAC(Driver):
    """

    :ivar voltage: The user specified DAC output voltage.
    :ivar output: Defines which output apears on the DAC. The allowed values
        depend on the DAC channel. See :attr:`~.DAC.OUTPUT`.

    """
    OUTPUT = [
        ('x1', 'noise', 'ratio', 'logratio', 'equation1', 'equation2', 'user', 'demod1', 'r2'),
        ('y1', 'noise', 'ratio', 'logratio', 'equation1', 'equation2', 'user', 'ext adc monitor', 'theta2'),
        ('r1', 'noise', 'ratio', 'logratio', 'equation1', 'equation2', 'user', 'demod2', 'x2'),
        ('theta1', 'noise', 'ratio', 'logratio', 'equation1', 'equation2', 'user', 'sync', 'y2'),
    ]
    def __init__(self, transport, protocol, idx):
        super(DAC, self).__init__(transport, protocol)
        self.voltage = Command(
            'DAC. {}'.format(idx),
            'DAC. {} '.format(idx),
            Float(min=-10., max=10.)
        )
        self.output = Command(
            'CH {}'.format(idx),
            'CH {} '.format(idx),
            Enum(*DAC.OUTPUT[idx - 1])
        )


class DigitalPort(Driver):
    """The digital port configuration.

    :ivar output: Defines which ports are configured as outputs.
    :ivar value: Reads the bit state of all lines but writes only to output
        lines.

    """
    DIGITAL_OUTPUT = {
        0: 'DO',
        1: 'D1',
        2: 'D2',
        3: 'D3',
        4: 'D4',
        5: 'D5',
        6: 'D6',
        7: 'D7',
    }
    def __init__(self, transport, protocol):
        super(DigitalPort, self).__init__(transport, protocol)
        self.output = Command(
            'PORTDIR',
            'PORTDIR',
            Register(DigitalPort.DIGITAL_OUTPUT)
        )
        self.value = Command(
            'READBYTE',
            'BYTE',
            Register(DigitalPort.DIGITAL_OUTPUT)
        )


class FastBuffer(Driver):
    """Represents the fast curve buffer command group.

    The fast curve buffer is similar to the :class:`~.StandardBuffer`. It is
    less flexible but allows for the fastest data acquisition rate.

    :ivar length: The length of the fast curve buffer, at most 100000 can be
        stored.
    :ivar enabled: A boolean flag enabling/disabling the fast curve buffer.

        .. note::

            Enabling the fast curve buffer disables the standard curve buffer.

    :ivar storage_interval: The storage interval in microseconds. The smallest
        value is 1.

    """
    KEYS = [
        'x', 'y', 'demod1', 'adc1', 'adc2', 'x2', 'y2', 'demod2'
    ]
    def __init__(self, transport, protocol):
        super(FastBuffer, self).__init__(transport, protocol)
        self.length = Command('LEN', 'LEN', Integer(min=0, max=100001))
        self.enabled = Command('CMODE', 'CMODE', Boolean)
        self.storage_interval = Command('STR', 'STR', Integer(min=1))

    def __getitem__(self, item):
        try:
            idx = str(FastBuffer.KEYS.index(item))
        except ValueError:
            raise KeyError('Invalid Curve key: {}'.format(item))
        # The data is stored as two byte integers.
        nbytes = self.length * 2
        data = self._protocol.query_bytes(self._transport, nbytes, 'DCB', idx)
        return np.frombuffer(data, dtype='>h')


class StandardBuffer(Driver):
    """Represents the standard buffer command group.

    :ivar length: The size of the standard curve buffer is 100000 points. These
        are shared equally between all define curves.
    :ivar enabled: A boolean flag enabling/disabling the fast curve buffer.

        .. note::

            Enabling the fast curve buffer disables the standard curve buffer.
    :ivar storage_interval: The storage interval in microseconds. The smallest
        value is 1000.
    :ivar define: Selects which curves should be stored. See
        :attr:`~.StandardBuffer.KEYS` for allowed values.

    """
    KEYS = [
        'x', 'y', 'r', 'theta', 'sensitivity', 'noise', 'ratio', 'log ratio',
        'adc1', 'adc2', 'adc3', 'adc4', 'dac1', 'dac2', 'event',
        'frequency', 'frequency',
        'x2', 'y2', 'r2', 'theta2', 'sensitivity2'
    ]
    def __init__(self, transport, protocol):
        super(StandardBuffer, self).__init__(transport, protocol)
        self.enabled = Command('CMODE', 'CMODE', Enum(True, False))
        self.storage_interval = Command('STR', 'STR', Integer(min=1000))
        self._define = Command(
            'CBD',
            'CBD',
            Register({i: v for i, v in enumerate(StandardBuffer.KEYS)})
        )

    @property
    def length(self):
        return self._query(('LEN', Integer))

    @length.setter
    def length(self, value):
        curves = self.define
        # Calculate the max curve buffer length.
        # Note: The frequency needs twice as much space than other curves.
        if 'frequency' in curves:
            maxlen = 100000 / (len(curves) + 1)
        else:
            maxlen = 100000 / len(curves)
        if value > maxlen:
            raise ValueError('Value {} is too large; max: {}'.format(value, maxlen))
        self._write(('LEN', Integer), value)

    @property
    def define(self):
        return [k for k, v in self._define.items() if v is True]

    @define.setter
    def define(self, value):
        self._define = {v: True for v in value}

    def event(self, value):
        """Set an event marker.

        If the event curve is defined and data acquisition is running, a call to
        event stores the value in the event curve.

        """
        self._write(('EVENT', Integer(min=0, max=32768)), value)

    def __getitem__(self, item):
        if not item in self.define:
            raise KeyError(item)
        idx = str(StandardBuffer.KEYS.index(item))
        # The data is stored as two byte integers.
        nbytes = self.length * 2

        if item == 'frequency':
            f1 = self._protocol.query_bytes(self._transport, nbytes, 'DCB', '15')
            f2 = self._protocol.query_bytes(self._transport, nbytes, 'DCB', '16')
            f1 = np.frombuffer(data, dtype='>H')
            f2 = np.frombuffer(data, dtype='>h')
            return (f2.astype(float) * 65536 + f1.astype(float)) / 1e3
        else:
            data = self._protocol.query_bytes(self._transport, nbytes, 'DCB', idx)
            return np.frombuffer(data, dtype='>h')


class Demodulator(Driver):
    """Implements the dual reference mode commands.

    .. note::

       These commands only work if the lockin is in dual reference mode. See
       :attr:`~.SR7230.reference_mode`.

    :ivar x: A float representing the X-channel output in either volt or
        ampere. (read only)
    :ivar y: A float representing the Y-channel output in either volt or
        ampere. (read only)
    :ivar x_offset: The x-channel output offset control.
        *(<enabled>, <range>)*, where

        * *<enabled>* A boolean enabling/disabling the output offset.
        * *<range>* The range of the offset, an integer between -30000 and
          30000 corresponding to +/- 300%.

    :ivar y_offset: The y-channel output offset control.
        *(<enabled>, <range>)*, where

        * *<enabled>* A boolean enabling/disabling the output offset.
        * *<range>* The range of the offset, an integer between -30000 and
          30000 corresponding to +/- 300%.

    :ivar xy: X and Y-channel output with the following format *(<x>, <y>)*.
        (read only)
    :ivar r: The signal magnitude, as float. (read only)
    :ivar theta: The signal phase, as float. (read only)
    :ivar r_theta: The magnitude and the signal phase. *(<r>, <theta>)*.
        (read only)
    :ivar reference_phase: The phase of the reference signal, a float ranging
        from -360 to 360 corresponding to the angle in degrees with a resolution
        of mili degree.
    :ivar harmonic: The reference harmonic mode, an integer between 1 and 128
        corresponding to the first to 127 harmonics.
    :ivar slope: The output lowpass filter slope in dB/octave, either '6 dB',
        '12 dB', '18 dB' or '24 dB'.

        .. note::

            If :attr:¸.noise_measurement` or :attr:`.fastmode` is enabled, only
            '6 dB' and '12 dB' are valid.

    :ivar time_constant: The filter time constant. See
        :attr:`~.SR7230.TIME_CONSTANT` for proper values.

        .. note::

            If :attr:`.noise_measurement` is enabled, only '500 us', '1 ms',
            '2 ms', '5 ms' and '10 ms' are valid.

    :ivar sensitivity: The full-scale sensitivity. The valid entries depend on
        the current mode. See :attr:`~.SR7230.sensitivity` for valid entries.

    """
    def __init__(self, transport, protocol, idx):
        super(Demodulator, self).__init__(transport, protocol)
        self.idx = idx
        self.x = Command(('X{}.'.format(idx), Float))
        self.x_offset = Command(
            'XOF{}'.format(idx),
            'XOF{}'.format(idx),
            [Boolean, Integer(min=-30000, max=30000)]
        )
        self.y = Command(('Y{}.'.format(idx), Float))
        self.y_offset = Command(
            'YOF{}'.format(idx),
            'YOF{}'.format(idx),
            [Boolean, Integer(min=-30000, max=30000)]
        )
        self.xy = Command(('XY{}.'.format(idx), [Float, Float]))
        self.r = Command(('MAG{}.', Float))
        self.theta = Command(('PHA{}.', Float))
        self.r_theta = Command(('MP{}.', [Float, Float]))
        self.reference_phase = Command(
            'REFP{}.'.format(idx),
            'REFP{}.'.format(idx),
            Float(min=-360., max=360., fmt='{:.3f}')
        )
        self.harmonic = Command(
            'REFN{}'.format(idx),
            'REFN{}'.format(idx),
            Integer(min=1, max=128)
        )
        self.slope = Command(
            'SLOPE{}'.format(idx),
            'SLOPE{}'.format(idx),
            Enum('6 dB', '12 dB', '18 dB', '24 dB')
        )
        self.time_constant = Command(
            'TC{}'.format(idx),
            'TC{}'.format(idx),
            Enum(*SR7230.TIME_CONSTANT)
        )
        self._voltage_sensitivity = Command(
            'SEN{}'.format(idx),
            'SEN{}'.format(idx),
            Enum(*SR7230.SENSITIVITY_VOLTAGE, start=1)
        )
        self._highbandwidth_sensitivity = Command(
            'SEN{}'.format(idx),
            'SEN{}'.format(idx),
            Enum(*SR7230.SENSITIVITY_CURRENT_HIGHBW, start=1)
        )
        self._lownoise_sensitivity = Command(
            'SEN{}'.format(idx),
            'SEN{}'.format(idx),
            Enum(*SR7230.SENSITIVITY_CURRENT_LOWNOISE, start=7)
        )

    @property
    def sensitivity(self):
        imode = self._query((
            'IMODE',
            Enum('off', 'high bandwidth', 'low noise')
        ))
        if imode == 'off':
            return self._voltage_sensitivity
        elif imode == 'high bandwidth':
            return self._highbandwidth_sensitivity
        else:
            return self._lownoise_sensitivity

    @sensitivity.setter
    def sensitivity(self, value):
        imode = self._query((
            'IMODE',
            Enum('off', 'high bandwidth', 'low noise')
        ))
        if imode == 'off':
            self._voltage_sensitivity = value
        elif imode == 'high bandwidth':
            self._highbandwidth_sensitivity = value
        else:
            self._lownoise_sensitivity = value

    def auto_sensitivity(self):
        """Triggers the auto sensitivity mode.

        When the auto sensitivity mode is triggered, the SR7225 adjustes the
        sensitivity so that the signal magnitude lies in between 30% and 90%
        of the full scale sensitivity.
        """
        self._write('AS{}'.format(self.idx))

    def auto_phase(self):
        """Triggers the auto phase mode."""
        self._write('AQN{}'.format(self.idx))

    def auto_offset(self):
        """Triggers the auto offset mode."""
        self._write('AXO{}'.format(idx))
