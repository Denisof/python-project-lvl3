# -*- coding:utf-8 -*-

"""Page-loader tests."""
import pytest
import os.path
import requests_mock
from tempfile import TemporaryDirectory
from page_loader.loader.page import download

def test_page_load():
    page_url = 'https://ru.hexlet.io/courses'
    with requests_mock.Mocker() as req_mock:
        req_mock.get(page_url, text='some text')
        with TemporaryDirectory() as tmp_dir_name:
            expected = os.path.join(tmp_dir_name, 'ru-hexlet-io-courses.html')
            assert download(page_url, tmp_dir_name) == expected
            assert os.path.isfile(expected) == True

def test_page_not_found():
    target_page = 'https://ru.hexlet.io/404'
    with requests_mock.Mocker() as req_mock:
        req_mock.get(target_page, status_code=404)
        with pytest.raises(ValueError) as excinfo:
            with TemporaryDirectory() as tmp_dir_name:
                download(target_page, tmp_dir_name)
        assert 'Target page {0} is not available '.format(target_page) in str(excinfo.value)

def test_can_not_write_denied():
    target_page = 'https://ru.hexlet.io/courses'
    temp_dir_name = '/sys'
    target_file = os.path.join(temp_dir_name, 'ru-hexlet-io-courses.html')
    with pytest.raises(ValueError) as excinfo:
        download(target_page, temp_dir_name)
    assert 'Can not write to {0}'.format(target_file) in str(excinfo.value)
