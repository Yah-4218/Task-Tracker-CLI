from setuptools import setup, find_packages

setup(
    name='TaskTracker',
    description = 'A CLI task tracker',
    author = 'Yah4218',
    version='1.0.0',
    py_modules=['main'],
    install_requires=["tabulate"],
    entry_points={
        'console_scripts': [
            'track=main:main'
        ]
    }
)