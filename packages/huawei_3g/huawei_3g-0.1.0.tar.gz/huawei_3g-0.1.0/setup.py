from distutils.core import setup, Command


def discover_and_run_tests():
    import os
    import sys
    import unittest

    # get setup.py directory
    setup_file = sys.modules['__main__'].__file__
    setup_dir = os.path.abspath(os.path.dirname(setup_file))

    # use the default shared TestLoader instance
    test_loader = unittest.defaultTestLoader

    # use the basic test runner that outputs to sys.stderr
    test_runner = unittest.TextTestRunner()

    # automatically discover all tests
    # NOTE: only works for python 2.7 and later
    test_suite = test_loader.discover(setup_dir)

    # run the test suite
    test_runner.run(test_suite)


class DiscoverTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        discover_and_run_tests()


setup(
    name='huawei_3g',
    version='0.1.0',
    packages=['huawei_3g'],
    url='https://github.com/MartijnBraam/huawei-3g',
    license='MIT',
    author='Martijn Braam',
    author_email='martijn@brixit.nl',
    description='Python module for controlling huawei 3g usb modems',
    cmdclass={'test': DiscoverTest},
)