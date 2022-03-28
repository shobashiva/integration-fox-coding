import datetime
import argparse
import gen
import pytest


@pytest.fixture()
def column_args():
    args = argparse.Namespace()
    args.column = [('free', 'string'), ('fee', 'integer')]
    return args


def test_column_data_just_name():
    with pytest.raises(TypeError):
        name = gen.column_data('foo')


def test_column_data_bad_type():
    with pytest.raises(TypeError):
        name = gen.column_data('foo, bar')


def test_column_data_bad_name():
    with pytest.raises(TypeError):
        name = gen.column_data('%, bar')


def test_column_data_too_much_data():
    with pytest.raises(TypeError):
        name = gen.column_data('foo, bar, foo')


def test_column_data():
    name = gen.column_data(' foo, integer')  # accept whitespace
    name = gen.column_data('foo,integer')


def test_filename(monkeypatch):
    with monkeypatch.context() as m:
        def mock_now():
            return datetime.datetime(2021, 10, 31, 19, 52, 0, 0)
        m.setattr('gen.get_now', mock_now)
        assert gen.get_filename() == '2021-10-31-19_52_00.csv'


def test_get_headers(column_args):
    headers = gen.get_headers(column_args)
    assert headers == ['free', 'fee']


def test_get_types(column_args):
    column_types = gen.get_column_types(column_args)
    assert column_types == ['string', 'integer']


def test_generate_csv(column_args):
    column_types = gen.get_column_types(column_args)
    rows = 20
    csv_rows = gen.generate_csv(column_types, rows)
    assert len(csv_rows) == rows
