from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name="land_searcher",
    version="0.1.0",
    description="Scrape website and search the land for sale",
    author="Tatsuro Homma",
    author_email="thomma@emile-tech.com",
    url="private",
    packages=find_packages("land_searcher"),
    package_dir={"": "land_searcher"},
    py_modules=[splitext(basename(path))[0] for path in glob('land_searcher/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt'),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"]
)