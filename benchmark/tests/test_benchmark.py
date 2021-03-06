from deepecho.benchmark import run_benchmark
from deepecho.benchmark.dataset import Dataset


def test_run_benchmark():
    models = [('PARModel', {'epochs': 5, 'cuda': False, 'verbose': False})]
    datasets = [Dataset('Libras', max_entities=10)]
    metrics = ['sdmetrics', 'rf_detection']
    results = run_benchmark(
        models=models,
        datasets=datasets,
        metrics=metrics
    )

    expected = ['model', 'dataset', 'fit_time', 'sample_time', 'rf_detection',
                'rf_detection_time', 'sdmetrics', 'sdmetrics_time']
    assert list(results.columns) == expected
    assert results.shape == (1, 8)
