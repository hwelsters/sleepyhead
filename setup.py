from setuptools import find_packages
from setuptools import setup

description = """For doing data collection, analysis and research related to math / ChatGPT while sleeping 💤."""

setup(
    name='sleepyhead',
    version='1.0.1',
    description='A synthetic dataset of school-level mathematics questions',
    long_description=description,
    author='hwelsters',
    author_email='pending',
    license='Creative Commons Zero v1.0 Universal',
    keywords='mathematics dataset',
    url='Creative Commons Zero v1.0 Universal',
    packages=find_packages(),
    install_requires=[
        'revChatGPT==2.3.6',
        'pandas==1.5.2',
        'schedule==1.1.0',
        'sympy==1.11.1',
        'numpy==1.23.4'
    ],
    classifiers=[],
)
