"""
The inputs.py module represents some form of all inputs
to the Automater program to include target files, and
the standard config file - sites.xml. Any addition to
Automater that brings any other input requirement should
be programmed in this module.
Class(es):
TargetFile -- Provides a representation of a file containing target
              strings for Automater to utilize.
SitesFile -- Provides a representation of the sites.xml
             configuration file.
              
Function(s):
No global exportable functions are defined.
Exception(s):
No exceptions exported.
"""
import os
import hashlib
import requests
from outputs import SiteDetailOutput
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
import json

#__REMOTE_TEKD_XML_LOCATION__ = 'https://raw.githubusercontent.com/1aN0rmus/TekDefense-Automater/master/tekdefense.xml' #Update to mine
__TEKDEFENSEXML__ = 'tobdefense.json'

class TargetFile(object):
    """
    TargetFile provides a Class Method to retrieve information from a file-
    based target when one is entered as the first parameter to the program.
    
    Public Method(s):
    (Class Method) TargetList
    
    Instance variable(s):
    No instance variables.
    """

    @classmethod
    def TargetList(self, filename, verbose):
        """
        Opens a file for reading.
        Returns each string from each line of a single or multi-line file.
        
        Argument(s):
        filename -- string based name of the file that will be retrieved and parsed.
        verbose -- boolean value representing whether output will be printed to stdout
        Return value(s):
        Iterator of string(s) found in a single or multi-line file.
        
        Restriction(s):
        This Method is tagged as a Class Method
        """
        try:
            target = ''
            with open(filename) as f:
                li = f.readlines()
                for i in li:
                    target = str(i).strip()
                    yield target
        except IOError:
            SiteDetailOutput.PrintStandardOutput('There was an error reading from the target input file.',
                                                 verbose=verbose)

class SitesFile(object):
    """
    SitesFile represents an JSON object representing the
    program's configuration file. Returns DICT object. The tobdefense.json file is hosted on tobias1012's
    github
    
    Method(s):
    (Class Method) getJSONObject
    (Class Method) fileExists
    
    Instance variable(s):
    No instance variables.
    """

    @classmethod
    def getJSONObject(cls, filename: str, verbose) -> dict:
        """
        Opens a config file for reading.
        Returns DICT object representing JSON Config file.
        
        Argument(s):
        No arguments are required.
        
        Return value(s):
        ElementTree
        
        Restrictions:
        File must be named sites.xml and must be in same directory as caller.
        This Method is tagged as a Class Method
        """
        if SitesFile.fileExists(filename):
            try:
                with open(filename) as f:
                    conf = json.load(f)
                    return conf
            except Exception:
                SiteDetailOutput.PrintStandardOutput('There was an error reading from the {conffile} input file.\n'
                                                     'Please check that the {conffile} file is present and correctly '
                                                     'formatted.'.format(conffile=filename), verbose=verbose)
        else:
            SiteDetailOutput.PrintStandardOutput('No local {conffile} file present.'.format(conffile=filename),
                                                 verbose=verbose)
        return None

    @classmethod
    def fileExists(cls, filename):
        """
        Checks if a file exists. Returns boolean representing if file exists.
        
        Argument(s):
        No arguments are required.
        
        Return value(s):
        Boolean
        
        Restrictions:
        File must be in same directory as caller.
        This Method is tagged as a Class Method
        """
        return os.path.exists(filename) and os.path.isfile(filename)
