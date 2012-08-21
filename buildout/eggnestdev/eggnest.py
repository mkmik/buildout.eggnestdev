import os
import sys
import logging
from zc.buildout.buildout import _open
from ConfigParser import MissingSectionHeaderError

log = logging.getLogger('buildout.eggnest')


def get_eggs(src_dirs):
    """Creates a list of dictionaries with eggs to install.     
    """
    
    for directory in src_dirs:
        if os.path.isdir(directory):            
            for file in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, file)):
                    try:
                        content = _open(os.path.dirname(file),os.path.join(directory, file),[])
                    except MissingSectionHeaderError:
                        continue
                    except TypeError:
                        try:
                            # this is for compatibility with zc.buildout 1.4.0
                            content = _open(os.path.dirname(file),os.path.join(directory, file),[], 
                                                {}, {}, set())
                        except MissingSectionHeaderError:
                            continue
                    
                    if content.has_key('eggnest'):
                        yield content['eggnest']
        else:
            log.warning("%s is not a directory." % directory)
    
def add_egg_to_part(buildout, part, egg):
    """Add the egg to the eggs option of the part
    """

    if 'eggs' not in buildout[part]:
        buildout[part]['eggs'] = ''

    if egg not in buildout[part]['eggs']:
        if not buildout[part]['eggs'].endswith('\n'):
            buildout[part]['eggs'] += '\n'
        buildout[part]['eggs'] += egg
        # be nice and show message if verbose is on
        msg = "Added %s to the egg section of [%s]" % (egg, part)
        if buildout['buildout'].get('eggnest-verbose', None) in ['true','True']:
            log.info(msg)
        else:            
            log.debug(msg)

def add_develop(buildout, egg):
    """Add the egg to the develop option of the part
    """

    part = "buildout"

    if egg not in buildout[part]['develop']:
        if not buildout[part]['develop'].endswith('\n'):
            buildout[part]['develop'] += '\n'
        buildout[part]['develop'] += egg
        # be nice and show message if verbose is on
        msg = "Added %s to the develop section of [%s]" % (egg, part)
        if buildout['buildout'].get('eggnest-verbose', None) in ['true','True']:
            log.info(msg)
        else:
            log.debug(msg)
        
def add_zcml_to_part(buildout, part, zcmls):
    """Add all zcml entries to the part
    """
    
    if 'zcml' not in buildout[part]:
        buildout[part]['zcml'] = ''
        
    for zcml in zcmls.split('\n'):
        if zcml not in buildout[part]['zcml']:
            if not buildout[part]['zcml'].endswith('\n'):
                buildout[part]['zcml'] += '\n'
            buildout[part]['zcml'] +=  zcml
            # be nice and show message if verbose is on
            msg = "Added %s to the zcml section of [%s]" % (zcml, part)
            if buildout['buildout'].get('eggnest-verbose', None) in ['true','True']:
                log.info(msg)
            else:            
                log.debug(msg)
            
                      
def install(buildout=None):
    """o
    """
    if not buildout:
        return
    if 'eggnest-src-directory' in buildout['buildout']:
        src_dirs = buildout['buildout']['eggnest-src-directory'].split()
        if not src_dirs and buildout['buildout'].get('eggnest-verbose', None) in ['true','True']:
            log.warning("'eggnest-src-directory' option exist but no src directory was specified, please add one or more entries or remove the option to use the default directory 'src'.")
    elif os.path.exists('src'):
        src_dirs = ['src']
    else:
        return
    if 'eggnest-parts' in buildout['buildout']:
        buildout_parts = buildout['buildout']['eggnest-parts'].split()

        for egg_to_install in get_eggs(src_dirs):
            if 'develop' not in egg_to_install:
                continue

            # this is for compatibility with zc.buildout 1.4.0
            if type(egg_to_install['develop']) == tuple:
                egg_to_install['develop'] = egg_to_install['develop'][0]

            add_develop(buildout, egg_to_install['develop'])

        for part in buildout_parts:
            if part in buildout.keys():
                for egg_to_install in get_eggs(src_dirs):
                    # this is for compatibility with zc.buildout 1.4.0
                    if type(egg_to_install['egg']) == tuple:
                        egg_to_install['egg'] = egg_to_install['egg'][0]
                    egg_to_install['egg'] = egg_to_install['egg'].strip()
                    add_egg_to_part(buildout, part, egg_to_install['egg'])
                    if not egg_to_install['egg'].startswith('Products'):
                        if 'zcml' not in egg_to_install:
                            continue

                        # this is for compatibility with zc.buildout 1.4.0
                        if type(egg_to_install['zcml']) == tuple:
                            egg_to_install['zcml'] = egg_to_install['zcml'][0]
                        egg_to_install['zcml'] = egg_to_install['zcml'].strip()
                        add_zcml_to_part(buildout, part, egg_to_install['zcml'])
                    if buildout['buildout'].get('eggnest-verbose', None):
                        log.info('Added %s to the buildout part of %s' % (egg_to_install['egg'], part))
            else:
                log.critical("Unable to find part '%s' (maybe missspelled?)" % part)
    else:
        log.info("No part was specified with option 'eggnest-parts'")
