from setuptools import setup, find_packages
from setuptools.command.install import install

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        import src.first_time_setup
        src.first_time_setup.write_to_config_file()

setup(
    name='oops-gpt',
    version='0.0.1',
    description='Analyzes your previous terminal output with a LLM to suggest follow up commands, summarize output, fix errors, and more.',
    author='Sam Kececi',
    author_email='sam.kececi@gmail.com',
    url='http://github.com/skececi/oops-gpt',
    packages=find_packages(),
    install_requires=requirements,
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'oops = src.main:main', 
        ],
    },
)