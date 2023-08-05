
import io
import os.path
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytrends',
    version='1.0.1',
    description='Pseudo API for Google Trends',
    long_description=long_description,
    url='https://github.com/dreyco676/pytrends',
    author=['John Hogue', 'Burton DeWilde'],
    author_email='dreyco676@gmail.com', #TODO add burton's email
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License'
        ],
    install_requires=["fake_useragent"],
    keywords='google trends api search',
    packages=['pytrends'],
)
