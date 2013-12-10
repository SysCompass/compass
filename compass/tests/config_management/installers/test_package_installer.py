import unittest2

from compass.config_management.installers import package_installer


class DummyInstaller(package_installer.Installer):
    NAME = 'dummy'

    def __init__(self):
        pass


class Dummy2Installer(package_installer.Installer):
    NAME = 'dummy'

    def __init__(self):
        pass


class TestInstallerFunctions(unittest2.TestCase):
    def setUp(self):
        package_installer.INSTALLERS = {}

    def tearDown(self):
        package_installer.INSTALLERS = {}

    def test_found_installer(self):
        package_installer.register(DummyInstaller)
        intaller = package_installer.getInstallerByName(DummyInstaller.NAME)
        self.assertIsInstance(intaller, DummyInstaller)

    def test_notfound_unregistered_installer(self):
        self.assertRaises(KeyError, package_installer.getInstallerByName,
                          DummyInstaller.NAME)

    def test_multi_registered_installer(self):
        package_installer.register(DummyInstaller)
        self.assertRaises(KeyError, package_installer.register,
                          Dummy2Installer)


if __name__ == '__main__':
    unittest2.main()
