"""Test uniti test for dataset class."""

from unittest.mock import Mock, patch

from deepecho.benchmark.dataset import Dataset


class TestDataset:
    """Testing class for Dataset."""

    @patch('deepecho.benchmark.dataset.Metadata', autospec=True)
    def test__load_from_path(self, gm_mock):
        """Test ``_load_from_path``.

        The _load_from_path is expected to:
        - call ```self._load_table()`` method.

        Side Effects
        - ``self._load_table()`` is called.
        """
        # Setup
        mock_dataset = Mock(spec=Dataset)
        dataset_name = 'test'
        table_name = None

        # Run
        Dataset._load_from_path(mock_dataset, dataset_name, table_name)

        # Asserts
        assert mock_dataset._load_table.called

    def test__load_from_s3(self):
        """Test ``_load_from_s3``.

        The _load_from_s3 is expected to:
        - call ```self._load_table()`` method.

        Side Effects
        - ``self._load_table()`` is called.
        """
        # Setup
        mock_dataset = Mock(spec=Dataset)
        dataset_name = 'test'
        table_name = None

        # Run
        Dataset._load_from_s3(mock_dataset, dataset_name, table_name)

        # Asserts
        assert mock_dataset._load_table.called

    @patch('deepecho.benchmark.dataset.os.chdir', autospec=True)
    @patch('deepecho.benchmark.dataset.Metadata', autospec=True)
    @patch('deepecho.benchmark.dataset.ZipFile', autospec=True)
    def test__load_from_zip(self, gm_mock_os, gm_mock_metadata, gm_mock_ZipFile):
        """Test ``_load_from_path``.

        The _load_from_zip is expected to:
        - call ```self._load_from_path()`` method.

        Side Effects
        - ``self._load_from_path()`` is called git the given values.
        """
        mock_dataset = Mock(spec=Dataset)
        dataset_name = 'test.zip'
        table_name = None

        # Run
        Dataset._load_from_zip(mock_dataset, dataset_name, table_name)

        # Asserts
        mock_dataset._load_from_path.assert_called_once_with(dataset_name[:-4], None)

    @patch('deepecho.benchmark.dataset.Dataset._load_from_path', return_value=None)
    def test___init__path(self, gm_mock):
        """Test ``__init__`` for a path corresponding to a local directory dataset.

        The __init__ method is expected to:
        - call ```self._load_from_path`` method.

        Side Effects
        - ``self._load_from_path()`` is called.
        """
        # Setup
        mock_dataset = Mock(set=Dataset)
        mock_dataset.data.columns = []
        # Run
        dataset_name = './'
        Dataset.__init__(mock_dataset, dataset_name)

        # Asserts
        assert mock_dataset._load_from_path.called

    @patch('deepecho.benchmark.dataset.Dataset._load_from_s3', return_value=None)
    def test___init__s3(self, gm_mock):
        """Test ``__init__`` for dataset stored in s3.

        The __init__ method is expected to:
        - call ```self._load_from_s3`` method.

        Side Effects
        - ``self._load_from_s3()`` is called.
        """
        # Setup
        mock_dataset = Mock(set=Dataset)
        mock_dataset.data.columns = []
        # Run
        dataset_name = 'some_dataset'
        Dataset.__init__(mock_dataset, dataset_name)

        # Asserts
        assert mock_dataset._load_from_s3.called

    @patch('deepecho.benchmark.dataset.os.path.exists', return_value=True)
    @patch('deepecho.benchmark.dataset.Dataset._load_from_zip', return_value=None)
    def test___init__zip(self, gm_mock_os, gm_mock_metadata):
        """Test ``__init__`` for a path corresponding to a local zip file.

        The __init__ method is expected to:
        - call ```self._load_from_zip`` method.

        Side Effects
        - ``self._load_from_zip()`` is called.
        """
        # Setup
        mock_dataset = Mock(set=Dataset)
        mock_dataset.data.columns = []
        # Run
        dataset_name = '.zip'
        Dataset.__init__(mock_dataset, dataset_name)

        # Asserts
        assert mock_dataset._load_from_zip.called

    def test___init__segment_size(self):
        """Test ``__init__`` for passing max_entities value.

        This test calls the __init__ method passig a max_entities value,
        is necesary provide a way to get the dataset, that means pass a
        directory, s3 dataset or zip dataset. That test provides a path.
        The __init__ method is expected to:
        - call ```self._filter_entities`` method.

        Side Effects
        - ``self._get_evaluation_data()`` is called with the given value.
        """
        # Setup
        mock_dataset = Mock(set=Dataset)
        mock_dataset.data.columns = []
        # Run
        dataset_name = './'
        segment_size = 10
        Dataset.__init__(mock_dataset, dataset_name, segment_size=segment_size)

        # Asserts
        mock_dataset._get_evaluation_data.assert_called_once_with(segment_size)

    def test___init__max_entities(self):
        """Test ``__init__`` for passing max_entities value.

        This test calls the __init__ method passig a max_entities value,
        is necesary provide a way to get the dataset, that means pass a
        directory, s3 dataset or zip dataset. That test provides a path.
        The __init__ method is expected to:
        - call ```self._filter_entities`` method.

        Side Effects
        - ``self._filter_entities()`` is called with the given value.
        """
        # Setup
        mock_dataset = Mock(set=Dataset)
        mock_dataset.data.columns = []
        # Run
        dataset_name = './'
        max_entities = 10
        Dataset.__init__(mock_dataset, dataset_name, max_entities=max_entities)

        # Asserts
        mock_dataset._filter_entities.assert_called_once_with(max_entities)
