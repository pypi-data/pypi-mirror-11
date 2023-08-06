from setuptools import setup
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))


def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    assert str.startswith(version_match.group(1), '0.6')
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

with open(os.path.join(here, 'AUTHORS')) as f:
    authors = f.read()

with open(os.path.join(here, 'requirements.txt')) as f:
    requirements = f.read().split('\n')

assert isinstance(long_description, str), 'Error in long description {}'.format(long_description)
assert isinstance(authors, str), 'Error in authors {}'.format(authors)
assert isinstance(requirements, list), 'Error in requirements {}'.format(requirements)

setup(
    name="rep",
    version=find_version('rep', '__init__.py'),
    description="infrastructure for collaborative computational experiments on data",
    long_description="""Reproducible Experiment Platform is a collaborative software infrastructure for computational experiments on data, which allows obtaining reproducible, repeatable results and consistent comparison of the obtained results.""",
    url='https://github.com/yandex/rep',

    # Author details
    author=authors,
    author_email='axelr@yandex-team.ru, antares@yandex-team.ru',

    # Choose your license
    license='Apache-2.0 License',
    packages=['rep', 'rep.estimators', 'rep.data', 'rep.metaml', 'rep.report', 'rep.test'],
    package_dir={'rep': 'rep'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7 ',
        # 'Programming Language :: Python :: 3.4 ',

    ],

    # What does your project relate to?
    keywords='machine learning, ydf, high energy physics, particle physics, data analysis, reproducible experiment',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages.
    # packages=find_packages(exclude=["cern_utils", "docs", "tests*"]),

    # List run-time dependencies here. These will be installed by pip when your
    # project is installed.

    install_requires=requirements,

    # ["numpy >= 1.9.0",
    #                   "scipy >= 0.14.0",
    #                   "ipython[all] == 3.2.0",
    #                   "pyzmq == 14.3.1",
    #                   "matplotlib == 1.3.1",
    #                   "openpyxl < 2.0.0",
    #                   "pandas == 0.14.0",
    #                   "requests[security] >= 2.5.1",
    #                   "Jinja2 >= 2.7.3",
    #                   "numexpr >= 2.4",
    #                   "plotly == 1.2.3",
    #                   "scikit-learn == 0.16.1",
    #                   "bokeh == 0.8.1",
    #                   "mpld3 == 0.2",
    #                   "neurolab == 0.3.5",
    #                   "theanets == 0.5.2",
    #                   "pybrain == 0.3",
    # ],

    # If there are data files included in your packages that need to be
    # installed, specify them here. If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    # 'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    #entry_points={
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},
)
