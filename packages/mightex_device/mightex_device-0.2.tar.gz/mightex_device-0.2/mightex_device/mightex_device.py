# -*- coding: utf-8 -*-
from __future__ import print_function, division
import serial
import time
import atexit
import platform
import os
from exceptions import Exception
import threading
import re

from serial_device2 import SerialDevice, SerialDevices, find_serial_device_ports, WriteFrequencyError

try:
    from pkg_resources import get_distribution, DistributionNotFound
    _dist = get_distribution('mightex_device')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'mightex_device')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except (ImportError,DistributionNotFound):
    __version__ = None
else:
    __version__ = _dist.version


DEBUG = False
BAUDRATE = 9600

class MightexError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MightexDevice(object):
    '''
    This Python package (mightex_device) creates a class named MightexDevice,
    which contains an instance of serial_device2.SerialDevice and adds
    methods to it to interface to Mightex LED controllers.

    Example Usage:

    dev = MightexDevice() # Automatically finds device if one available
    dev = MightexDevice('/dev/ttyUSB0') # Linux
    dev = MightexDevice('/dev/tty.usbmodem262471') # Mac OS X
    dev = MightexDevice('COM3') # Windows
    dev.get_serial_number()
    '04-150824-007'
    channel = 1
    dev.get_mode(channel)
    'disable'
    dev.set_normal_parameters(channel,1000,30)
    dev.get_normal_parameters(channel)
    {'current': 30, 'current_max': 1000}
    dev.set_mode_normal(channel)
    dev.set_normal_current(channel,200)
    dev.set_mode_disable(channel)
    dev.set_strobe_parameters(channel,100,1)
    dev.get_strobe_parameters(channel)
    {'current_max': 100, 'repeat': 1}
    dev.set_strobe_profile_set_point(channel,0,100,1000000)
    dev.set_strobe_profile_set_point(channel,1,10,500000)
    dev.get_strobe_profile(channel)
    [{'current': 100, 'duration': 1000000},
     {'current': 10, 'duration': 500000},
     {'current': 0, 'duration': 0}]
    dev.set_mode_strobe(channel)
    '''
    _TIMEOUT = 0.05
    _WRITE_WRITE_DELAY = 0.05
    _RESET_DELAY = 2.0

    def __init__(self,*args,**kwargs):
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        else:
            kwargs.update({'debug': DEBUG})
            self.debug = DEBUG
        kwargs['debug'] = False
        if 'try_ports' in kwargs:
            try_ports = kwargs.pop('try_ports')
        else:
            try_ports = None
        if 'baudrate' not in kwargs:
            kwargs.update({'baudrate': BAUDRATE})
        elif (kwargs['baudrate'] is None) or (str(kwargs['baudrate']).lower() == 'default'):
            kwargs.update({'baudrate': BAUDRATE})
        if 'timeout' not in kwargs:
            kwargs.update({'timeout': self._TIMEOUT})
        if 'write_write_delay' not in kwargs:
            kwargs.update({'write_write_delay': self._WRITE_WRITE_DELAY})
        if ('port' not in kwargs) or (kwargs['port'] is None):
            port =  find_mightex_device_port(baudrate=kwargs['baudrate'],
                                           try_ports=try_ports,
                                           debug=kwargs['debug'])
            kwargs.update({'port': port})

        t_start = time.time()
        self._serial_device = SerialDevice(*args,**kwargs)
        atexit.register(self._exit_mightex_device)
        time.sleep(self._RESET_DELAY)
        self._lock = threading.Lock()
        t_end = time.time()
        self._debug_print('Initialization time =', (t_end - t_start))

    def _debug_print(self, *args):
        if self.debug:
            print(*args)

    def _exit_mightex_device(self):
        pass

    def _args_to_request(self,*args):
        request = ' '.join(map(str,args))
        request = request + '\n\r';
        return request

    def _send_request(self,*args):
        '''
        Sends request to device over serial port and
        returns number of bytes written.
        '''
        self._lock.acquire()
        request = self._args_to_request(*args)
        self._debug_print('request', request)
        bytes_written = self._serial_device.write_check_freq(request,delay_write=True)
        self._lock.release()
        return bytes_written

    def _send_request_get_response(self,*args):
        '''
        Sends request to device over serial port and
        returns response.
        '''
        self._lock.acquire()
        request = self._args_to_request(*args)
        self._debug_print('request', request)
        response = self._serial_device.write_read(request,use_readline=True,check_write_freq=True)
        self._lock.release()
        response = response.strip()
        if '#!' in response:
            raise MightexError('The command is valid and executed, but an error occurred during execution.')
        elif '#?' in response:
            raise MightexError('The latest command is a valid command but the argument is NOT in valid range.')
        response = response.replace('#','')
        return response

    def close(self):
        '''
        Close the device serial port.
        '''
        self._serial_device.close()

    def get_port(self):
        return self._serial_device.port

    def get_device_info(self):
        '''
        Get device_info.
        '''
        request = self._args_to_request('DEVICEINFO')
        self._debug_print('request', request)
        response = self._send_request_get_response(request)
        if 'Mightex' not in response:
            raise MightexError('"Mightex" not in device_info.')
        return response

    def get_serial_number(self):
        '''
        Get serial_number.
        '''
        device_info = self.get_device_info()
        serial_number_str = 'Serial No.:'
        p = re.compile(serial_number_str+'\d+-?\d+-?\d+')
        found_list = p.findall(device_info)
        if len(found_list) != 1:
            raise MightexError('serial_number not found in device_info.')
        else:
            serial_number = found_list[0]
            serial_number = serial_number.replace(serial_number_str,'')
            return serial_number

    def get_mode(self,channel):
        '''
        Get channel mode. Modes = ['DISABLE','NORMAL','STROBE','TRIGGER']
        '''
        channel = int(channel)
        request = self._args_to_request('?MODE',channel)
        self._debug_print('request', request)
        response = self._send_request_get_response(request)
        if response == '0':
            return 'DISABLE'
        elif response == '1':
            return 'NORMAL'
        elif response == '2':
            return 'STROBE'
        elif response == '3':
            return 'TRIGGER'
        else:
            raise MightexError('Unknown response: {0}'.format(response))

    def set_mode_disable(self,channel):
        '''
        Set DISABLE mode.
        '''
        channel = int(channel)
        request = self._args_to_request('MODE',channel,0)
        self._debug_print('request', request)
        self._send_request(request)

    def set_mode_normal(self,channel):
        '''
        Set NORMAL mode.
        '''
        channel = int(channel)
        request = self._args_to_request('MODE',channel,1)
        self._debug_print('request', request)
        self._send_request(request)

    def set_mode_strobe(self,channel):
        '''
        Set STROBE mode.
        '''
        channel = int(channel)
        request = self._args_to_request('MODE',channel,2)
        self._debug_print('request', request)
        self._send_request(request)

    def set_mode_trigger(self,channel):
        '''
        Set TRIGGER mode.
        '''
        channel = int(channel)
        request = self._args_to_request('MODE',channel,3)
        self._debug_print('request', request)
        self._send_request(request)

    def set_normal_parameters(self,channel,current_max,current):
        '''
        Set NORMAL mode parameters. current_max is the maximum current
        allowed for NORMAL mode, in mA. current is the working current
        for NORMAL mode, in mA.
        '''
        channel = int(channel)
        current_max = int(current_max)
        current = int(current)
        request = self._args_to_request('NORMAL',channel,current_max,current)
        self._debug_print('request', request)
        self._send_request(request)

    def set_normal_current(self,channel,current):
        '''
        Set the working current for NORMAL mode, in mA.
        '''
        channel = int(channel)
        current = int(current)
        request = self._args_to_request('CURRENT',channel,current)
        self._debug_print('request', request)
        self._send_request(request)

    def get_normal_parameters(self,channel):
        '''
        Get NORMAL mode parameters. current_max is the maximum current
        allowed for NORMAL mode, in mA. current is the working current
        for NORMAL mode, in mA.
        '''
        channel = int(channel)
        request = self._args_to_request('?CURRENT',channel)
        self._debug_print('request', request)
        response = self._send_request_get_response(request)
        response_list = response.split(' ')
        parameters = {}
        parameters['current_max'] = int(response_list[-2])
        parameters['current'] = int(response_list[-1])
        return parameters

    def set_strobe_parameters(self,channel,current_max,repeat):
        '''
        Set STROBE mode parameters. current_max is the maximum current
        allowed for STROBE mode, in mA. repeat is the Repeat Count for
        running the profile. It can be from 0 to 99999999. And the
        number 9999 is special, it means repeat forever. Note that
        when it is 0, the programmed wave form will output once, when
        it is 1, the wave form will be repeated once, which will be
        output twice and so on.
        '''
        channel = int(channel)
        current_max = int(current_max)
        repeat = int(repeat)
        request = self._args_to_request('STROBE',channel,current_max,repeat)
        self._debug_print('request', request)
        self._send_request(request)

    def set_strobe_profile_set_point(self,channel,set_point,current,duration):
        '''
        Each channel has a programmable profile for STROBE mode. The
        profile contains 128 set_point values (0-127), and each
        set_point has current(mA)/duration(us) pair. A ZERO/ZERO pair
        means it is the end of the profile. If user does not program
        the profile for a certain channel, the default is all
        Zero/Zero pairs, which means the channel is always OFF. Use
        this method over and over to set a customized profile and
        then enter STROBE mode with the set_mode_strobe method. The
        profile will be executed (repeatedly) after device enters (or
        reenters) the STROBE mode.
        '''
        channel = int(channel)
        set_point = int(set_point)
        current = int(current)
        duration = int(duration)
        request = self._args_to_request('STRP',channel,set_point,current,duration)
        self._debug_print('request', request)
        self._send_request(request)

    def get_strobe_parameters(self,channel):
        '''
        Get STROBE mode parameters. current_max is the maximum current
        allowed for STROBE mode, in mA. repeat is the Repeat Count for
        running the profile. It can be from 0 to 99999999. And the
        number 9999 is special, it means repeat forever. Note that
        when it is 0, the programmed wave form will output once, when
        it is 1, the wave form will be repeated once, which will be
        output twice and so on.
        '''
        channel = int(channel)
        request = self._args_to_request('?STROBE',channel)
        self._debug_print('request', request)
        response = self._send_request_get_response(request)
        response_list = response.split(' ')
        parameters = {}
        parameters['current_max'] = int(response_list[0])
        parameters['repeat'] = int(response_list[1])
        return parameters

    def get_strobe_profile(self,channel):
        '''
        Each channel has a programmable profile for STROBE mode. The
        profile contains 128 set_point values (0-127), and each
        set_point has current(mA)/duration(us) pair. A ZERO/ZERO pair
        means it is the end of the profile. If user does not program
        the profile for a certain channel, the default is all
        Zero/Zero pairs, which means the channel is always OFF.
        '''
        request = self._args_to_request('?STRP',channel)
        self._debug_print('request', request)
        self._send_request(request)
        current = None
        duration = None
        profile = []
        while not ((current == 0) and (duration == 0)):
            response = self._serial_device.readline()
            response = response.strip()
            response = response.replace('#','')
            response_list = response.split(' ')
            self._debug_print('strobe_profile set_point',response_list)
            try:
                current = int(response_list[0])
                duration = int(response_list[1])
                profile_set_point = {}
                profile_set_point['current'] = current
                profile_set_point['duration'] = duration
                profile.append(profile_set_point)
            except:
                pass
        return profile


class MightexDevices(dict):
    '''
    MightexDevices inherits from dict and automatically populates it with
    MightexDevices on all available serial ports. Access each individual
    device with one key, the device serial_number. If you
    want to connect multiple MightexDevices with the same name at the
    same time, first make sure they have unique serial_numbers by
    connecting each device one by one and using the set_serial_number
    method on each device.
    Example Usage:
    devs = MightexDevices()  # Automatically finds all available devices
    devs.keys()
    dev = devs[serial_number]
    '''
    def __init__(self,*args,**kwargs):
        if ('use_ports' not in kwargs) or (kwargs['use_ports'] is None):
            mightex_device_ports = find_mightex_device_ports(*args,**kwargs)
        else:
            mightex_device_ports = use_ports

        for port in mightex_device_ports:
            kwargs.update({'port': port})
            self._add_device(*args,**kwargs)

    def _add_device(self,*args,**kwargs):
        dev = MightexDevice(*args,**kwargs)
        serial_number = dev.get_serial_number()
        self[serial_number] = dev


def find_mightex_device_ports(baudrate=None,
                            try_ports=None,
                            serial_number=None,
                            debug=DEBUG,
                            *args,
                            **kwargs):
    serial_device_ports = find_serial_device_ports(try_ports=try_ports, debug=debug)
    os_type = platform.system()
    if os_type == 'Darwin':
        serial_device_ports = [x for x in serial_device_ports if 'tty.usbmodem' in x or 'tty.usbserial' in x]

    mightex_device_ports = {}
    for port in serial_device_ports:
        try:
            dev = MightexDevice(port=port,baudrate=baudrate,debug=debug)
            try:
                s_n = dev.get_serial_number()
                if (serial_number is None) or (s_n == serial_number):
                    mightex_device_ports[port] = {'serial_number':s_n}
            except:
                continue
            dev.close()
        except (serial.SerialException, IOError):
            pass
    return mightex_device_ports

def find_mightex_device_port(baudrate=None,
                           try_ports=None,
                           serial_number=None,
                           debug=DEBUG):
    mightex_device_ports = find_mightex_device_ports(baudrate=baudrate,
                                                     try_ports=try_ports,
                                                     serial_number=serial_number,
                                                     debug=debug)
    if len(mightex_device_ports) == 1:
        return mightex_device_ports.keys()[0]
    elif len(mightex_device_ports) == 0:
        serial_device_ports = find_serial_device_ports(try_ports)
        err_string = 'Could not find any Mightex devices. Check connections and permissions.\n'
        err_string += 'Tried ports: ' + str(serial_device_ports)
        raise RuntimeError(err_string)
    else:
        err_string = 'Found more than one Mightex device. Specify port or serial_number.\n'
        err_string += 'Matching ports: ' + str(mightex_device_ports)
        raise RuntimeError(err_string)


# -----------------------------------------------------------------------------------------
if __name__ == '__main__':

    debug = False
    dev = MightexDevice(debug=debug)
