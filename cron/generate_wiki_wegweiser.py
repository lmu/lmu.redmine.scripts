#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket

from redmine import Redmine
from redmine.exceptions import ValidationError


redmine = Redmine(
    'https://www.scm.verwaltung.uni-muenchen.de/webprojekte/',
    username='admin',
    password='admin',
    requests={'verify': False},
    raise_attr_exception=False
)

master_project = 'webprojekte'
rmaster_project_id = redmine.project.get(master_project).id


def generate_wiki_wegweiser():

    all_projects = [(project.id,
                     project,
                     project.identifier,
                     project.name)
                    for project in redmine.project.all()]

    for project_id, project, project_identifier, project_name in all_projects:
        try:
            print u"Try to update Project: [{id}] {identifier}: {name}".format(
                id=project_id,
                identifier=project_identifier,
                name=project_name)
            content = '[[Fionagruppen]]' if isWebproject(project) \
                else 'Bitte [[wegweiser]] aufbauen'
            print u"write: {content}".format(
                content=content)
            redmine.wiki_page.create(project_id=project_id,
                                     title='wegweiser',
                                     text=content)
        except ValidationError:
            pass
        #except UnknownError:
        #    ipdb.set_trace()


def isWebproject(project):
    return '_' in project.identifier
    #try:
    #    parent = project.parent
    #    if parent:
    #    #ipdb.set_trace()
    #        if parent.id == rmaster_project_id:
    #            return True
    #        else:
    #            return isWebproject(parent)
    #    return False
    #except ResourceAttrError:
    #    return False

if __name__ == "__main__":
    generate_wiki_wegweiser()
