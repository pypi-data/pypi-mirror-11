from os import path

try:
    from setuptools import find_packages, setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import find_packages, setup


PWD = path.abspath(path.dirname(__file__))


def readfile(filename):
    try:
        with open(path.join(PWD, filename)) as f:
            return f.read()
    except (IOError, OSError):
        return ''


with open(path.join(PWD, 'requirements.txt')) as fp:
    install_reqs = [ir.strip() for ir in fp.readlines()]


setup(
    name='dju-intranet',
    description='Daejeon university intranet API',
    version='0.1.5',
    long_description=readfile('README.rst'),
    url='https://github.com/Kjwon15/dju-intranet',
    download_url='https://github.com/Kjwon15/dju-intranet/releases',
    author='Kjwon15',
    author_email='kjwonmail@gmail.com',
    packages=find_packages(),
    install_requires=install_reqs,
)
