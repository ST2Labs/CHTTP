#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CHTTP.py

Copyright 2015 Julian J. Gonzalez
www.st2labs.com | @ST2Labs | @rhodius | @seguridadxato2

This is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

This is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along it; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import sys
import argparse
import requests

ControlTable = {"Joomla": False,
                "Wordpress": False,
                "Drupal": False
            }


def serverInfo(req1):
    r = req1
    try:
        srv = r.headers["Server"]
        pwd = r.headers["X-Powered-By"]
        return srv, pwd
    except:
        return srv


def cms_version(req1):

    r = req1
    try:
        ver = r.headers["X-Generator"]
        return ver
    except:
        return """
            Sorry but your Server
            is protected and doesn't show
            CMS Version
            """


def showHTTPHead(req1):
    return req1.headers


def showResult(ver):

    if ControlTable["Joomla"] is True:
        print """
            Maybe this URL is a Joomla CMS with 25% accuracy
            """ + ver + "\n"
    elif ControlTable["Wordpress"] is True:
        print """
            Maybe this URL is a Worpress CMS with 25% accuracy
            """ + ver + "\n"
    elif ControlTable["Drupal"] is True:
        print """
            Maybe this URL is a Drupal CMS with 25% accuracy
            """ + ver + "\n"
    else:
        print """
            No CMS detected or I can't find out it!!!
            Please, Use other Open Source Free tools like whatWeb
            """


def getHTTPHead(myurl):
    return requests.head(myurl)


def cms_Wordpress_detect(req1):

    r = req1
    #verbs = requests.options(r.url)
    #print(verbs.headers['allow'])
    try:
        if r.headers['X-Pingback']:
            ControlTable["Wordpress"] = True
    except:
            ControlTable["Wordpress"] = False


def cms_Drupal_detect(req1):

    r = req1
    try:
        XDrupal = r.headers['X-Drupal-Cache']
        if XDrupal != "x-drupal-cache":
            ControlTable["Drupal"] = True
    except:
            ControlTable["Drupal"] = False


def cms_Joomla_detect(req1):

    JoomlaP3P = 'CP="NOI ADM DEV PSAi COM NAV OUR OTRo STP IND DEM"'
    r = req1
    try:
        if r.headers['P3P'] == JoomlaP3P:
            ControlTable["Joomla"] = True
    except:
            ControlTable["Joomla"] = False


def usage():

    print '''

        _______  __   __  _______  _______  _______ ..
        |       ||  | |  ||       ||       ||       |.
        |       ||  |_|  ||_     _||_     _||    _  |.
        |       ||       |  |   |    |   |  |   |_| |.
        |      _||       |  |   |    |   |  |    ___|.
        |     |_ |   _   |  |   |    |   |  |   |    .
        |_______||__| |__|  |___|    |___|  |___|    .


        CMS HTTP DETECTION- BASED ON HEADERS INFORMATION

        ST2Labs 2014/2015
        @Autor: Julian J. Gonzalez
        @ST2Labs / @rhodius / @seguridadxato2

        ST2Labs
        www.seguridadparatodos.es / www.st2labs.com

        CHTTP.py [Options]

            -h --help
                Show this MENU info
            -d --host
                URL of host to get HTTP HEADERS INFO
                This arguments is a valid URL with http://
            -H, --head
                Show HTTP Header using HEAD Method
            -i, --info
                Show HTTP Server Info()

        Example:

            CHTTP.py -d http://www.example.com
            CHTTP.py -i -d http://www.example.com
            CHHTP.py -H -d http://www.example.com
    '''


def main(argv):

    host = ''

    try:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=
            """
        _______  __   __  _______  _______  _______ ..
        |       ||  | |  ||       ||       ||       |.
        |       ||  |_|  ||_     _||_     _||    _  |.
        |       ||       |  |   |    |   |  |   |_| |.
        |      _||       |  |   |    |   |  |    ___|.
        |     |_ |   _   |  |   |    |   |  |   |    .
        |_______||__| |__|  |___|    |___|  |___|    .

        CMS HTTP DETECTION - BASED ON HEADERS INFORMATION
        """)

        parser.add_argument('-c', '--cms',
                            help='Show CMS Version Info()',
                            action="store_true")
        parser.add_argument('-i', '--info',
                            help='Show HTTP Server Info()',
                            action="store_true")
        parser.add_argument('-d', '--host',
                            help='''URL of host to get HTTP HEADERS INFO
                            This arguments is a valid URL with http://''',
                            required=True)
        parser.add_argument('-H', '--head',
                            help='Show HTTP Header using HEAD Method',
                             action="store_true")

        args = parser.parse_args()

        host = args.host
        r = getHTTPHead(host)

        if args.cms is True:

            cms_Joomla_detect(r)
            cms_Wordpress_detect(r)
            cms_Drupal_detect(r)
            v = cms_version(r)
            showResult(v)

        if args.info is True:
            try:
                s = serverInfo(r)
                print """     SERVIDOR: """ + s
            except:
                print """     SERVIDOR: """ + s[0]
                print """     POWERRED-BY: """ + s[1]

        if args.head is True:
            hh = showHTTPHead(r)
            for name, value in hh.items():
                print """
        """ + name.upper() + ": " + value

    except Exception:
        print Exception
        usage()
        sys.exit(2)

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            main(sys.argv[1:])
        else:
            usage()
    except Exception, e:
        print "Error: %s" % e
