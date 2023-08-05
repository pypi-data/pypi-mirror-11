# Tests for the odt_to_html module
import os
import tempfile
import shutil
import unittest
from Products.PortalTransforms.interfaces import ITransform
from Products.PortalTransforms.data import datastream
from ulif.openoffice.cachemanager import CacheManager, get_marker
from zope.interface.verify import verifyObject, verifyClass
from psj.policy.testing import IntegrationTestCase
from psj.policy.transforms.cmd_oooconv import OPTIONS_HTML, OPTIONS_PDF
from psj.policy.transforms.doc_to_html import Doc2Html, register


class HelperTests(unittest.TestCase):
    # Tests for non-Doc2Html components in module

    def test_register(self):
        # there is a register function that returns an appropriate object
        assert isinstance(register(), Doc2Html)


class FakeContext(object):
    # a context that holds cache keys.
    def __init__(self, html_key=None, pdf_key=None):
        self.cache_key_html = html_key
        self.cache_key_pdf = pdf_key


class Doc2HtmlTests(unittest.TestCase):
    # Tests for Doc2Html class

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.inputdir = os.path.join(os.path.dirname(__file__), 'input')
        self.cachedir = tempfile.mkdtemp()
        self.src_path1 = os.path.join(self.workdir, 'sample1.doc')
        self.src_path2 = os.path.join(self.workdir, 'sample2.docx')
        shutil.copy2(
            os.path.join(self.inputdir, 'testdoc1.doc'), self.src_path1)
        shutil.copy2(
            os.path.join(self.inputdir, 'testdoc1.docx'), self.src_path2)

    def tearDown(self):
        shutil.rmtree(self.workdir)
        if os.path.isdir(self.cachedir):
            shutil.rmtree(self.cachedir)

    def register_fakedoc_in_cache(self, src, options):
        # register a fake doc in cache. Result cache_key is based on
        # path to src document and options given.
        cm = CacheManager(self.cachedir)
        fake_result_path = os.path.join(self.workdir, 'result.html')
        open(fake_result_path, 'w').write('A fake result.')
        marker = get_marker(options)
        cache_key = cm.register_doc(src, fake_result_path, repr_key=marker)
        return cache_key

    def test_iface(self):
        # make sure we fullfill interface contracts
        obj = Doc2Html()
        verifyClass(ITransform, Doc2Html)
        verifyObject(ITransform, obj)

    def test_mimetypes(self):
        # we have proper mimetypes set
        transform = Doc2Html()
        self.assertEqual(transform.output, 'text/html')
        self.assertEqual(transform.output_encoding, 'utf-8')
        self.assertEqual(
            transform.inputs,
            ('application/msword',
             'application/vnd.openxmlformats-officedocument' +
             '.wordprocessingml.document'))

    def test_name(self):
        # we can get the transform name
        transform = Doc2Html()
        self.assertEqual(transform.name(), 'doc_to_html')
        self.assertEqual(transform.name('other_name'), 'doc_to_html')

    def test_cache_dir(self):
        # we can set/get a cache dir
        transform = Doc2Html(cache_dir='/foo')
        self.assertEqual(transform.cache_dir, '/foo')

    def test_cache_dir_default(self):
        # we have a cache_dir default (emtpy string)
        transform = Doc2Html()
        self.assertEqual(transform.cache_dir, '')

    def test_convert(self):
        # we can convert odt docs to HTML.
        transform = Doc2Html()
        idatastream = datastream('mystream')
        transform.convert(
            open(self.src_path2, 'r').read(),
            idatastream)
        assert '</span>' in idatastream.getData()
        self.assertEqual(idatastream.getMetadata(), {'cache_key_html': None})

    def test_convert_with_cachekey(self):
        # we retrieve cached files if cache_key is set and valid
        cache_key = self.register_fakedoc_in_cache(
            src=self.src_path1, options=OPTIONS_HTML)
        transform = Doc2Html(cache_dir=self.cachedir)
        idatastream = datastream('mystream')
        # set cache key for HTML
        idatastream.context = FakeContext(html_key=cache_key)
        transform.convert(
            # We give a different source than what was cached as source.
            # This way we can be sure that if we get the fake result, it was
            # really retrieved via cache key lookup and not via source
            # lookup.
            open(self.src_path2, 'r').read(),
            idatastream)
        assert idatastream.getData() == 'A fake result.'


class Doc2HtmlIntegrationTests(IntegrationTestCase):

    def test_registered(self):
        # the transform is registered in a standard plonesite after install
        transforms = self.portal.portal_transforms
        assert 'doc_to_html' in transforms.keys()
