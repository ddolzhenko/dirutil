from setuptools import setup, find_packages


setup(

    name         = 'dirutil',
    version      = '0.1',

    description  = 'High level directory utilities',
    keywords     = ['dir', 'directory', 'workdir', 'tempdir'],

    author       = 'Dmitri Dolzhenko',
    author_email = 'd.dolzhenko@gmail.com',

    packages     = find_packages(),
    test_suite   = 'dirutil.get_tests',

    url          = 'https://github.com/ddolzhenko/dirutil',
    download_url = 'https://github.com/ddolzhenko/dirutil/archive/0.1.tar.gz',

    classifiers  = [],
    install_requires = [
        "checksumdir==1.0.5",
    ],
)

