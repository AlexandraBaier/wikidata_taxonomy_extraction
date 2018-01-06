# wikidata_taxonomy_extraction

Script to extract Wikidata's taxonomy and corresponding class objects from JSON dump.

JSON dumps are available at [https://dumps.wikimedia.org/wikidatawiki/entities/](https://dumps.wikimedia.org/wikidatawiki/entities/).

Any dump formats as provided by Wikidata can be used as  input.
Specifically this means ``.bz2``, ``.gz`` or uncompressed/plain ``.json`` are legal file formats.

Due to large file size, file compression and no parallel processes the runtime of the script is very high.
For example: On my local machine, taxonomy extraction of the 20th Nov. 2017 dataset (.bz2) had a runtime of approx. 18 hours with ``-f`` and ``-v`` flag.

Running the script in parallel on subsets of the dump and then merging the resulting taxonomies is a good idea.

## Taxonomy in Wikidata

A taxonomy is a directed acyclic graph (DAG) with classes (concepts) as vertices and subclass-of relations as edges.
In Wikidata, the subclass-of relation is the property [subclass-of (P279)](https://www.wikidata.org/wiki/Property:P279).
This tool identifies classes with the following rule:

A Wikidata entity *X* is a class, if it is an item (ID starts with Q) and at least one of the following statements is fulfilled:
* *X* is a subclass iff *X* has at least one statement with property P279
* *X* is a superclass iff there exists a class *Y*, which has a statement with property P279 and value *Y*
* *X* has instances iff there exists an item *Y*, which has a statement with property P31 and value *X* 

## Installation

``pip install git+https://github.com/AlexBaier/wikidata_taxonomy_extraction.git``

## Script
usage: ``extract-wd-taxonomy [-h] [-f] [-v] dump``

positional arguments:
  * ``dump``    &nbsp;&nbsp;  Path to Wikidata JSON dump.

optional arguments:
  * ``-h``, ``--help``     &nbsp;&nbsp; Show help message
  * ``-f``, ``--full``     &nbsp;&nbsp; Additionally extract class objects. Requires second read of dump.
  * ``-v``, ``--verbose``  &nbsp;&nbsp; Prints progress log to stdout.
  
output:

Given dump path ``path/to/dump.json.bz2``, the following files are generated:

* ``path/to/dump.nodes.taxonomy.csv``: Nodes, Table with one column ``class``
* ``path/to/dump.edges.taxonomy.csv``: Edges, Table with columns ``subclass`` and ``superclass``
* if ``-f`` then ``.classes.taxonomy.jsonl``: Wikidata JSON objects of each class (correspond to IDs in Nodes table)