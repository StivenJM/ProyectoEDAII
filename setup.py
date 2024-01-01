from setuptools import setup 

setup(name='proyecto', version='1.0.0', packages=['proyecto'],
entry_points={
    'console_scripts': ['proyecto = proyecto.__main__:main']
})