from setuptools import setup, find_packages
import linguafilter

def get_readme_text():
    with open('README.rst') as f:
        return f.read()

setup(
    name = 'linguafilter',
    packages = find_packages(),
    install_requires = ['panflute'],
    version = linguafilter.VERSION,
    description = 'A pandoc filter adding support for various linguistics constructs',
    long_description = get_readme_text(),
    license = 'GPLv3',
    author = 'Ben Weedon',
    author_email = 'ben.weedon@outlook.com',
    url = 'https://github.com/benweedon/linguafilter',
    keywords = ['language', 'linguistics', 'pandoc', 'filter', 'conlang', 'conlangs'],
    classifiers = [
        'Development Status :: 3 - Alpha',

        'Environment :: Console',
        'Environment :: Plugins',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Topic :: Other/Nonlisted Topic',
    ],
    entry_points = {
        'console_scripts': [
            'linguafilter = linguafilter.main:main',
        ],
    },
)
