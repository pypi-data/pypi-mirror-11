# -*- coding: utf-8 -*-

#from ez_setup import use_setuptools
#use_setuptools()
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
import imp, os

# the following metadata part is stolen from:
# https://github.com/seanfisk/python-project-template

# Import metadata. Normally this would just be:
#
#     from doorpi import metadata
#
# However, when we do this, we also import `doorpi/__init__.py'. If this
# imports names from some other modules and these modules have third-party
# dependencies that need installing (which happens after this file is run), the
# script will crash. What we do instead is to load the metadata module by path
# instead, effectively side-stepping the dependency problem. Please make sure
# metadata has no dependencies, otherwise they will need to be added to
# the setup_requires keyword.
metadata = imp.load_source(
    'metadata', os.path.join('doorpi', 'metadata.py'))

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()

# See here for more options:
setup_dict = dict(
    license = metadata.license,
    name = metadata.package,
    version = metadata.version,
    author = metadata.authors[0],
    author_email = metadata.emails[0],
    maintainer = metadata.authors[0],
    maintainer_email = metadata.emails[0],
    url = metadata.url,
    keywords = metadata.keywords,
    description = metadata.description,
    long_description = read('README.md'),
    # Find a list of classifiers here:
    # <http://pypi.python.org/pypi?%3Aaction=list_classifiers>
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: Free for non-commercial use',
        'Natural Language :: German',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Software Distribution',
        'Topic :: Communications :: Internet Phone',
        'Topic :: Communications :: Telephony',
        'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
        'Topic :: Multimedia :: Video :: Capture',
        'Topic :: Multimedia :: Video :: Conversion',
        'Topic :: Security',
        'Topic :: System :: Emulators',
        'Topic :: System :: Filesystems',
        'Topic :: System :: Hardware',
        'Topic :: Utilities'
    ],
    packages = find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires = read('requires.txt').split('\n'),
    platforms = ["any"],
    #zip_safe = False,  # don't use eggs
    entry_points = {
        'console_scripts': [
            'doorpi_cli = doorpi.main:entry_point'
        ],
        # if you have a gui, use this
        # 'gui_scripts': [
        #     'doorpi_gui = doorpi.gui:entry_point'
        # ]
    }

# <http://pythonhosted.org/setuptools/setuptools.html>
)
def main():
    setup(**setup_dict)

if __name__ == '__main__':
    main()
