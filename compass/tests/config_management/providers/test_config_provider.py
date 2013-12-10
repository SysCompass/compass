import unittest2

from compass.config_management.providers import config_provider


class DummyProvider(config_provider.ConfigProvider):
    NAME = 'dummy'

    def __init__(self):
        pass


class Dummy2Provider(config_provider.ConfigProvider):
    NAME = 'dummy'

    def __init__(self):
        pass


class TestProviderRegisterFunctions(unittest2.TestCase):
    def setUp(self):
        config_provider.PROVIDERS = {}

    def tearDown(self):
        config_provider.PROVIDERS = {}

    def test_found_provider(self):
        config_provider.registerProvider(DummyProvider)
        provider = config_provider.getProviderByName(DummyProvider.NAME)
        self.assertIsInstance(provider, DummyProvider)

    def test_notfound_unregistered_provider(self):
        self.assertRaises(KeyError, config_provider.getProviderByName,
                          DummyProvider.NAME)

    def test_multi_registered_provider(self):
        config_provider.registerProvider(DummyProvider)
        self.assertRaises(KeyError, config_provider.registerProvider,
                          Dummy2Provider)


if __name__ == '__main__':
    unittest2.main()
