from metaknowledge.journalAbbreviations import abrevDBname

from setuptools import setup, find_packages
setup(name='metaknowledge',
    version='0.3.0',
    description = "A library for handling Web of science files",
    author="Reid McIlroy-Young, John McLevey",
    author_email = "rmcilroy@uwaterloo.ca",
    url="https://github.com/networks-lab/metaknowledge",
    download_url = "https://github.com/networks-lab/isilib/archive/0.3.tar.gz",
    keywords= 'isi wos testing',
    classifiers = [],
    install_requires= ['networkx'],
    #extras_require={'visualizer' : ['matplotlib']},
    packages=find_packages(),#['metaknowledge', 'metaknowledge.journalAbbreviations'],
    scripts=['metaknowledge/bin/metaknowledge-CLI'],
    test_suite='metaknowledge.tests',
    include_package_data = True,
    package_data = {'': [abrevDBname + '.*']}
    #data_files= [('/tests', ["testFile.isi", "OnePaper.isi", "ManyAuthors.isi"])]
)
