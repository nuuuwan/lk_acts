import os
import unittest

from lk_acts import pdf2xml


class TestCase(unittest.TestCase):
    def testConvert(self):
        pdf_file = 'data/bill-2022-09-personal-data-protection.pdf'
        page_nos = 'all'
        xml_file = f'{pdf_file}.{page_nos}.xml'
        if os.path.exists(xml_file):
            os.remove(xml_file)
        pdf2xml.convert(pdf_file, page_nos, xml_file)
        # self.assertTrue(os.path.exists(xml_file))


if __name__ == '__main__':
    unittest.main()
