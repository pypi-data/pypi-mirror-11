import prang.simplification
import prang.validation
import pkgutil
import xml.dom
import xml.dom.minidom
from ._version import get_versions
import os.path
__version__ = get_versions()['version']
del get_versions

from prang.simplification import PrangException

rng_str = pkgutil.get_data('prang', 'relaxng.rng').decode('utf8')
rng_dom = xml.dom.minidom.parseString(rng_str)
rng_el = prang.simplification.to_prang_elem(None, rng_dom.documentElement)
prang.simplification.simplify(rng_el)
test_el = rng_el
rng_el = prang.validation.typify(rng_el)


class Schema():
    def __init__(
            self, schema_str=None, schema_file=None, schema_file_name=None,
            base_uri=None):
        # print("After simplification of rng", test_el)
        if schema_file_name is not None:
            schema_file = open(schema_file_name)
            if base_uri is None:
                base_uri = os.path.dirname(
                    os.path.join(os.getcwd(), schema_file_name)) + os.sep
        if schema_file is not None:
            schema_str = ''.join(schema_file.readlines())
        if schema_str is None:
            raise Exception(
                "A schema_str, schema_file or schema_file_name argument must "
                "be given.")
        schema_dom = xml.dom.minidom.parseString(schema_str)
        self.schema_el = prang.simplification.to_prang_elem(
            base_uri, schema_dom.documentElement)
        prang.validation.validate(rng_el, schema_str)
        # print("about to simplify")
        prang.simplification.simplify(self.schema_el)
        # print(self.schema_el)
        # print("about to typify")
        self.frozen_schema_el = prang.validation.typify(self.schema_el)
        # print("finished typifying")
        # print(self.frozen_schema_el)

    def validate(self, doc_str=None, doc_file=None, doc_file_name=None):
        if doc_file_name is not None:
            doc_file = open(doc_file_name)
        if doc_file is not None:
            doc_str = ''.join(doc_file.readlines())
        if doc_str is None:
            raise Exception(
                "A doc_str, doc_file or doc_file_name argument must be given.")
        # print("frozen schema is " + str(self.frozen_schema_el))
        # print("starting to validate", doc_str)
        prang.validation.validate(self.frozen_schema_el, doc_str)

__all__ = (PrangException)
