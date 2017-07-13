#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from ConfigParser import SafeConfigParser
from redmine import Redmine

import datetime
import logging
import sys


log = logging.getLogger('Redmine-Warteschlange-Handler')
my_formatter = logging.Formatter(
    fmt='%(name)s: %(asctime)s - %(levelname)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)
stdout_hanlder = logging.StreamHandler(sys.stdout)
stdout_hanlder.setFormatter(my_formatter)
log.addHandler(stdout_hanlder)
file_handler = logging.FileHandler(
    'warteschlange.log',
    mode='a',
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
    requests={'verify': False})

log.info("Connecting to Redmine Instance %s ", redmine.url)

statuses = redmine.issue_status.all()

todo_id = 0
warteschlange_id = 0
for status in statuses:
    if status.name == 'Todo':
        todo_id = status.id
    elif status.name == 'Warteschlange':
        warteschlange_id = status.id

issues = redmine.issue.filter(
    status=todo_id,
    start_date=">{date}".format(date=today.isoformat())
)

for issue in issues:
    log.info('Move Issue "%s" to Warteschlange', issue.id)
    issue.status = warteschlange_id
    issue.save()

issues = redmine.issue.filter(
    status=todo_id,
    start_date="<={date}".format(date=today.isoformat())
)

for issue in issues:
    log.info('Move Issue "%s" to Todo', issue.id)
    issue.status = todo_id
    issue.save()
