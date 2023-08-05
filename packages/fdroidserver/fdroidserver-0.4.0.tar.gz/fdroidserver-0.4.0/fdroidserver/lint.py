#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# lint.py - part of the FDroid server tool
# Copyright (C) 2013-2014 Daniel Martí <mvdan@mvdan.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See th
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public Licen
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from optparse import OptionParser
import re
import logging
import common
import metadata
import sys
from collections import Counter
from sets import Set

config = None
options = None


def enforce_https(domain):
    return (re.compile(r'.*[^sS]://[^/]*' + re.escape(domain) + r'/.*'),
            domain + " URLs should always use https://")

https_enforcings = [
    enforce_https('github.com'),
    enforce_https('gitlab.com'),
    enforce_https('gitorious.org'),
    enforce_https('apache.org'),
    enforce_https('google.com'),
    enforce_https('svn.code.sf.net'),
    enforce_https('googlecode.com'),
]

http_warnings = https_enforcings + [
    (re.compile(r'.*github\.com/[^/]+/[^/]+\.git'),
     "Appending .git is not necessary"),
    # TODO enable in August 2015, when Google Code goes read-only
    # (re.compile(r'.*://code\.google\.com/.*'),
    #  "code.google.com will be soon switching down, perhaps the project moved to github.com?"),
]

regex_warnings = {
    'Web Site': http_warnings + [
    ],
    'Source Code': http_warnings + [
    ],
    'Repo': https_enforcings + [
    ],
    'Issue Tracker': http_warnings + [
        (re.compile(r'.*github\.com/[^/]+/[^/]+[/]*$'),
         "/issues is missing"),
    ],
    'Changelog': http_warnings + [
    ],
    'License': [
        (re.compile(r'^(|None|Unknown)$'),
         "No license specified"),
    ],
    'Summary': [
        (re.compile(r'^$'),
         "Summary yet to be filled"),
        (re.compile(r'.*\b(free software|open source)\b.*', re.IGNORECASE),
         "No need to specify that the app is Free Software"),
        (re.compile(r'.*((your|for).*android|android.*(app|device|client|port|version))', re.IGNORECASE),
         "No need to specify that the app is for Android"),
        (re.compile(r'.*[a-z0-9][.!?]( |$)'),
         "Punctuation should be avoided"),
    ],
    'Description': [
        (re.compile(r'^No description available$'),
         "Description yet to be filled"),
        (re.compile(r'\s*[*#][^ .]'),
         "Invalid bulleted list"),
        (re.compile(r'^\s'),
         "Unnecessary leading space"),
        (re.compile(r'.*\s$'),
         "Unnecessary trailing space"),
    ],
}

categories = Set([
    "Children",
    "Development",
    "Games",
    "Internet",
    "Multimedia",
    "Navigation",
    "Office",
    "Phone & SMS",
    "Reading",
    "Science & Education",
    "Security",
    "System",
    "Wallpaper",
])


def main():

    global config, options, curid, count
    curid = None

    count = Counter()

    def warn(message):
        global curid, count
        if curid:
            print "%s:" % curid
            curid = None
            count['app'] += 1
        print '    %s' % message
        count['warn'] += 1

    # Parse command line...
    parser = OptionParser(usage="Usage: %prog [options] [APPID [APPID ...]]")
    parser.add_option("-v", "--verbose", action="store_true", default=False,
                      help="Spew out even more information than normal")
    parser.add_option("-q", "--quiet", action="store_true", default=False,
                      help="Restrict output to warnings and errors")
    (options, args) = parser.parse_args()

    config = common.read_config(options)

    # Get all apps...
    allapps = metadata.read_metadata(xref=False)
    apps = common.read_app_args(args, allapps, False)

    for appid, app in apps.iteritems():
        if app['Disabled']:
            continue

        curid = appid
        count['app_total'] += 1

        curbuild = None
        for build in app['builds']:
            if not curbuild or int(build['vercode']) > int(curbuild['vercode']):
                curbuild = build

        # Incorrect UCM
        if (curbuild and curbuild['commit']
                and app['Update Check Mode'] == 'RepoManifest'
                and not curbuild['commit'].startswith('unknown')
                and curbuild['vercode'] == app['Current Version Code']
                and not curbuild['forcevercode']
                and any(s in curbuild['commit'] for s in '.,_-/')):
            warn("Last used commit '%s' looks like a tag, but Update Check Mode is '%s'" % (
                curbuild['commit'], app['Update Check Mode']))

        # Summary size limit
        summ_chars = len(app['Summary'])
        if summ_chars > config['char_limits']['Summary']:
            warn("Summary of length %s is over the %i char limit" % (
                summ_chars, config['char_limits']['Summary']))

        # Redundant info
        if app['Web Site'] and app['Source Code']:
            if app['Web Site'].lower() == app['Source Code'].lower():
                warn("Website '%s' is just the app's source code link" % app['Web Site'])

        # Missing or incorrect categories
        if not app['Categories']:
            warn("Categories are not set")
        for categ in app['Categories']:
            if categ not in categories:
                warn("Category '%s' is not valid" % categ)

        if app['Name'] and app['Name'] == app['Auto Name']:
            warn("Name '%s' is just the auto name" % app['Name'])

        name = app['Name'] or app['Auto Name']
        if app['Summary'] and name:
            if app['Summary'].lower() == name.lower():
                warn("Summary '%s' is just the app's name" % app['Summary'])

        desc = app['Description']
        if app['Summary'] and desc and len(desc) == 1:
            if app['Summary'].lower() == desc[0].lower():
                warn("Description '%s' is just the app's summary" % app['Summary'])

        # Description size limit
        desc_charcount = sum(len(l) for l in desc)
        if desc_charcount > config['char_limits']['Description']:
            warn("Description of length %s is over the %i char limit" % (
                desc_charcount, config['char_limits']['Description']))

        if (not desc[0] or not desc[-1]
                or any(not desc[l - 1] and not desc[l] for l in range(1, len(desc)))):
            warn("Description has an extra empty line")

        # Regex checks in all kinds of fields
        for f in regex_warnings:
            for m, r in regex_warnings[f]:
                t = metadata.metafieldtype(f)
                if t == 'string':
                    if m.match(app[f]):
                        warn("%s '%s': %s" % (f, app[f], r))
                elif t == 'multiline':
                    for l in app[f]:
                        if m.match(l):
                            warn("%s at line '%s': %s" % (f, l, r))

        # Build warnings
        for build in app['builds']:
            if build['disable']:
                continue
            for s in ['master', 'origin', 'HEAD', 'default', 'trunk']:
                if build['commit'] and build['commit'].startswith(s):
                    warn("Branch '%s' used as commit in build '%s'" % (
                        s, build['version']))
                for srclib in build['srclibs']:
                    ref = srclib.split('@')[1].split('/')[0]
                    if ref.startswith(s):
                        warn("Branch '%s' used as commit in srclib '%s'" % (
                            s, srclib))

        if not curid:
            print

    logging.info("Found a total of %i warnings in %i apps out of %i total." % (
        count['warn'], count['app'], count['app_total']))

    sys.exit(1 if count['warn'] > 0 else 0)

if __name__ == "__main__":
    main()
