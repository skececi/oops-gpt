from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        import first_time_setup
        first_time_setup.write_to_config_file()

setup(
    name='oops-ai',
    version='0.0.1',
    description='My cool Python script',
    author='Sam Kececi',
    author_email='sam.kececi@gmail.com',
    url='http://github.com/skececi/oops-ai',
    scripts=['main.py'],
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'oops = main:main',  # this means when `oops` is typed in the command line, the `main` function of `main.py` will be called
        ],
    },
)