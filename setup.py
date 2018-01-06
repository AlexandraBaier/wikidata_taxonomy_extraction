import setuptools


def readme():
    with open('README.md') as f:
        return f.read()


setuptools.setup(
    name='wikidata_taxonomy_extraction',
    version='0.1',
    description='Script to extract Wikidata\'s taxonomy from Wikidata JSON dumps',
    long_description=readme(),
    url='',
    author='Alex Baier',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6'
    ],
    author_email='alx.baier@gmail.com',
    license='',
    packages=['wikidata_taxonomy_extraction'],
    zip_safe=False,
    install_requires=[
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': ['extract-wd-taxonomy=wikidata_taxonomy_extraction.__main__:main']
    }
)
