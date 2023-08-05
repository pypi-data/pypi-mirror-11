from setuptools import setup

setup(
    name='transcriptic',
    version='1.3.0',
    py_modules=['transcriptic'],
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        transcriptic=transcriptic:cli
    ''',
)
