import unittest
from unittest import mock

import pandas as pd
from pandas.errors import EmptyDataError

from filmweb_integrator.fwimdbmerge.merger import Merger


class TestMerger(unittest.TestCase):

    @mock.patch('filmweb_integrator.fwimdbmerge.filmweb.Filmweb')
    @mock.patch('filmweb_integrator.fwimdbmerge.imdb.Imdb')
    def setUp(self, mock_filmweb, mock_imdb):
        self.mock_filmweb = mock_filmweb
        self.mock_imdb = mock_imdb
        self.sut = Merger(filmweb=self.mock_filmweb, imdb=self.mock_imdb)

    def test_get_data_should_return_dataframe(self):
        # given
        df = pd.DataFrame()
        self.mock_filmweb.get_dataframe.return_value = df
        self.mock_imdb.merge.return_value = df

        # when
        result = self.sut.get_data({})

        # then
        self.assertIsInstance(result, pd.DataFrame)

    def test_get_data_should_throw_exception_when_wrong_json_given(self):
        # given
        json = '{'

        # expect
        self.mock_filmweb.get_dataframe.assert_not_called()
        self.mock_imdb.merge.assert_not_called()

        # then
        self.assertRaises(AttributeError, self.sut.get_data, json)

    def test_get_data_should_throw_exception_when_processing_error(self):
        # given
        json = {}
        self.mock_filmweb.get_dataframe.side_effect = EmptyDataError()

        # expect
        self.mock_imdb.merge.assert_not_called()

        # then
        self.assertRaises(EmptyDataError, self.sut.get_data, json)