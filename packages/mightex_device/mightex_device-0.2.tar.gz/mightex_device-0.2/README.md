mightex_device_python
=====================

This Python package (mightex\_device) creates a class named MightexDevice,
which contains an instance of serial\_device2.SerialDevice and adds
methods to it to interface to Mightex LED controllers.

Authors:

    Peter Polidoro <polidorop@janelia.hhmi.org>

License:

    BSD

##Example Usage

```python
dev = MightexDevice() # Automatically finds device if one available
dev = MightexDevice('/dev/ttyUSB0') # Linux
dev = MightexDevice('/dev/tty.usbmodem262471') # Mac OS X
dev = MightexDevice('COM3') # Windows
```

```python
devs = MightexDevices()  # Automatically finds all available devices
```
