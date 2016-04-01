'''
This is a template python script that has basic option parsing
and logging framework set up already. 

maintained by REndicott
'''

import logging
import sys
import inspect
import gc
import os
from optparse import OptionParser, OptionGroup

sversion = 'v0.1'
scriptfilename = os.path.basename(sys.argv[0])
defaultlogfilename = scriptfilename + '.log'



def setuplogging(loglevel,printtostdout,logfile):
    #pretty self explanatory. Takes options and sets up logging.
    print("starting up with loglevel",loglevel,logging.getLevelName(loglevel))
    logging.basicConfig(filename=logfile,
                        filemode='w',level=loglevel, 
                        format='%(asctime)s:%(levelname)s:%(message)s')
    if printtostdout:
        soh = logging.StreamHandler(sys.stdout)
        soh.setLevel(loglevel)
        logger = logging.getLogger()
        logger.addHandler(soh)

def main(options):
    ''' The main() method. Program starts here.
    '''
    # test the logging
    logging.info("%s : This is an INFO message" % thisFunctionName)
    logging.error("%s : This is an ERROR message" % thisFunctionName)
    logging.warning("%s : This is a WARNING message" % thisFunctionName)
    logging.critical("%s : This is a CRITICAL message" % thisFunctionName)
    logging.debug("%s : This is a DEBUG message" % thisFunctionName)

    try:
        print("I parsed the string '%s' as your desired samplefileoption" % options.samplefileoption)
    except Exception as ex:
        print("Exception processing samplefileoption: %s" % str(ex))

if __name__ == '__main__':
    '''This main section is mostly for parsing arguments to the 
    script and setting up debugging'''
    from optparse import OptionParser
    '''set up an additional option group just for debugging parameters'''
    from optparse import OptionGroup
    usage = ("%prog [--debug] [--printtostdout] [--logfile] [--version] [--help] [--samplefileoption]")
    #set up the parser object
    parser = OptionParser(usage, version='%prog ' + sversion)
    parser.add_option('-s','--samplefileoption', 
                    type='string',
                    metavar='FILE',
                    help=("This file is an optional argument to pass into the script"),default=None)
    parser.add_option('--sampleflag',
                    action='store_true',
                    help=("Boolean flag. If this option is present then options.sampleflag will be True"),
                    default=False)
    parser_debug = OptionGroup(parser,'Debug Options')
    parser_debug.add_option('-d','--debug',type='string',
        help=('Available levels are CRITICAL (3), ERROR (2), '
            'WARNING (1), INFO (0), DEBUG (-1)'),
        default='CRITICAL')
    parser_debug.add_option('-p','--printtostdout',action='store_true',
        default=False,help='Print all log messages to stdout')
    parser_debug.add_option('-l','--logfile',type='string',metavar='FILE',
        help=('Desired filename of log file output. Default '
            'is "'+ defaultlogfilename +'"')
        ,default=defaultlogfilename)
    #officially adds the debuggin option group
    parser.add_option_group(parser_debug) 
    options,args = parser.parse_args() #here's where the options get parsed

    try: #now try and get the debugging options
        loglevel = getattr(logging,options.debug)
    except AttributeError: #set the log level
        loglevel = {3:logging.CRITICAL,
                    2:logging.ERROR,
                    1:logging.WARNING,
                    0:logging.INFO,
                    -1:logging.DEBUG,
                    }[int(options.debug)]

    try:
        open(options.logfile,'w') #try and open the default log file
    except:
        print("Unable to open log file '%s' for writing." % options.logfile)
        logging.debug(
            "Unable to open log file '%s' for writing." % options.logfile)

    setuplogging(loglevel,options.printtostdout,options.logfile)

    main(options)