
import fnmatch
from zope.interface import classProvides
from zope.interface import implements
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.utils import Matcher

import re

"""
Backlinks Title
===============

This blueprint will take the _backlinks from the item generated by webcrawler
and if not Title field has been given to the item it will attempt to guess
it from the link names that linked to this document.
You can specify an option 'ignore' option to specify titles never to use

"""

class BacklinksTitle(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.toignore=options.get('ignore','').strip().split('\n')

    def __iter__(self):
        for item in self.previous:
            backlinks = item.get('_backlinks')
            title = item.get('title')
            if not backlinks or title:
                yield item
                continue
            #import pdb; pdb.set_trace()
            names = [name for url, name in backlinks if not self.ignore(name)]
            # do a vote
            votes = {}
            for name in names:
                votes[name] = votes.get(name,0) + 1
            votes = [(c,name) for name,c in votes.items()]
            votes.sort()
            if votes:
                c,item['title'] = votes[-1]
            yield item

    def ignore(self, name):
        for pat in self.toignore:
            if re.search(pat,name):
                return True
        return False

