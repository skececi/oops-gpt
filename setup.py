from setuptools import setup
from setuptools.command.install import install

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

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
    description='Analyzes your previous terminal output with a LLM to suggest follow up commands, summarize output, fix errors, and more.',
    author='Sam Kececi',
    author_email='sam.kececi@gmail.com',
    url='http://github.com/skececi/oops-ai',
    py_modules=['config', 'first_time_setup', 'main', 'gpt'],
    scripts=['main.py'],
    install_requires=requirements,
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'oops = main:main', 
        ],
    },
)