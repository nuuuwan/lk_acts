import os
import unittest

from lk_acts import download


class TestCase(unittest.TestCase):
    def testGetFile(self):
        self.assertEqual(
            download.get_file('bill-2022-09-personal-data-protection'),
            'data/bill-2022-09-personal-data-protection.pdf',
        )

    def testDownloadBill(self):
        for [url, label] in [
            [
                'http://documents.gov.lk/files/bill/2022/1/167-2022_E.pdf',
                'bill-2022-09-personal-data-protection',
            ]
        ]:
            doc_file = download.get_file(label)
            if os.path.exists(doc_file):
                os.remove(doc_file)
            download.download_bill(url, label)
            self.assertTrue(os.path.exists(doc_file))


if __name__ == '__main__':
    unittest.main()
