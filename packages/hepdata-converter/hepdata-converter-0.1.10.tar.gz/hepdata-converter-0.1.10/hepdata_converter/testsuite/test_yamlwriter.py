# -*- encoding: utf-8 -*-
import os
import StringIO
import hepdata_converter
from hepdata_converter.testsuite import insert_data_as_file, insert_data_as_str, insert_path
from hepdata_converter.testsuite.test_writer import WriterTestSuite

__author__ = 'Michał Szostak'


class YAMLWriterTestSuite(WriterTestSuite):
    @insert_path('oldhepdata/sample.input')
    @insert_data_as_file('oldhepdata/sample.input')
    @insert_data_as_str('oldhepdata/sample.input_single.yaml')
    def test_single_file_output(self, oldhepdata_path, oldhepdata_file, oldhepdata_yaml_file):
        data = hepdata_converter.convert(oldhepdata_file,
                                         options={
                                             'input_format': 'oldhepdata',
                                             'output_format': 'yaml',
                                             'single_file': True})

        yaml_single_output_path = os.path.join(self.current_tmp, 'output.yaml')

        hepdata_converter._main(['--input-format', 'oldhepdata', '--output-format', 'yaml', '--single-file',
                                 oldhepdata_path, yaml_single_output_path])

        self.assertTrue(os.path.exists(yaml_single_output_path))

        self.assertEqual(oldhepdata_yaml_file, data)

        with open(yaml_single_output_path, 'r') as _f:
            self.assertEqual(oldhepdata_yaml_file, _f.read())



