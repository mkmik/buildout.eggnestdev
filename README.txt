buildout.eggnest
=================


The problem
-----------
It is very convenient to install functionality to a buildout with just
a couple of lines, but for those used to Zope 2, one might miss
the way of adding a piece of functionality by just dropping something
(i.e. a product) into a folder. This could be good for people who want to try
out things without worrying about editing a configuration file with
lots of directives in it.
When wanting to install a new egg using buildout you currently have to
edit the buildout configuration file(s) and add a couple of lines in 
the right places. What if you could just drop a file in a folder instead?

Solution
--------
Make a buildout extension so that the only thing you need to do in order to install an egg
is to take a simple text file, and drop it in a certain directory. When you rerun buildout the
contents of that file is parsed, the specified egg is downloaded and added to the instance.

When ``buildout.eggnest`` is run it::

  1. If ``eggnest-src-directory`` is not given the default directory ``src``
     is scanned.  
  
  2. Adds the egg to the ``eggs`` and ``zcml`` option to a set of given buildout parts.

This steps are done on the fly when running buildout. So I can add/delete/rename
an egg and it will be picked up.

NOTE: The extension does not write to the buildout's configuration file.

buildout.eggnest options
-------------------------

eggnest-src-directory:
 Specified to the directory that your egg install files should be placed.
 Defaults to src. An idea could be
 to have a dedicated directory called "eggnest".
				
eggnest-parts:
 What part of your buildout config that the eggs should be added to. *required*	

eggnest-verbose:
 Set this to ``true`` to get more information. 
 Not really that much right now but a little bit more at least.


How to use it
-------------

To use ``buildout.eggnest`` you need to add the following to your buildout.cfg::

  [buildout]
  extensions = 
    buildout.eggnest

  eggnest-parts = 
    instance

In ``eggnest-parts`` you need to specify what buildout part that the eggs should be added to. 
By default the ``src`` directory is scanned for egg specification files. 


eggs specification files for eggnest
------------------------------------

The egg install specification files should have this structure. This is the same as the normal buildout config format.::

  [eggnest]
  egg = 
    plone.introspector
  
  zcml = 
    plone.introspector
	
``zcml`` can be multiple lines if additional slugs need to be specified.

If the egg is in the ``Products`` namespace the zcml is not needed in the specification file.::

  [eggnest]
  egg = 
    Products.DocFinderTab



buildout.eggnest was created by Martin Lundwall <martin@webworks.se> after an 
initial idea by Jorgen Modin <jorgen@webworks.se>
