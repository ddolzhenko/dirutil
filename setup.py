from setuptools import setup, find_packages

ver = "0.4"

setup(

    name         = 'dirutil',
    version      = ver,

    description  = 'High level directory utilities',
    keywords     = ['dir', 'directory', 'workdir', 'tempdir'],

    author       = 'Dmitri Dolzhenko',
    author_email = 'd.dolzhenko@gmail.com',

    packages     = find_packages(),
    test_suite   = 'dirutil.get_tests',

    url          = 'https://github.com/ddolzhenko/dirutil',
    download_url = 'https://github.com/ddolzhenko/dirutil/archive/v{}.tar.gz'.format(ver),

    classifiers  = [],
    install_requires = [
        # "checksumdir==1.0.5",
    ],
)

