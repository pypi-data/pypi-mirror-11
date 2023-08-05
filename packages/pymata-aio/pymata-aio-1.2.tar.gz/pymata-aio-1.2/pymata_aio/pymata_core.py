"""
Copyright (c) 2015 Alan Yorinks All rights reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU  General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import asyncio
import sys
import time
import signal
# import os

import serial

from .constants import Constants
from .private_constants import PrivateConstants
from .pin_data import PinData
from .pymata_serial import PymataSerial


class PymataCore:
    """
    This class exposes and implements the pymata_core asyncio API, It includes the public API methods as well as
    a set of private methods. If your application is using asyncio, this is the API that you should use.

    After instantiating this class, its "start" method MUST be called to perform Arduino pin auto-detection.
    """

    def __init__(self, arduino_wait=2, sleep_tune=.001, com_port=None):
        """
        This is the "constructor" method for the PymataCore class.
        @param arduino_wait: Amount of time to wait for Arduino to reset. UNO takes 2 seconds, Leonardo can be zero
        @param sleep_tune: This parameter sets the amount of time PyMata core uses to set asyncio.sleep
        @param com_port: Manually selected com port - normally it is auto-detected
        @return: This method never returns
        """
        self.sleep_tune = sleep_tune
        self.arduino_wait = arduino_wait
        self.com_port = com_port

        # this dictionary for mapping incoming Firmata message types to handlers for the messages
        self.command_dictionary = {PrivateConstants.REPORT_VERSION: self._report_version,
                                   PrivateConstants.REPORT_FIRMWARE: self._report_firmware,
                                   PrivateConstants.CAPABILITY_RESPONSE: self._capability_response,
                                   PrivateConstants.ANALOG_MAPPING_RESPONSE: self._analog_mapping_response,
                                   PrivateConstants.PIN_STATE_RESPONSE: self._pin_state_response,
                                   PrivateConstants.STRING_DATA: self._string_data,
                                   PrivateConstants.ANALOG_MESSAGE: self._analog_message,
                                   PrivateConstants.DIGITAL_MESSAGE: self._digital_message,
                                   PrivateConstants.I2C_REPLY: self._i2c_reply,
                                   PrivateConstants.SONAR_DATA: self._sonar_data,
                                   PrivateConstants.ENCODER_DATA: self._encoder_data}

        # report query results are stored in this dictionary
        self.query_reply_data = {PrivateConstants.REPORT_VERSION: '', PrivateConstants.STRING_DATA: '',
                                 PrivateConstants.REPORT_FIRMWARE: '',
                                 PrivateConstants.CAPABILITY_RESPONSE: None,
                                 PrivateConstants.ANALOG_MAPPING_RESPONSE: None,
                                 PrivateConstants.PIN_STATE_RESPONSE: None}

        # An i2c_map entry consists of a device i2c address as the key, and the value of the key consists of a
        # dictionary containing 2 entries. The first entry. 'value' contains the last value reported, and
        # the second, 'callback' contains a reference to a callback function.
        # For example: {12345: {'value': 23, 'callback': None}}
        self.i2c_map = {}

        # the active_sonar_map maps the sonar trigger pin number (the key) to the current data value returned
        # if a callback was specified, it is stored in the map as well.
        # an entry in the map consists of:
        #   pin: [callback,[current_data_returned]]
        self.active_sonar_map = {}

        # The latch_map is a dictionary that stores all latches setup by the user.
        # The key is a string defined as follows:
        #   Digital Pin : D + pin number (D12)
        #   Analog  Pin: A + pin number (A3)

        # The value associated with each key is a list comprised of:

        # [latched_state, threshold_type, threshold_value, latched_data, time_stamp]

        #   latched_state: Each list entry contains a latch state, a threshold type, a threshold value value
        #           the data value at time of latching,  and a date stamp when latched.
        # A latch state:

        # LATCH_IGNORE = 0  # this item currently not participating in latching
        # LATCH_ARMED = 1  # When the next item value change is received and,if it matches the latch
        #                    criteria, the data will be latched
        # LATCH_LATCHED = 2  # data has been latched. Read the data to re-arm the latch

        # threshold type:
        #     LATCH_EQ = 0  data value is equal to the latch threshold value
        #     LATCH_GT = 1  data value is greater than the latch threshold value
        #     LATCH_LT = 2  data value is less than the latch threshold value
        #     LATCH_GTE = 3  data value is greater than or equal to the latch threshold value
        #     LATCH_LTE = 4 # data value is less than or equal to the latch threshold value

        # threshold value: target threshold data value

        # latched data value: value of data at time of latching event

        # time stamp: time of latching event

        # analog_latch_table entry = pin: [latched_state, threshold_type, threshold_value, latched_data, time_stamp]
        # digital_latch_table_entry = pin: [latched_state, threshold_type, latched_data, time_stamp]

        self.latch_map = {}

        print('{}{}{}'.format('\n', "pymata_aio Version " + PrivateConstants.PYMATA_VERSION,
                              '\tCopyright (c) 2015 Alan Yorinks All rights reserved.\n'))
        sys.stdout.flush()

        if com_port is None:
            self.com_port = self._discover_port()

        self.sleep_tune = sleep_tune

        # a list of PinData objects - one for each pin segregate by pin type
        self.analog_pins = []
        self.digital_pins = []
        self.loop = None
        self.the_task = None
        self.serial_port = None

    def start(self):
        """
        This method must be called immediately after the class is instantiated. It instantiates the serial
        interface and then performs auto pin discovery.
        @return:No return value.
        """
        self.loop = asyncio.get_event_loop()
        try:
            self.serial_port = PymataSerial(self.com_port, 57600, self.sleep_tune)
        except serial.SerialException:
            print('Cannot instantiate serial interface: ' + self.com_port)
            sys.exit(0)

        # wait for arduino to go through a reset cycle if need be
        time.sleep(self.arduino_wait)

        # register the get_command method with the event loop
        self.loop = asyncio.get_event_loop()
        self.the_task = self.loop.create_task(self._command_dispatcher())

        # get an analog pin map
        asyncio.async(self.get_analog_map())

        # try to get an analog report. if it comes back as none - shutdown
        report = self.loop.run_until_complete(self.get_analog_map())
        if not report:
            print('\n\n{} {} ***'.format('*** Analog map query timed out waiting for port:',
                                         self.serial_port.com_port))
            print('\nIs your Arduino plugged in?')
            try:
                loop = asyncio.get_event_loop()
                for t in asyncio.Task.all_tasks(loop):
                    t.cancel()
                loop.run_until_complete(asyncio.sleep(.1))
                loop.close()
                loop.stop()
                sys.exit(0)
            except RuntimeError:
                # this suppresses the Event Loop Is Running message, which may be a bug in python 3.4.3
                sys.exit(0)
            except TypeError:
                sys.exit(0)

        # custom assemble the pin lists
        for pin in report:
            digital_data = PinData()
            self.digital_pins.append(digital_data)
            if pin != Constants.IGNORE:
                analog_data = PinData()
                self.analog_pins.append(analog_data)

        print('{} {} {} {} {}'.format('Auto-discovery complete. Found', len(self.digital_pins), 'Digital Pins and',
                                      len(self.analog_pins), 'Analog Pins\n\n'))

    @asyncio.coroutine
    def analog_read(self, pin):
        """
        Retrieve the last data update for the specified analog pin.
        @param pin: Analog pin number (ex. A2 is specified as 2)
        @return: Last value reported for the analog pin
        """
        return self.analog_pins[pin].current_value

    @asyncio.coroutine
    def analog_write(self, pin, value):
        """
        Set the selected pin to the specified value.
        @param pin: PWM pin number
        @param value: Pin value (0 - 0x4000)
        @return: No return value
        """
        if PrivateConstants.ANALOG_MESSAGE + pin < 0xf0:
            command = [PrivateConstants.ANALOG_MESSAGE + pin, value & 0x7f, value >> 7]
            yield from self._send_command(command)
        else:
            yield from self.extended_analog(pin, value)

    @asyncio.coroutine
    def digital_read(self, pin):
        """
        Retrieve the last data update for the specified digital pin.
        @param pin: Digital pin number
        @return: Last value reported for the digital pin
        """
        return self.digital_pins[pin].current_value

    @asyncio.coroutine
    def digital_write(self, pin, value):
        """
        Set the specified pin to the specified value.
        @param pin: pin number
        @param value: pin value
        @return: No return value
        """
        # The command value is not a fixed value, but needs to be calculated using the
        # pin's port number
        port = pin // 8

        calculated_command = PrivateConstants.DIGITAL_MESSAGE + port
        mask = 1 << (pin % 8)
        # Calculate the value for the pin's position in the port mask
        if value == 1:
            PrivateConstants.DIGITAL_OUTPUT_PORT_PINS[port] |= mask
        else:
            PrivateConstants.DIGITAL_OUTPUT_PORT_PINS[port] &= ~mask

        # Assemble the command
        command = (calculated_command, PrivateConstants.DIGITAL_OUTPUT_PORT_PINS[port] & 0x7f,
                   PrivateConstants.DIGITAL_OUTPUT_PORT_PINS[port] >> 7)

        yield from self._send_command(command)

    @asyncio.coroutine
    def disable_analog_reporting(self, pin):
        """
        Disables analog reporting for a single analog pin.
        @param pin: Analog pin number. For example for A0, the number is 0.
        @return: No return value
        """
        command = [PrivateConstants.REPORT_ANALOG + pin, PrivateConstants.REPORTING_DISABLE]
        yield from self._send_command(command)

    @asyncio.coroutine
    def disable_digital_reporting(self, pin):
        """
        Disables digital reporting. By turning reporting off for this pin, Reporting
        is disabled for all 8 bits in the "port" -
        @param pin: Pin and all pins for this port
        @return: No return value
        """
        port = pin // 8
        command = [PrivateConstants.REPORT_DIGITAL + port, PrivateConstants.REPORTING_DISABLE]
        yield from self._send_command(command)

    @asyncio.coroutine
    def encoder_config(self, pin_a, pin_b, cb=None):
        """
        This command enables the rotary encoder (2 pin + ground) and will
        enable encoder reporting.

        NOTE: This command is not currently part of standard arduino firmata, but is provided for legacy
        support of CodeShield on an Arduino UNO.

        Encoder data is retrieved by performing a digital_read from pin a (encoder pin_a)

        @param pin_a: Encoder pin 1.
        @param pin_b: Encoder pin 2.
        @param cb: callback function to report encoder changes
        @return: No return value
        """
        data = [pin_a, pin_b]
        if cb:
            self.digital_pins[pin_a].cb = cb
        yield from self._send_sysex(PrivateConstants.ENCODER_CONFIG, data)

    @asyncio.coroutine
    def encoder_read(self, pin):
        """
        This method retrieves the latest encoder data value
        @param pin: Encoder Pin
        @return: encoder data value
        """
        return self.digital_pins[pin].current_value

    @asyncio.coroutine
    def enable_analog_reporting(self, pin):
        """
        Enables analog reporting. By turning reporting on for a single pin,
        @param pin: Analog pin number. For example for A0, the number is 0.
        @return: No return value
        """
        command = [PrivateConstants.REPORT_ANALOG + pin, PrivateConstants.REPORTING_ENABLE]
        yield from self._send_command(command)

    @asyncio.coroutine
    def enable_digital_reporting(self, pin):
        """
        Enables digital reporting. By turning reporting on for all 8 bits in the "port" -
        this is part of Firmata's protocol specification.
        @param pin: Pin and all pins for this port
        @return: No return value
        """
        port = pin // 8
        command = [PrivateConstants.REPORT_DIGITAL + port, PrivateConstants.REPORTING_ENABLE]
        yield from self._send_command(command)

    @asyncio.coroutine
    def extended_analog(self, pin, data):
        """
        This method will send an extended-data analog write command to the selected pin.
        @param pin: 0 - 127
        @param data: 0 - 0xfffff
        @return: No return value
        """
        analog_data = [pin, data & 0x7f, (data >> 7) & 0x7f, data >> 14]
        yield from self._send_sysex(PrivateConstants.EXTENDED_ANALOG, analog_data)

    @asyncio.coroutine
    def get_analog_latch_data(self, pin):
        """
        A list is returned containing the latch state for the pin, the latched value, and the time stamp
        [latched_state, threshold_type, threshold_value, latched_data, time_stamp]
        @param pin: Pin number.
        @return:  [latched_state, threshold_type, threshold_value, latched_data, time_stamp]
        """
        key = 'A' + str(pin)
        if key in self.latch_map:
            entry = self.latch_map.get(key)
            return entry
        else:
            return None

    @asyncio.coroutine
    def get_analog_map(self):
        """
        This method requests a Firmata analog map query and returns the results.
        @return: An analog map response or None if a timeout occurs
        """
        # get the current time to make sure a report is retrieved
        current_time = time.time()

        # if we do not have existing report results, send a Firmata message to request one
        if self.query_reply_data.get(PrivateConstants.ANALOG_MAPPING_QUERY) is None:
            yield from self._send_sysex(PrivateConstants.ANALOG_MAPPING_QUERY, None)
            # wait for the report results to return for 2 seconds
            # if the timer expires, shutdown
            while self.query_reply_data.get(PrivateConstants.ANALOG_MAPPING_RESPONSE) is None:
                elapsed_time = time.time()
                if elapsed_time - current_time > 2:
                    return None
                yield from asyncio.sleep(self.sleep_tune)
        return self.query_reply_data.get(PrivateConstants.ANALOG_MAPPING_RESPONSE)

    @asyncio.coroutine
    def get_capability_report(self):
        """
        This method requests and returns a Firmata capability query report
        @return: A capability report in the form of a list
        """
        if self.query_reply_data.get(PrivateConstants.CAPABILITY_QUERY) is None:
            yield from self._send_sysex(PrivateConstants.CAPABILITY_QUERY, None)
            while self.query_reply_data.get(PrivateConstants.CAPABILITY_RESPONSE) is None:
                yield from asyncio.sleep(self.sleep_tune)
        return self.query_reply_data.get(PrivateConstants.CAPABILITY_RESPONSE)

    @asyncio.coroutine
    def get_digital_latch_data(self, pin):
        """
        A list is returned containing the latch state for the pin, the latched value, and the time stamp
        [pin_num, latch_state, latched_value, time_stamp]
        @param pin: Pin number.
        @return:  [latched_state, threshold_type, threshold_value, latched_data, time_stamp]
        """
        key = 'D' + str(pin)
        if key in self.latch_map:
            entry = self.latch_map.get(key)
            return entry
        else:
            return None

    @asyncio.coroutine
    def get_firmware_version(self):
        """
        This method retrieves the Firmata firmware version
        @return: Firmata firmware version
        """
        if self.query_reply_data.get(PrivateConstants.REPORT_FIRMWARE) == '':
            yield from self._send_sysex(PrivateConstants.REPORT_FIRMWARE, None)
            while self.query_reply_data.get(PrivateConstants.REPORT_FIRMWARE) == '':
                yield from asyncio.sleep(self.sleep_tune)
        reply = ''
        for x in self.query_reply_data.get(PrivateConstants.REPORT_FIRMWARE):
            reply_data = ord(x)
            if reply_data:
                reply += chr(reply_data)
        self.query_reply_data[PrivateConstants.REPORT_FIRMWARE] = reply
        return self.query_reply_data.get(PrivateConstants.REPORT_FIRMWARE)

    @asyncio.coroutine
    def get_protocol_version(self):
        """
        This method returns the major and minor values for the protocol version, i.e. 2.4
        @return: Firmata protocol version
        """
        if self.query_reply_data.get(PrivateConstants.REPORT_VERSION) == '':
            yield from self._send_command(PrivateConstants.REPORT_VERSION)
            while self.query_reply_data.get(PrivateConstants.REPORT_VERSION) == '':
                yield from asyncio.sleep(self.sleep_tune)
        return self.query_reply_data.get(PrivateConstants.REPORT_VERSION)

    @asyncio.coroutine
    def get_pin_state(self, pin):
        """
        This method retrieves a pin state report for the specified pin
        @param pin: Pin of interest
        @return: pin state report
        """
        pin_list = [pin]
        yield from self._send_sysex(PrivateConstants.PIN_STATE_QUERY, pin_list)
        while self.query_reply_data.get(PrivateConstants.PIN_STATE_RESPONSE) is None:
            yield from asyncio.sleep(self.sleep_tune)
        pin_state_report = self.query_reply_data.get(PrivateConstants.PIN_STATE_RESPONSE)
        self.query_reply_data[PrivateConstants.PIN_STATE_RESPONSE] = None
        return pin_state_report

    @asyncio.coroutine
    def get_pymata_version(self):
        """
        This method retrieves the PyMata version number
        @return: PyMata version number.
        """
        return PrivateConstants.PYMATA_VERSION

    @asyncio.coroutine
    def i2c_config(self, read_delay_time=0):
        """
        NOTE: THIS METHOD MUST BE CALLED BEFORE ANY I2C REQUEST IS MADE
        This method initializes Firmata for I2c operations.

        @param read_delay_time (in microseconds): an optional parameter, default is 0
        @return: No Return Value
        """
        data = [read_delay_time & 0x7f, read_delay_time >> 7]
        yield from self._send_sysex(PrivateConstants.I2C_CONFIG, data)

    @asyncio.coroutine
    def i2c_read_data(self, address):
        """
        This method retrieves cached i2c data to support a polling mode.
        @param address: I2C device address
        @return:Last cached value read
        """
        if address in self.i2c_map:
            map_entry = self.i2c_map.get(address)
            data = map_entry.get('value')
            return data
        else:
            return None

    @asyncio.coroutine
    def i2c_read_request(self, address, register, number_of_bytes, read_type, cb=None):
        """
        This method requests the read of an i2c device. Results are retrieved by a call to
        i2c_get_read_data(). or by callback.
        If a callback method is provided, when data is received from the device it will be sent to the callback method.
        Some devices require that transmission be restarted (e.g. MMA8452Q accelerometer).
        Use I2C_READ | I2C_RESTART_TX for those cases.
        @param address: i2c device address
        @param register: register number (can be set to zero)
        @param number_of_bytes: number of bytes expected to be returned
        @param read_type: I2C_READ  or I2C_READ_CONTINUOUSLY. I2C_RESTART_TX may be OR'ed when required
        @param cb: Optional callback function to report i2c data as result of read command
        @return: No return value.
        """

        if address not in self.i2c_map:
            # self.i2c_map[address] = [None, cb]
            self.i2c_map[address] = {'value': None, 'callback': cb}
        data = [address, read_type, register & 0x7f, register >> 7,
                number_of_bytes & 0x7f, number_of_bytes >> 7]
        yield from self._send_sysex(PrivateConstants.I2C_REQUEST, data)

    @asyncio.coroutine
    def i2c_write_request(self, address, args):
        """
        Write data to an i2c device.
        @param address: i2c device address
        @param args: A variable number of bytes to be sent to the device passed in as a list
        @return: No return value.
        """
        data = [address, Constants.I2C_WRITE]
        for item in args:
            item_lsb = item & 0x7f
            data.append(item_lsb)
            item_msb = item >> 7
            data.append(item_msb)
        yield from self._send_sysex(PrivateConstants.I2C_REQUEST, data)

    @asyncio.coroutine
    def play_tone(self, pin, tone_command, frequency, duration):
        """
        This method will call the Tone library for the selected pin.
        It requires FirmataPlus to be loaded onto the arduino
        If the tone command is set to TONE_TONE, then the specified tone will be played.
        Else, if the tone command is TONE_NO_TONE, then any currently playing tone will be disabled.
        @param pin: Pin number
        @param tone_command: Either TONE_TONE, or TONE_NO_TONE
        @param frequency: Frequency of tone
        @param duration: Duration of tone in milliseconds
        @return: No return value
        """
        # convert the integer values to bytes
        if tone_command == Constants.TONE_TONE:
            # duration is specified
            if duration:
                data = [tone_command, pin, frequency & 0x7f, frequency >> 7, duration & 0x7f, duration >> 7]

            else:
                data = [tone_command, pin, frequency & 0x7f, frequency >> 7, 0, 0]

                # self._command_handler.digital_response_table[pin][self._command_handler.RESPONSE_TABLE_MODE] = \
                # self.TONE
        # turn off tone
        else:
            data = [tone_command, pin]
        yield from self._send_sysex(PrivateConstants.TONE_DATA, data)

    @asyncio.coroutine
    def send_reset(self):
        """
        Send a Sysex reset command to the arduino
        @return: No return value.
        """
        try:
            yield from self._send_command([PrivateConstants.SYSTEM_RESET])
        except RuntimeError:
            exit(0)

    @asyncio.coroutine
    def servo_config(self, pin, min_pulse=544, max_pulse=2400):
        """
        Configure a pin as a servo pin. Set pulse min, max in ms.
        Use this method (not set_pin_mode) to configure a pin for servo operation.
        @param pin: Servo Pin.
        @param min_pulse: Min pulse width in ms.
        @param max_pulse: Max pulse width in ms.
        @return: No return value
        """
        # self.set_pin_mode(pin, PrivateConstants.SERVO, PrivateConstants.OUTPUT)
        command = [pin, min_pulse & 0x7f, min_pulse >> 7, max_pulse & 0x7f,
                   max_pulse >> 7]

        yield from self._send_sysex(PrivateConstants.SERVO_CONFIG, command)

    @asyncio.coroutine
    def set_analog_latch(self, pin, threshold_type, threshold_value, cb=None):
        """
        This method "arms" an analog pin for its data to be latched and saved in the latching table
        If a callback method is provided, when latching criteria is achieved, the callback function is called
        with latching data notification.
        Data returned in the callback list has the pin number as the first element,
        @param pin: Analog pin number (value following an 'A' designator, i.e. A5 = 5
        @param threshold_type: ANALOG_LATCH_GT | ANALOG_LATCH_LT  | ANALOG_LATCH_GTE | ANALOG_LATCH_LTE
        @param threshold_value: numerical value - between 0 and 1023
        @param cb: callback method
        @return: True if successful, False if parameter data is invalid
        """
        if Constants.LATCH_GT <= threshold_type <= Constants.LATCH_LTE:
            key = 'A' + str(pin)
            if 0 <= threshold_value <= 1023:
                self.latch_map[key] = [Constants.LATCH_ARMED, threshold_type, threshold_value, 0, 0, cb]
                return True
        else:
            return False

    @asyncio.coroutine
    def set_digital_latch(self, pin, threshold_value, cb=None):
        """
        This method "arms" a digital pin for its data to be latched and saved in the latching table
        If a callback method is provided, when latching criteria is achieved, the callback function is called
        with latching data notification.
        Data returned in the callback list has the pin number as the first element,
        @param pin: Digital pin number
        @param threshold_value: 0 or 1
        @param cb: callback function
        @return: True if successful, False if parameter data is invalid
        """
        if 0 <= threshold_value <= 1:
            key = 'D' + str(pin)
            self.latch_map[key] = [Constants.LATCH_ARMED, Constants.LATCH_EQ, threshold_value, 0, 0, cb]
            return True
        else:
            return False

    @asyncio.coroutine
    def set_pin_mode(self, pin_number, pin_state, callback=None):
        """
        This method sets the pin mode for the specified pin. For Servo, use servo_config() instead.
        @param pin_number: Arduino Pin Number
        @param pin_state:INPUT/OUTPUT/ANALOG/PWM/
        @param callback: Optional: A reference to a call back function to be called when pin data value changes
        @return: No return value.
        """
        if callback:
            if pin_state == Constants.INPUT:
                self.digital_pins[pin_number].cb = callback
            elif pin_state == Constants.ANALOG:
                self.analog_pins[pin_number].cb = callback
            else:
                print('{} {}'.format('set_pin_mode: callback ignored for pin state:', pin_state))
        #
        if pin_state == Constants.INPUT or pin_state == Constants.ANALOG:
            pin_mode = Constants.INPUT
        else:
            pin_mode = pin_state
        command = [PrivateConstants.SET_PIN_MODE, pin_number, pin_mode]
        yield from self._send_command(command)
        if pin_state == Constants.ANALOG:
            yield from self.enable_analog_reporting(pin_number)
        elif pin_state == Constants.INPUT:
            yield from self.enable_digital_reporting(pin_number)
        else:
            pass

    @asyncio.coroutine
    def set_sampling_interval(self, interval):
        """
        This method sends the desired sampling interval to Firmata.
        Note: Standard Firmata  will ignore any interval less than 10 milliseconds
        @param interval: Integer value for desired sampling interval in milliseconds
        @return: No return value.
        """
        data = [interval & 0x7f, interval >> 7]
        self._send_sysex(PrivateConstants.SAMPLING_INTERVAL, data)

    @asyncio.coroutine
    def shutdown(self):
        """
        This method attempts an orderly shutdown
        @return: No return value
        """
        print('Shutting down ...')
        yield from self.send_reset()
        yield from asyncio.sleep(1)
        signal.alarm(1)

    @asyncio.coroutine
    def sleep(self, sleep_time):
        """
        This method is a proxy method for asyncio.sleep
        @param sleep_time: Sleep interval in seconds
        @return:No return value.
        """
        try:
            yield from asyncio.sleep(sleep_time)
        except RuntimeError:
            print('sleep exception')
            self.shutdown()

    @asyncio.coroutine
    def sonar_config(self, trigger_pin, echo_pin, cb=None, ping_interval=50, max_distance=200):
        """
        Configure the pins,ping interval and maximum distance for an HC-SR04 type device.
        Single pin configuration may be used. To do so, set both the trigger and echo pins to the same value.
        Up to a maximum of 6 SONAR devices is supported
        If the maximum is exceeded a message is sent to the console and the request is ignored.
        NOTE: data is measured in centimeters
        @param trigger_pin: The pin number of for the trigger (transmitter).
        @param echo_pin: The pin number for the received echo.
        @param cb: optional callback function to report sonar data changes
        @param ping_interval: Minimum interval between pings. Lowest number to use is 33 ms.Max is 127
        @param max_distance: Maximum distance in cm. Max is 200.
        @return:No return value.

        """

        # if there is an entry for the trigger pin in existence, just exit
        if trigger_pin in self.active_sonar_map:
            return

        if max_distance > 200:
            max_distance = 200
        max_distance_lsb = max_distance & 0x7f
        max_distance_msb = max_distance >> 7
        data = [trigger_pin, echo_pin, ping_interval, max_distance_lsb, max_distance_msb]
        self.set_pin_mode(trigger_pin, Constants.SONAR, Constants.INPUT)
        self.set_pin_mode(echo_pin, Constants.SONAR, Constants.INPUT)
        # update the ping data map for this pin
        if len(self.active_sonar_map) > 6:

            # if self.verbose:
            print("sonar_config: maximum number of devices assigned - ignoring request")
            # return
        else:
            self.active_sonar_map[trigger_pin] = [cb, 0]

        yield from self._send_sysex(PrivateConstants.SONAR_CONFIG, data)

    @asyncio.coroutine
    def sonar_data_retrieve(self, trigger_pin):
        """
        Retrieve Ping (HC-SR04 type) data. The data is presented as a dictionary.
        The 'key' is the trigger pin specified in sonar_config() and the 'data' is the
        current measured distance (in centimeters)
        for that pin. If there is no data, the value is set to None.
        @param trigger_pin: key into sonar data map
        @return: active_sonar_map
        """
        # sonar_pin_entry = self.active_sonar_map[pin]
        sonar_pin_entry = self.active_sonar_map.get(trigger_pin)
        value = sonar_pin_entry[1]
        return value

    @asyncio.coroutine
    def stepper_config(self, steps_per_revolution, stepper_pins):
        """
        Configure stepper motor prior to operation.
        This is a FirmataPlus feature.
        @param steps_per_revolution: number of steps per motor revolution
        @param stepper_pins: a list of control pin numbers - either 4 or 2
        @return:No return value.

        """
        data = [PrivateConstants.STEPPER_CONFIGURE, steps_per_revolution & 0x7f, steps_per_revolution >> 7]
        for pin in range(len(stepper_pins)):
            data.append(stepper_pins[pin])
        yield from self._send_sysex(PrivateConstants.STEPPER_DATA, data)

    @asyncio.coroutine
    def stepper_step(self, motor_speed, number_of_steps):
        """
        Move a stepper motor for the number of steps at the specified speed
        This is a FirmataPlus feature.
        @param motor_speed: 21 bits of data to set motor speed
        @param number_of_steps: 14 bits for number of steps & direction
                                positive is forward, negative is reverse
        @return:No return value.

        """
        if number_of_steps > 0:
            direction = 1
        else:
            direction = 0
        abs_number_of_steps = abs(number_of_steps)
        data = [PrivateConstants.STEPPER_STEP, motor_speed & 0x7f, (motor_speed >> 7) & 0x7f, motor_speed >> 14,
                abs_number_of_steps & 0x7f, abs_number_of_steps >> 7, direction]
        yield from self._send_sysex(PrivateConstants.STEPPER_DATA, data)

    @asyncio.coroutine
    def _command_dispatcher(self):
        """
        This is a private method.
        It continually accepts and interprets data coming from Firmata,and then
        dispatches the correct handler to process the data.
        @return: This method never returns
        """
        # sysex commands are assembled into this list for processing
        sysex = []

        while True:
            try:
                next_command_byte = yield from self.serial_port.read()
                # if this is a SYSEX command, then assemble the entire command process it
                if next_command_byte == PrivateConstants.START_SYSEX:
                    while next_command_byte != PrivateConstants.END_SYSEX:
                        yield from asyncio.sleep(self.sleep_tune)
                        next_command_byte = yield from self.serial_port.read()
                        sysex.append(next_command_byte)
                    yield from self.command_dictionary[sysex[0]](sysex)
                    sysex = []
                    yield from asyncio.sleep(self.sleep_tune)
                # if this is an analog message, process it.
                elif 0xE0 <= next_command_byte < 0xEF:
                    # analog message
                    # assemble the entire analog message in command
                    command = []
                    # get the pin number for the message
                    pin = next_command_byte & 0x0f
                    command.append(pin)
                    # get the next 2 bytes for the command
                    command = yield from self._wait_for_data(command, 2)
                    # process the analog message
                    yield from self._analog_message(command)
                # handle the digital message
                elif 0x90 <= next_command_byte <= 0x9F:
                    command = []
                    pin = next_command_byte & 0x0f
                    command.append(pin)
                    command = yield from self._wait_for_data(command, 2)
                    yield from self._digital_message(command)
                # handle all other messages by looking them up in the command dictionary
                elif next_command_byte in self.command_dictionary:
                    yield from self.command_dictionary[next_command_byte]()
                    yield from asyncio.sleep(self.sleep_tune)
                else:
                    # we need to yield back to the loop
                    yield from asyncio.sleep(self.sleep_tune)
                    continue
                    # yield from asyncio.sleep(self.sleep_tune)
            except Exception as ex:
                # should never get here
                print(ex)
                raise  # re-raise exception.

    '''
    Firmata message handlers
    '''

    @asyncio.coroutine
    def _analog_mapping_response(self, data):
        """
        This is a private message handler method.
        It is a message handler for the analog mapping response message
        @param data: response data
        @return: none - but saves the response
        """
        self.query_reply_data[PrivateConstants.ANALOG_MAPPING_RESPONSE] = data[1:-1]

    @asyncio.coroutine
    def _analog_message(self, data):
        """
        This is a private message handler method.
        It is a message handler for analog messages.
        @param data: message data
        @return: None - but saves the data in the pins structure
        """
        pin = data[0]
        value = (data[PrivateConstants.MSB] << 7) + data[PrivateConstants.LSB]
        # if self.analog_pins[pin].current_value != value:
        self.analog_pins[pin].current_value = value
        if self.analog_pins[pin].cb:
            # append pin number to return value and return as a list
            # self.analog_pins[pin].cb(value)
            value = [pin, value]
            loop = asyncio.get_event_loop()
            loop.call_soon(self.analog_pins[pin].cb, value)

        # is there a latch entry for this pin?
        key = 'A' + str(pin)
        if key in self.latch_map:
            yield from self._check_latch_data(key, value[1])

    @asyncio.coroutine
    def _capability_response(self, data):
        """
        This is a private message handler method.
        It is a message handler for capability report responses.
        @param data: capability report
        @return: None - but report is saved
        """
        self.query_reply_data[PrivateConstants.CAPABILITY_RESPONSE] = data[1:-1]

    @asyncio.coroutine
    def _digital_message(self, data):
        """
        This is a private message handler method.
        It is a message handler for Digital Messages.
        @param data: digital message
        @return: None - but update is saved in pins structure
        """
        port = data[0]
        port_data = (data[PrivateConstants.MSB] << 7) + data[PrivateConstants.LSB]
        pin = port * 8
        for pin in range(pin, min(pin + 8, len(self.digital_pins))):
            self.digital_pins[pin].current_value = port_data & 0x01
            data = [pin, self.digital_pins[pin].current_value]
            if self.digital_pins[pin].cb:
                self.digital_pins[pin].cb(data)
                # is there a latch entry for this pin?
                key = 'D' + str(pin)
                if key in self.latch_map:
                    yield from self._check_latch_data(key, port_data & 0x01)
            port_data >>= 1

    @asyncio.coroutine
    def _encoder_data(self, data):
        """
        This is a private message handler method.
        It handles encoder data messages.
        @param data: encoder data
        @return: None - but update is saved in the digital pins structure
        """
        # strip off sysex start and end
        data = data[1:-1]
        pin = data[0]
        val = int((data[PrivateConstants.MSB] << 7) + data[PrivateConstants.LSB])
        # set value so that it shows positive and negative values
        if val > 8192:
            val -= 16384
        # if this value is different that is what is already in the table store it and check for callback
        if val != self.digital_pins[pin].current_value:
            self.digital_pins[pin].current_value = val
            if self.digital_pins[pin].cb:
                self.digital_pins[pin].cb([pin, val])

    @asyncio.coroutine
    def _i2c_reply(self, data):
        """
        This is a private message handler method.
        It handles replies to i2c_read requests. It stores the data for each i2c device
        address in a dictionary called i2c_map. The data may be retrieved via a polling call to i2c_get_read_data().
        It a callback was specified in pymata.i2c_read, the raw data is sent through the callback
        @param data: raw data returned from i2c device
        """
        # remove the start and end sysex commands from the data
        data = data[1:-1]
        reply_data = []
        # reassemble the data from the firmata 2 byte format
        address = (data[0] & 0x7f) + (data[1] << 7)

        # if we have an entry in the i2c_map, proceed
        if address in self.i2c_map:
            # get 2 bytes, combine them and append to reply data list
            for i in range(0, len(data), 2):
                combined_data = (data[i] & 0x7f) + (data[i+1] << 7)
                reply_data.append(combined_data)

            # place the data in the i2c map without storing the address byte or register byte (returned data only)
            map_entry = self.i2c_map.get(address)
            map_entry['value'] = reply_data[2:]
            self.i2c_map[address] = map_entry
            cb = map_entry.get('callback')
            if cb:
                # send everything, including address and register bytes back to caller
                cb(reply_data)
                yield from asyncio.sleep(self.sleep_tune)

    @asyncio.coroutine
    def _pin_state_response(self, data):
        """
        This is a private message handler method.
        It handles pin state query response messages.
        @param data: Pin state message
        @return: None - but response is saved
        """
        self.query_reply_data[PrivateConstants.PIN_STATE_RESPONSE] = data[1:-1]

    @asyncio.coroutine
    def _report_firmware(self, sysex_data):
        """
        This is a private message handler method.
        This method handles the sysex 'report firmware' command sent by Firmata (0x79).
        It assembles the firmware version by concatenating the major and minor version number components and
        the firmware identifier into a string.
        e.g. "2.3 StandardFirmata.ino"
        @param sysex_data: Sysex data sent from Firmata
        @return: None
        """
        # first byte after command is major number
        major = sysex_data[1]
        version_string = str(major)

        # next byte is minor number
        minor = sysex_data[2]

        # append a dot to major number
        version_string += '.'

        # append minor number
        version_string += str(minor)
        # add a space after the major and minor numbers
        version_string += ' '

        # slice the identifier - from the first byte after the minor number up until, but not including
        # the END_SYSEX byte
        name = sysex_data[3:-1]

        # convert the identifier to printable text and add each character to the version string
        for e in name:
            version_string += chr(e)

        # store the value
        self.query_reply_data[PrivateConstants.REPORT_FIRMWARE] = version_string

    @asyncio.coroutine
    def _report_version(self):
        """
        This is a private message handler method.
        This method reads the following 2 bytes after the report version command (0xF9 - non sysex).
        The first byte is the major number and the second byte is the minor number.
        @return: None
        """
        # get next two bytes
        major = yield from self.serial_port.read()
        version_string = str(major)
        minor = yield from self.serial_port.read()
        version_string += '.'
        version_string += str(minor)
        self.query_reply_data[PrivateConstants.REPORT_VERSION] = version_string

    @asyncio.coroutine
    def _sonar_data(self, data):
        """
        This method handles the incoming sonar data message and stores
        the data in the response table.
        @param data: Message data from Firmata
        @return: No return value.
        """

        # strip off sysex start and end
        data = data[1:-1]
        pin_number = data[0]
        val = int((data[PrivateConstants.MSB] << 7) + data[PrivateConstants.LSB])

        sonar_pin_entry = self.active_sonar_map[pin_number]
        # also write it into the digital response table
        # self.digital_response_table[data[self.RESPONSE_TABLE_MODE]][self.RESPONSE_TABLE_PIN_DATA_VALUE] = val
        # send data through callback if there is a callback function for the pin
        if sonar_pin_entry[0] is not None:
            # check if value changed since last reading
            if sonar_pin_entry[1] != val:
                sonar_pin_entry[1] = val
                self.active_sonar_map[pin_number] = sonar_pin_entry
                # Do a callback if one is specified in the table
                if sonar_pin_entry[0]:
                    sonar_pin_entry[0]([pin_number, val])
        # update the data in the table with latest value
        # sonar_pin_entry[1] = val
        self.active_sonar_map[pin_number] = sonar_pin_entry

        yield from asyncio.sleep(self.sleep_tune)

    @asyncio.coroutine
    def _string_data(self, data):
        """
        This is a private message handler method.
        It is the message handler for String data messages that will be printed to the console.
        @param data:  message
        @return: None - message is sent to console
        """
        reply = ''
        data = data[1:-1]
        for x in data:
            reply_data = x
            if reply_data:
                reply += chr(reply_data)
        print(reply)

    '''
    utilities
    '''

    @asyncio.coroutine
    def _check_latch_data(self, key, data):
        """
        This is a private utility method.
        When a data change message is received this method checks to see if latching needs to be processed
        @param key: encoded pin number
        @param data: data change
        @return: None
        """
        process = False
        latching_entry = self.latch_map.get(key)
        if latching_entry[Constants.LATCH_STATE] == Constants.LATCH_ARMED:
            # Has the latching criteria been met
            if latching_entry[Constants.LATCHED_THRESHOLD_TYPE] == Constants.LATCH_EQ:
                if data == latching_entry[Constants.LATCH_DATA_TARGET]:
                    process = True
            elif latching_entry[Constants.LATCHED_THRESHOLD_TYPE] == Constants.LATCH_GT:
                if data > latching_entry[Constants.LATCH_DATA_TARGET]:
                    process = True
            elif latching_entry[Constants.LATCHED_THRESHOLD_TYPE] == Constants.LATCH_GTE:
                if data >= latching_entry[Constants.LATCH_DATA_TARGET]:
                    process = True
            elif latching_entry[Constants.LATCHED_THRESHOLD_TYPE] == Constants.LATCH_LT:
                if data < latching_entry[Constants.LATCH_DATA_TARGET]:
                    process = True
            elif latching_entry[Constants.LATCHED_THRESHOLD_TYPE] == Constants.LATCH_LTE:
                if data <= latching_entry[Constants.LATCH_DATA_TARGET]:
                    process = True
            if process:
                latching_entry[Constants.LATCHED_DATA] = data
                yield from self._process_latching(key, latching_entry)

    # noinspection PyMethodMayBeStatic
    def _discover_port(self):
        """
        This is a private utility method.
        This method attempts to discover the com port that the arduino is connected to.
        @return: Detected Comport
        """
        locations = ['dev/ttyACM0', '/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2', '/dev/ttyACM3', '/dev/ttyACM4',
                     '/dev/ttyACM5', '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4',
                     '/dev/ttyUSB5', '/dev/ttyUSB6', '/dev/ttyUSB7', '/dev/ttyUSB8', '/dev/ttyUSB9', '/dev/ttyUSB10',
                     '/dev/ttyS0', '/dev/ttyS1', '/dev/ttyS2', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8',
                     'com9', 'com10', 'com11', 'com12', 'com13', 'com14', 'com15', 'com16', 'com17', 'com18', 'com19',
                     'com20', 'com21', 'com1', 'end'
                     ]
        detected = None
        for device in locations:
            try:
                serialport = serial.Serial(device, 57600, timeout=0)
                detected = device
                serialport.close()
                break
            except serial.SerialException:
                if device == 'end':
                    print('Unable to find Serial Port, Please plug in cable or check cable connections.')
                    detected = None
                    exit()
        print('{}{}\n'.format("Using COM Port:", detected))
        return detected

    # noinspection PyMethodMayBeStatic
    def _format_capability_report(self, data):
        """
        This is a private utility method.
        This method formats a capability report if the user wishes to send it to the console
        @param data: Capability report
        @return: None
        """
        pin_modes = {0: 'Digital_Input', 1: 'Digital_Output', 2: 'Analog', 3: 'PWM', 4: 'Servo',
                     5: 'Shift', 6: 'I2C', 7: 'One Wire', 8: 'Stepper', 9: 'Encoder'}
        x = 0
        pin = 0

        print('\nCapability Report')
        print('-----------------\n')
        while x < len(data):
            # get index of next end marker
            print('{} {}{}'.format('Pin', str(pin), ':'))
            while data[x] != 127:
                mode_str = ""
                pin_mode = pin_modes.get(data[x])
                mode_str += pin_mode
                x += 1
                bits = data[x]
                print('{:>5}{}{} {}'.format('  ', mode_str, ':', bits))
                x += 1
            x += 1
            pin += 1

    @asyncio.coroutine
    def _process_latching(self, key, latching_entry):
        """
        This is a private utility method.
        This method process latching events and either returns them via callback or stores them in the latch map
        @param key: Encoded pin
        @param latching_entry: a latch table entry
        @return: Callback or store data in latch map
        """
        if latching_entry[Constants.LATCH_CALLBACK]:
            # auto clear entry and execute the callback

            latching_entry[Constants.LATCH_CALLBACK]([key,
                                                      latching_entry[Constants.LATCHED_DATA],
                                                      time.time()])
            self.latch_map[key] = [0, 0, 0, 0, 0, None]
        else:
            updated_latch_entry = latching_entry
            updated_latch_entry[Constants.LATCH_STATE] = Constants.LATCH_LATCHED
            updated_latch_entry[Constants.LATCHED_DATA] = latching_entry[Constants.LATCHED_DATA]
            # time stamp it
            updated_latch_entry[Constants.LATCHED_TIME_STAMP] = time.time()
            self.latch_map[key] = updated_latch_entry

    @asyncio.coroutine
    def _send_command(self, command):
        """
        This is a private utility method.
        The method sends a non-sysex command to Firmata.
        @param command:  command data
        @return: length of data sent
        """
        send_message = ""
        for i in command:
            send_message += chr(i)
        result = None
        for data in send_message:
            try:
                result = yield from self.serial_port.write(data)
            except():
                print('cannot send command')
        return result

    @asyncio.coroutine
    def _send_sysex(self, sysex_command, sysex_data=None):
        """
        This is a private utility method.
        This method sends a sysex command to Firmata.

        @param sysex_command: sysex command
        @param sysex_data: data for command
        @return : No return value.
        """
        if not sysex_data:
            sysex_data = []

        # convert the message command and data to characters
        sysex_message = chr(PrivateConstants.START_SYSEX)
        sysex_message += chr(sysex_command)
        if len(sysex_data):
            for d in sysex_data:
                sysex_message += chr(d)
        sysex_message += chr(PrivateConstants.END_SYSEX)

        for data in sysex_message:
            yield from self.serial_port.write(data)

    @asyncio.coroutine
    def _wait_for_data(self, current_command, number_of_bytes):
        """
        This is a private utility method.
        This method accumulates the requested number of bytes and then returns the full command
        @param current_command:  command id
        @param number_of_bytes:  how many bytes to wait for
        @return: command
        """
        while number_of_bytes:
            next_command_byte = yield from self.serial_port.read()
            current_command.append(next_command_byte)
            number_of_bytes -= 1
            yield from asyncio.sleep(self.sleep_tune)
        return current_command


# noinspection PyUnusedLocal
def _signal_handler(the_signal, frame):
    """
    The 'Control-C' handler
    @param the_signal: signal
    @param frame: not used
    @return: never returns.
    """
    print('You pressed Ctrl+C!')
    # to get coverage data or profiling data the code using pymata_iot, uncomment out the following line
    # exit()
    try:
        loop = asyncio.get_event_loop()
        for t in asyncio.Task.all_tasks(loop):
            t.cancel()
        loop.run_until_complete(asyncio.sleep(.01))
        loop.close()
        loop.stop()
        # os._exit(0)
        sys.exit(0)
    except RuntimeError:
        # this suppresses the Event Loop Is Running message, which may be a bug in python 3.4.3
        # os._exit(1)
        sys.exit(1)


signal.signal(signal.SIGINT, _signal_handler)
signal.signal(signal.SIGTERM, _signal_handler)
signal.signal(signal.SIGALRM, _signal_handler)
