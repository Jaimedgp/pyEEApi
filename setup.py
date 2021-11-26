import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyeeapi",
    version="0.0.1",
    author="Jaimedgp",
    author_email="jaime.diez.gp@gmail.com",
    description="Python package to interact with the EEA API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='EEA, Air quality, API',
    # url="https://pypi.org/project/pyeeapi/",
    project_urls={
        "Source": "https://github.com/Jaimedgp/pyEEApi",
        "Bug Tracker": "https://github.com/Jaimedgp/pyEEApi/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "setuptools>=42",
        "wheel",
        "numpy",
        "pandas",
        "requests",
        "python-dateutil",
        "geocoder",
    ],
    packages=setuptools.find_packages(include=['pyeeapi']),
    python_requires=">=3.6",
    zip_safe=False,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    # test_suite='pyeeapi.tests',
)
