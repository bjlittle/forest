import os
import re
import setuptools


def find_version():
    path = os.path.join(os.path.dirname(__file__), "forest", "__init__.py")
    with open(path) as stream:
        contents = stream.read()
    match = re.search(r"^__version__ = ['\"']([0-9\.]*)['\"']", contents, re.MULTILINE)
    if match:
        return match.group(1)
    else:
        raise RuntimeError("Unable to find version number")


setuptools.setup(
        name="forest",
        version=find_version(),
        author="Andrew Ryan",
        author_email="andrew.ryan@metoffice.gov.uk",
        description="Forecast visualisation and survey tool",
        packages=setuptools.find_packages(),
        entry_points={
            'console_scripts': [
                'forest=forest.cli.main:main',
                'forestdb=forest.db.main:main'
            ]
        })
