from distutils.core import setup
setup(
    name='pyIDS',
    packages=['pyIDS'],
    version='0.1.1',
    description='Python wrapper for the IDS(IBM Bluemix Devops Services) API',
    author='James Royal',
    author_email='jhr.atx@gmail.com',
    url='https://github.com/jroyal/pyIDS',
    download_url='https://github.com/jroyal/pyIDS/tarball/0.1.1',
    install_requires=[
        "requests",
        "xmltodict",
    ],
    keywords=[],
    classifiers=[],
)