import os
import unittest

from lk_acts import pdf2xml


class TestCase(unittest.TestCase):
    def testConvert(self):
        pdf_file = 'data/bill-2022-09-personal-data-protection.pdf'
        page_no = 1
        xml_file = f'{pdf_file}.{page_no:06d}.xml'
        if os.path.exists(xml_file):
            os.remove(xml_file)
        pdf2xml.convert(pdf_file, page_no, xml_file)
        # self.assertTrue(os.path.exists(xml_file))


if __name__ == '__main__':
    unittest.main()
