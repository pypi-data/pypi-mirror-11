bioshake_device_python
======================

This Python package (bioshake\_device) creates a class named
BioshakeDevice, which contains an instance of
serial\_device2.SerialDevice and adds methods to it to interface to
Q.instruments BioShake devices.

Authors::

    Peter Polidoro <polidorop@janelia.hhmi.org>

License::

    BSD

Example Usage::

    from bioshake_device import BioshakeDevice
    dev = BioshakeDevice() # Automatically finds device if one available
    dev = BioshakeDevice('/dev/ttyUSB0') # Linux
    dev = BioshakeDevice('/dev/tty.usbmodem262471') # Mac OS X
    dev = BioshakeDevice('COM3') # Windows
    dev.get_description()
    dev.shake_on(speed_target=1000) # speed_target (rpm)
    dev.get_shake_actual_speed()
    dev.shake_off()
    dev.temp_on(temp_target=45) # temp_target (°C)
    dev.get_temp_actual()
    dev.temp_off()
    devs = BioshakeDevices()  # Automatically finds all available devices
    dev = devs[0]

