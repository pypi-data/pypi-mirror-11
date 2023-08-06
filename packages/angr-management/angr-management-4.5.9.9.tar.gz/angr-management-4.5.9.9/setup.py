from distutils.core import setup

setup(
    name='angr-management',
    version='4.5.9.9',
    packages=['angrmanagement', 'angrmanagement.ui', 'angrmanagement.data'],
    package_data={
        'angrmanagement.ui': ['*.enaml']
    },
    install_requires=[
        'angr',
        'enaml==0.9.8',
        'pygments',
        'websocket-client'
    ]
)
