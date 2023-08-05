# test script of types.py
__author__ = 'yuanchun'
import time
import os
from unittest import TestCase
from droidbot.types import Device, App, Intent


class DeviceTest(TestCase):
    """
    test the Device class,
    before testing, please make sure a emulator is started
    """
    def setUp(self):
        self.device = Device("emulator-5554")

    def tearDown(self):
        self.device.disconnect()
        self.device = None

    def test_init(self):
        self.assertTrue(self.device.is_connected)
        self.assertIsNotNone(self.device.get_display_info())

        device_real = Device("emulator-5554", is_emulator=False)
        self.assertTrue(device_real.is_connected)

    def test_connect(self):
        if self.device.is_emulator:
            self.assertIsNotNone(self.device.get_adb())
            self.assertIsNotNone(self.device.get_telnet())
            self.assertIsNotNone(self.device.get_view_client())
        else:
            self.assertIsNotNone(self.device.get_adb())
            self.assertIsNotNone(self.device.get_telnet())
        self.device.check_connectivity()
        self.device.disconnect()
        self.device.connect()
        self.assertTrue(self.device.is_connected)

    def test_is_foreground(self):
        settings_app = App(package_name="com.android.settings")
        no_app = App()
        self.device.get_adb().press('HOME')
        time.sleep(2)
        self.assertTrue(self.device.is_foreground(no_app))
        self.assertFalse(self.device.is_foreground(settings_app))

        self.device.start_app(settings_app)
        time.sleep(2)
        self.assertTrue(settings_app)
        self.assertFalse(self.device.is_foreground("com.android.unknown"))

    def test_add_contact(self):
        contact_data = {
            'name': 'Lynn',
            'phone': '1234567890'
        }
        r = self.device.add_contact(contact_data)
        self.assertTrue(r)

    def test_call(self):
        phone_num = "1234567890"

        r = self.device.call(phone_num)
        self.assertTrue(r)
        time.sleep(2)

        r = self.device.cancel_call(phone_num)
        self.assertTrue(r)
        time.sleep(2)

        r = self.device.receive_call(phone_num)
        self.assertTrue(r)
        time.sleep(2)

        r = self.device.accept_call(phone_num)
        self.assertTrue(r)
        time.sleep(2)

        r = self.device.cancel_call(phone_num)
        self.assertTrue(r)

    def test_sms(self):
        r = self.device.send_sms()
        self.assertTrue(r)

        r = self.device.receive_sms()
        self.assertTrue(r)

    def test_set_gps(self):
        r = self.device.set_gps(10, 10)
        self.assertTrue(r)

    def test_settings(self):
        self.device.change_settings(table_name='system', name='volume_system', value='10')
        self.assertEqual(self.device.get_settings()['system']['volume_system'], '10')
        self.device.change_settings(table_name='system', name='volume_system', value='20')
        self.assertEqual(self.device.get_settings()['system']['volume_system'], '20')


class AppTest(TestCase):
    """
    test the App class
    """
    def setUp(self):
        self.app = App(app_path="resources/DroidBoxTests.apk")

    def test_init(self):
        noapp = App()
        self.assertTrue(noapp.whole_device)

        app_with_file_path = self.app
        self.assertFalse(app_with_file_path.whole_device)
        self.assertEqual(app_with_file_path.get_package_name(), 'droidbox.tests')

    def test_get_package_name(self):
        package_name = self.app.get_package_name()
        self.assertEqual(package_name, "droidbox.tests")

    # useless function
    # def test_get_app_path(self):
    #     from droidbot.droidbot import DroidBot
    #     droidbot = DroidBot(device_serial="emulator-5554", package_name="com.android.settings")
    #     self.assertFalse(droidbot.app.whole_device)
    #     app_file_path = droidbot.app.pull_app_from_device(device=droidbot.device)
    #     self.assertIsNotNone(app_file_path)
    #     self.assertTrue(os.path.exists(app_file_path))
    #     droidbot.stop()

    def test_get_main_activity(self):
        main_activity = self.app.get_main_activity()
        self.assertEqual(main_activity, "droidbox.tests.DroidBoxTests")

    def test_get_possible_broadcasts(self):
        possible_broadcasts = self.app.get_possible_broadcasts()
        self.assertIsNotNone(possible_broadcasts)
        i = possible_broadcasts.pop()
        self.assertEqual(i.action, "android.provider.Telephony.SMS_RECEIVED")
