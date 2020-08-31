"""Test uniti test for dataset class."""

import os
from unittest.mock import Mock, patch

from deepecho.benchmark.dataset import Dataset


class TestDataset:
    """Testing class for Dataset."""

    @patch('deepecho.benchmark.dataset.Metadata', autospec=True)
    def test__load_from_path(self, gm_mock):
        """Test ``_load_from_path``.

        The _load_from_path is expected to:
        - Initialize parameters according to input variables. Like 'self.name'
        - call ```self._load_table()`` method.
        - call ```Metadata``` method.

        Side Effects
        - Variable 'self.name' equal to input variable `dataset_name`
        - ``self._load_table()`` is called.
        - ```Metadata`` is called once with the expected parameters.
        """
        # Setup
        mock_dataset = Mock(spec=Dataset)
        dataset_name = 'test'
        table_name = None

        # Run
        Dataset._load_from_path(mock_dataset, dataset_name, table_name)

        # Asserts
        assert mock_dataset._load_table.called
        assert mock_dataset.name == dataset_name
        gm_mock.assert_called_once_with(os.path.join(dataset_name, 'metadata.json'))

    def test__load_from_s3(self):
        """Test ``_load_from_s3``.

        The _load_from_s3 is expected to:
        - Initialize parameters according to input variables. Like 'self.name'
        - call ```self._load_table()`` method.

        Side Effects
        - ``self._load_table()`` is called.
        - Variable 'self.name' equal to input variable `dataset_name`
        """
        # Setup
        mock_dataset = Mock(spec=Dataset)
        dataset_name = 'test'
        table_name = None

        # Run
        Dataset._load_from_s3(mock_dataset, dataset_name, table_name)

        # Asserts
        assert mock_dataset._load_table.called
        assert mock_dataset.name == dataset_name

    @patch('deepecho.benchmark.dataset.os.chdir', autospec=True)
    @patch('deepecho.benchmark.dataset.ZipFile', autospec=True)
    def test__load_from_zip(self, gm_mock_os, gm_mock_ZipFile):
        """Test ``_load_from_zip``.

        The _load_from_zip is expected to:
        - call ```self._load_from_path()`` method.

        Side Effects
        - ``self._load_from_path()`` is called with the given values.
        """
        # Setup
        mock_dataset = Mock(spec=Dataset)
        dataset_name = 'test.zip'
        table_name = None

        # Run
        Dataset._load_from_zip(mock_dataset, dataset_name, table_name)

        # Asserts
        assert mock_dataset._load_from_path.called

    @patch('deepecho.benchmark.dataset.Dataset._load_from_path', return_value=None)
    def test___init__path(self, gm_mock):
        """Test ``__init__`` for a path corresponding to a local directory dataset.

        The __init__ method is expected to:
        - call ```self._load_from_path`` method.
        - Initialize parameters. Like 'self.context_columns'.
        - Do not call method ```_filter_entities```.
        - Do not call method ```_get_evaluation_data```.

        Side Effects
        - ``self._load_from_path()`` is called.
        -  'self.context_columns' variable equal to the defined value.
        - ```_filter_entities``` method is not called.
        - ```_get_evaluation_data``` method is not called.
        """
        # Setup
        mock_dataset = Mock(set=Dataset)
        mock_dataset.data.columns = []
        mock_dataset._get_context_columns.return_value = 'context_columns'

        # Run
        dataset_name = './'
        Dataset.__init__(mock_dataset, dataset_name)

        # Asserts
        mock_dataset._load_from_path.assert_called_once_with(dataset_name, None)
        assert mock_dataset.context_columns == 'context_columns'
        assert not mock_dataset._filter_entities.called
        assert not mock_dataset._get_evaluation_data.called

    @patch('deepecho.benchmark.dataset.Dataset._load_from_s3', return_value=None)
    def test___init__s3(self, gm_mock):
        """Test ``__init__`` for a dataset stored in s3.

        The __init__ method is expected to:
        - call ```self._load_from_s3`` method.
        - Initialize parameters. Like 'self.context_columns'.
        - Do not call method ```_filter_entities```.
        - Do not call method ```_get_evaluation_data```.

        Side Effects
        - ``self._load_from_s3()`` is called.
        -  'self.context_columns' variable equal to the defined value.
        - ```_filter_entities``` method is not called.
        - ```_get_evaluation_data``` method is not called.
        """
        # Setup
        mock_dataset = Mock(set=Dataset)
        mock_dataset.data.columns = []
        mock_dataset._get_context_columns.return_value = 'context_columns'

        # Run
        dataset_name = 'some_dataset'
        Dataset.__init__(mock_dataset, dataset_name)

        # Asserts
        mock_dataset._load_from_s3.assert_called_once_with(dataset_name, None)
        assert mock_dataset.context_columns == 'context_columns'
        assert not mock_dataset._filter_entities.called
        assert not mock_dataset._get_evaluation_data.called

    @patch('deepecho.benchmark.dataset.os.path.exists', return_value=True)
    @patch('deepecho.benchmark.dataset.Dataset._load_from_zip', return_value=None)
    def test___init__zip(self, gm_mock_os, gm_mock_metadata):
        """Test ``__init__`` for a path corresponding to a local zip file.

        The __init__ method is expected to:
        - call ```self._load_from_zip`` method.
        - Initialize parameters. Like 'self.context_columns'.
        - Do not call method ```_filter_entities```.
        - Do not call method ```_get_evaluation_data```.

        Side Effects
        - ``self._load_from_zip()`` is called.
        -  'self.context_columns' variable equal to the defined value.
        - ```_filter_entities``` method is not called.
        - ```_get_evaluation_data``` method is not called.
        """
        # Setup
        mock_dataset = Mock(set=Dataset)
        mock_dataset.data.columns = []
        mock_dataset._get_context_columns.return_value = 'context_columns'

        # Run
        dataset_name = '.zip'
        Dataset.__init__(mock_dataset, dataset_name)

        # Asserts
        mock_dataset._load_from_zip.assert_called_once_with(dataset_name, None)
        assert mock_dataset.context_columns == 'context_columns'
        assert not mock_dataset._filter_entities.called
        assert not mock_dataset._get_evaluation_data.called

    def test___init__segment_size(self):
        """Test ``__init__`` for passing max_entities value.

        This test calls the __init__ method passig a max_entities value,
        is necesary provide a way to get the dataset, that means pass a
        directory, s3 dataset or zip dataset. That test provides a path.

        The __init__ method is expected to:
        - call ```self._load_from_path`` method.
        - Initialize parameters. Like 'self.context_columns'.
        - Do not call method ```_filter_entities```.
        - Call method ```_get_evaluation_data```.

        Side Effects
        - ``self._load_from_path()`` is called.
        -  'self.context_columns' variable equal to the defined value.
        - ```_filter_entities``` method is not called.
        - ```_get_evaluation_data``` method is called.
        """
        # Setup
        mock_dataset = Mock(set=Dataset)
        mock_dataset.data.columns = []
        mock_dataset._get_context_columns.return_value = 'context_columns'

        # Run
        dataset_name = './'
        segment_size = 10
        Dataset.__init__(mock_dataset, dataset_name, segment_size=segment_size)

        # Asserts
        mock_dataset._load_from_path.assert_called_once_with(dataset_name, None)
        assert mock_dataset.context_columns == 'context_columns'
        assert not mock_dataset._filter_entities.called
        assert mock_dataset._get_evaluation_data.called

    def test___init__max_entities(self):
        """Test ``__init__`` for passing max_entities value.

        This test calls the __init__ method passig a max_entities value,
        is necesary provide a way to get the dataset, that means pass a
        directory, s3 dataset or zip dataset. That test provides a path.

        The __init__ method is expected to:
        - call ```self._load_from_path`` method.
        - Initialize parameters. Like 'self.context_columns'.
        - Call method ```_filter_entities```.
        - Do not call method ```_get_evaluation_data```.

        Side Effects
        - ``self._load_from_path()`` is called.
        -  'self.context_columns' variable equal to the defined value.
        - ```_filter_entities``` method is called.
        - ```_get_evaluation_data``` method is not called.
        """
        # Setup
        mock_dataset = Mock(set=Dataset)
        mock_dataset.data.columns = []
        mock_dataset._get_context_columns.return_value = 'context_columns'

        # Run
        dataset_name = './'
        max_entities = 10
        Dataset.__init__(mock_dataset, dataset_name, max_entities=max_entities)

        # Asserts
        mock_dataset._load_from_path.assert_called_once_with(dataset_name, None)
        assert mock_dataset.context_columns == 'context_columns'
        assert mock_dataset._filter_entities.called
        assert not mock_dataset._get_evaluation_data.called
