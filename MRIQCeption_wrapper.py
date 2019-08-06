#!/usr/bin/env python
"""
Call this program with:
    -g full path to your group csv or tsv you want to compare to API data.)
    -t scan type (modality) to compare to: bold, T1w, or T2w)
    -? filter/search phrase - argument in unknown format...
__authors__ = [Elizabeth C. Beard, Stephanie Rossi Chen,Stephanie N. DeCross,
               Damion V. Demeter, Sofía Fernández-Lozano, Chris Foulon,
               Helena M. Gellersen, Estée Rubien-Thomas, Saren H. Seeley,
               Catherine R. Walsh]
__version__ = '0.01'
__maintainer__ = '??'
__email__ = '??@??.edu'
__status__ = 'pre-alpha'
"""

import argparse,datetime,os,sys,time
from tools import load_groupfile, query_api, scatter

#################################################
##             MAIN SCRIPT ENTRY               ##
#################################################

here = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
PROG = 'QCeption'
prog_desc = """%(prog)s:
A utility for doing QC, on your group QC report, using the MRIQC "global" data. Originally written \
during Neurohackademy, 2019.
""" % {'prog': PROG}


def main(argv=sys.argv):
    arg_parser = argparse.ArgumentParser(description=prog_desc,
                                         formatter_class=
                                         argparse.ArgumentDefaultsHelpFormatter)
    # Check for arguments. #
    if len(sys.argv[1:]) == 0:
        print('\nArguments required. Use -h option to print FULL usage.\n')

    arg_parser.add_argument('-g', metavar='GROUP_FILE', action='store',
                            type=os.path.abspath, required=True,
                            help=('FULL path to your group csv/tsv file - '
                                  'the output from MRIQC.'),
                            dest='group_file'
                            )
    arg_parser.add_argument('-s', metavar='SEARCH_PHRASE', action='store', type=str,
                            required=True, help=('Search phrase to filter API query.'
                                                 'Format: xxxx xxxxx xxxxxx xxxxxx'),
                            dest='search_phrase'
                            )
    arg_parser.add_argument('-t', metavar='SCAN_TYPE', action='store', type=str,
                            choices=['bold', 'T1w', 'T2w'], required=False,
                            default='T1w',
                            help=('Scan type to query. Can choose from bold,'
                                  ' T1w, or T2w.'),
                            dest='scan_type'
                            )
    args = arg_parser.parse_args()

    #################################################
    ## Script Argument Verification and Assignment ##
    #################################################
    if os.path.isfile(args.group_file):
        pass
    else:
        print('The groupfile you are trying to use was not found. Exiting...')
        sys.exit()

    #################################################
    ##          Global Variable Assignment         ##
    #################################################    
    start_time = time.time()
    time.sleep(1)
    today_date = datetime.datetime.now().strftime('%m%d%Y')

    print('Querying API for ' + args.scan_type + ' scans.')

    ## GROUP FILE COULD TURN INTO A LIST OF FILES!!! Just need a way to keep track and name them...perhaps turn it into a tuple 
    ## of (name,path) or maybe even a key: val?
    ## Check that this dataframe is the same format as the result_df output from the query_api function!!
    loaded_df = load_groupfile(args.group_file)

    # result_df = query_api(args.scan_type,'MultibandAccelerationFactor>3','RepetitionTime>1')
    # result_df = query_api(args.scan_type, ['MultibandAccelerationFactor>3', 'EchoTime>1'])
    result_df = query_api(args.scan_type, 'MultibandAccelerationFactor>3&EchoTime>1')

    ## Scater plot/visualization functions would go below here and pass result_df as well as loaded_df pandas dataframes
    # something like this:
    # scatter(loaded_df, result_df)


    full_runtime = time.time() - start_time
    print('\nFull Script Runtime: ', datetime.timedelta(seconds=full_runtime), '\n')
if __name__ == '__main__':
    sys.exit(main())
