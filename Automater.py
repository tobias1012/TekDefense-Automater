"""
// Tobias - this is stolen from original
The Automater.py module defines the main() function for Automater.
Parameter Required is:
target -- List one IP Address (CIDR or dash notation accepted), URL or Hash
to query or pass the filename of a file containing IP Address info, URL or
Hash to query each separated by a newline.
Optional Parameters are:
-o, --output -- This option will output the results to a file.
-b, --bot -- This option will output minimized results for a bot.
-f, --cef -- This option will output the results to a CEF formatted file.
-w, --web -- This option will output the results to an HTML file.
-c, --csv -- This option will output the results to a CSV file.
-d, --delay -- Change the delay to the inputted seconds. Default is 2.
-s, --source -- Will only run the target against a specific source engine
to pull associated domains. Options are defined in the name attribute of
the site element in the XML configuration file. This can be a list of names separated by a semicolon.
--proxy -- This option will set a proxy (eg. proxy.example.com:8080)
-a --useragent -- Will set a user-agent string in the header of a web request.
is set by default to Automater/version#
-V, --vercheck -- This option checks and reports versioning for Automater. Checks each python
module in the Automater scope.  Default, (no -V) is False
-r, --refreshxml -- This option refreshes the tekdefense.xml file from the remote GitHub site.
Default (no -r) is False.
-v, --verbose -- This option prints messages to the screen. Default (no -v) is False.
Class(es):
No classes are defined in this module.
Function(s):
main -- Provides the instantiation point for Automater.
Exception(s):
No exceptions exported.
"""

import sys
from utilities import Parser, IPWrapper
from outputs import SiteDetailOutput
from inputs import TargetFile


__VERSION__ = "1.0"

def main():
    """
    Serves as the instantiation point to start Automater.
    Argument(s):
    No arguments are required.
    Return value(s):
    Nothing is returned from this Method.
    Restriction(s):
    The Method has no restrictions.
    """

    sites = []
    parser = Parser('IP, URL, and Hash Passive Analysis tool', __VERSION__)

    # if no target run and print help
    if not parser.hasTarget():
        print('[!] No argument given.')
        parser.print_help()  # need to fix this. Will later
        sys.exit()

    sourcelist = ['allsources']
    if parser.hasSource():
        sourcelist = parser.Source.split(';')

    # a file input capability provides a possibility of
    # multiple lines of targets
    targetlist = []
    if parser.hasInputFile():
        for tgtstr in TargetFile.TargetList(parser.InputFile, parser.Verbose):
            tgtstrstripped = tgtstr.replace('[.]', '.').replace('{.}', '.').replace('(.)', '.')
            if IPWrapper.isIPorIPList(tgtstrstripped):
                for targ in IPWrapper.getTarget(tgtstrstripped):
                    targetlist.append(targ)
            else:
                targetlist.append(tgtstrstripped)
    else:  # one target or list of range of targets added on console
        target = parser.Target
        tgtstrstripped = target.replace('[.]', '.').replace('{.}', '.').replace('(.)', '.')
        if IPWrapper.isIPorIPList(tgtstrstripped):
            for targ in IPWrapper.getTarget(tgtstrstripped):
                targetlist.append(targ)
        else:
            targetlist.append(tgtstrstripped)


if __name__ == "__main__":
    main()