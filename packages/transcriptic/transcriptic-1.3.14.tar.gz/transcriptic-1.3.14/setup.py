from setuptools import setup

setup(
    name='transcriptic',
    version='1.3.14',
    py_modules=['transcriptic', 'ap2en'],
    install_requires=[
        'Click>=5.1',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        transcriptic=transcriptic:cli
    ''',
)
