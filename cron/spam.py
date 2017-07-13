#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from ConfigParser import SafeConfigParser
from redmine import Redmine

import datetime
import logging
import sys


# Set up log handler for Fiona Redmine Import:
log = logging.getLogger('Redmine-SPAM-Handler')
my_formatter = logging.Formatter(
    fmt='%(name)s: %(asctime)s - %(levelname)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)
stdout_hanlder = logging.StreamHandler(sys.stdout)
stdout_hanlder.setFormatter(my_formatter)
log.addHandler(stdout_hanlder)
file_handler = logging.FileHandler(
    'fione_import.log',
    mode='w',
    encoding='utf-8')
file_handler.setFormatter(my_formatter)
log.addHandler(file_handler)
# Set Basic Log-Level for this
log.setLevel(logging.DEBUG)

# Timestamp for reporting
datefmt = '%Y-%m-%d %H:%M'  # user timestamp.strf(datefmt) for output
today = datetime.date.today()

# Setup Redmine-Connector:
redmine = Redmine(
    'https://www.scm.verwaltung.uni-muenchen.de/webprojekte/',
    key='6824fa6b6ad10fa4828e003faf793a2260688486',
    requests={'verify': False}
)

log.info("Connecting to Redmine Instance %s ", redmine.url)

spam_tag = 'SPAM'
new_tag = 'Neuer Kontakt'

new_contacts = redmine.contact.filter(tags=new_tag)
for contact in new_contacts:
    log.info(
        'Found Contact "%s" in Tag: "%s" with e-mail: $s',
        contact.id,
        new_tag,
        ', '.join(contact.emails)
    )
    if not contact.issues:
        contact.tags = spam_tag
        contact.save()

        contact.project.add('spam')
        projects = contact.projects
        for project in projects:
            if project.identfier != 'spam':
                contact.project.remove(project.identfier)
        log.info(
            'Contact "%s" moved into project: spam',
            contact.id
        )
