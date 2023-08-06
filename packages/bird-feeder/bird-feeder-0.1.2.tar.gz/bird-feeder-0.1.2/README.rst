***********
Bird Feeder
***********

.. image:: https://travis-ci.org/bird-house/bird-feeder.svg?branch=master
   :alt: Travis Build

Bird Feeder (the bird)
    *Feed the Birds ...* 

Bird Feeder is parsing Thredds catalogs and local directories with ``NetCDF`` files and publishes metadata with download URLs to a Solr index service with a birdhouse schema.

Install from Anaconda
=====================

.. image:: https://anaconda.org/birdhouse/bird-feeder/badges/build.svg
   :alt: Anaconda Build

.. image:: https://anaconda.org/birdhouse/bird-feeder/badges/version.svg
   :alt: Anaconda Version

.. image:: https://anaconda.org/birdhouse/bird-feeder/badges/downloads.svg
   :alt: Anaconda Downloads

.. code-block:: sh

   $ conda install -c birdhouse bird-feeder



Install from GitHub
===================

.. code-block:: sh

   $ git clone https://github.com/bird-house/bird-feeder.git
   $ cd bird-feeder
   $ make install
   
Start Solr service on http://localhost:8983/solr/birdhouse:

.. code-block:: sh

   $ make start
   $ make status


Using the command line
======================

Help:

.. code-block:: sh

   $ birdfeeder -h 
   usage: birdfeeder [<options>] <command> [<args>]

   Feeds Solr with Datasets (NetCDF Format) from Thredds Catalogs and File
   System.

   optional arguments:
     -h, --help            show this help message and exit
     --debug               enable debug mode
     --service SERVICE     Solr URL. Default:
                           http://localhost:8983/solr/birdhouse
     --maxrecords MAXRECORDS
                           Maximum number of records to publish. Default: -1
                           (unlimited)
     --batch-size BATCH_SIZE
                           Batch size of records to publish. Default: 50000

   command:
     List of available commands

     {clear,from-thredds,from-directory}
                        Run "birdfeeder <command> -h" to get additional help.
       clear               Clears the complete solr index. Use with caution!
       from-thredds        Publish datasets from Thredds Catalog to Solr.
       from-directory      Publish NetCDF files from directory to Solr.


Parse a Thredds catalog (recursively until depth level 2):

.. code-block:: sh

   $ birdfeeder from-thredds --catalog-url http://example.com/thredds/catalog.xml --depth=2


Parse local NetCDF files:

.. code-block:: sh

   $ birdfeeder from-directory --start-dir /home/data/myarchive


