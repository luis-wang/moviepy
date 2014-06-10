# -*- coding: utf-8 -*-
import os
from distutils.core import setup

version='0.1.1'
README = os.path.join(os.path.dirname(__file__), 'README')
long_description = open(README).read() + '\n\n'

setup(
    name='wffmpeg',
    version=version,
    description=('wffmpeg is a wrapper to ffmpeg command line program, written in python. Is structured as a base library, easy to extend by combining standard ffmpeg features.'),
    long_description=long_description,
    classifiers=[
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Video',
    ],
    keywords='video ffmpeg convert libav encode decode transcode',
    author='leofiore',
    author_email='leofiore@gmail.com',
#    url='http://knivez.homelinux.org/pipeffmpeg/',
    url='https://github.com/kanryu/wffmpeg',
    license='LGPL',
    py_modules=['wffmpeg'],
)
