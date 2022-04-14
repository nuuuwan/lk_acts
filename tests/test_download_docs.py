import os
import unittest

from lk_acts import download


class TestCase(unittest.TestCase):
    def Test(self):
        for [url, label] in [
            [
                'http://documents.gov.lk/files/bill/2022/1/167-2022_E.pdf',
                'bill-99-personal-data-protection',
            ]
        ]:
            doc_file = download.get_file(label)
            os.rm(doc_file)
            download.download_bill(url, label)
            self.assertTrue(os.path.exists(doc_file))


if __name__ == '__main__':
    unittest.main()
