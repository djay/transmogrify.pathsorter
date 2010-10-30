
import unittest

from zope.testing import doctest
from zope.component import provideUtility
from Products.Five import zcml
from zope.component import provideUtility
from zope.interface import classProvides, implements
from collective.transmogrifier.interfaces import ISectionBlueprint, ISection

from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure

from collective.transmogrifier.tests import setUp as baseSetUp
from collective.transmogrifier.tests import tearDown
from collective.transmogrifier.sections.tests import PrettyPrinter
from collective.transmogrifier.sections.tests import SampleSource

from transmogrify.webcrawler.webcrawler import WebCrawler
from treeserializer import TreeSerializer
from transmogrify.webcrawler.typerecognitor import TypeRecognitor
import transmogrify.pathsorter
from lxml import etree
import lxml.html
import lxml.html.soupparser
from lxml.html.clean import Cleaner
import urlparse
from os.path import dirname, abspath
import urllib


def setUp(test):
    baseSetUp(test)

    from collective.transmogrifier.transmogrifier import Transmogrifier
    test.globs['transmogrifier'] = Transmogrifier(test.globs['plone'])

    import zope.component
    import collective.transmogrifier.sections
    zcml.load_config('meta.zcml', zope.app.component)
    zcml.load_config('configure.zcml', collective.transmogrifier.sections)

    test.globs['plone'].portal_transforms = MockPortalTransforms()

    provideUtility(PrettyPrinter,
        name=u'collective.transmogrifier.sections.tests.pprinter')
    provideUtility(WebCrawler,
        name=u'transmogrify.pathsorter.webcrawler')
    provideUtility(TreeSerializer,
        name=u'transmogrify.pathsorter.treeserializer')
    provideUtility(TypeRecognitor,
        name=u'transmogrify.pathsorter.typerecognitor')
    provideUtility(TemplateFinder,
        name=u'transmogrify.pathsorter.templatefinder')
    provideUtility(urlnormalizer)
    provideUtility(Relinker,
        name=u'transmogrify.pathsorter.relinker')
    provideUtility(SimpleXPath,
        name=u'transmogrify.pathsorter.simplexpath')
    provideUtility(SafePortalTransforms,
        name=u'transmogrify.pathsorter.safeportaltransforms')
    from backlinkstitle import BacklinksTitle
    provideUtility(BacklinksTitle,
        name=u'transmogrify.pathsorter.backlinkstitle')
    from isindex import IsIndex
    provideUtility(IsIndex,
        name=u'transmogrify.pathsorter.isindex')
    from pathmover import PathMover
    provideUtility(PathMover,
        name=u'transmogrify.pathsorter.pathmover')
    from safeatschemaupdater import SafeATSchemaUpdaterSection
    provideUtility(SafeATSchemaUpdaterSection,
        name=u'transmogrify.pathsorter.safeatschemaupdater')
    from constructor import SafeConstructorSection
    provideUtility(SafeConstructorSection,
        name=u'transmogrify.pathsorter.constructor')
    from makeattachments import MakeAttachments
    provideUtility(MakeAttachments,
        name=u'transmogrify.pathsorter.makeattachments')
    from debugsection import DebugSection
    provideUtility(DebugSection,
        name=u'transmogrify.pathsorter.debugsection')
    from staticcreator import StaticCreatorSection
    provideUtility(StaticCreatorSection,
        name=u'transmogrify.pathsorter.staticcreator')

    provideUtility(HTMLSource,
        name=u'transmogrify.pathsorter.test.htmlsource')
    provideUtility(HTMLBacklinkSource,
        name=u'transmogrify.pathsorter.test.htmlbacklinksource')

#@onsetup
def setup_product():
    """ """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', transmogrify.pathsorter)
    fiveconfigure.debug_mode = False
    ztc.installPackage('plone.app.z3cform')
#    ztc.installPackage('lovely.remotetask')
    ztc.installPackage('transmogrify.pathsorter')


setup_product()
#ptc.setupPloneSite(extension_profiles=('transmogrify.pathsorter:default',), with_default_memberarea=False)
ptc.setupPloneSite(products=['transmogrify.pathsorter'])



def test_suite():
    flags = optionflags = doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE | \
                        doctest.NORMALIZE_WHITESPACE | doctest.REPORT_UDIFF

    return unittest.TestSuite((

        doctest.DocFileSuite('treeserializer.txt', 
                setUp=setUp, 
                tearDown=tearDown, 
                optionflags=flags),



    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


