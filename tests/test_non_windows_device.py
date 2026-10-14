import unittest
from types import SimpleNamespace
from unittest.mock import patch

from module.device.device import Device
from module.device.connection import Connection
from module.device.env import IS_WINDOWS


@unittest.skipIf(IS_WINDOWS, 'Non-Windows MRO regression')
class NonWindowsDeviceTest(unittest.TestCase):
    def test_device_initializes_without_passing_config_to_object(self):
        config = SimpleNamespace(script=SimpleNamespace(device=SimpleNamespace(screenshot_method='ADB')))

        def connect(device, supplied_config):
            device.config = supplied_config
            device.serial = 'test-usb-device'

        with patch.object(Connection, '__init__', connect), patch.object(Device, 'screenshot_interval_set'):
            device = Device(config)
        self.assertIs(device.config, config)
        self.assertEqual(device.serial, 'test-usb-device')


if __name__ == '__main__':
    unittest.main()
