# -*- coding:utf-8 -*-

"""Page-loader tests."""
import pytest
import os.path
import requests_mock
from tempfile import TemporaryDirectory
from page_loader.loader.page import download

assets_folder = 'page-loader-hexlet-repl-co_files'
assets_local_list = [
    'page-loader-hexlet-repl-co-assets-application.css',
    'page-loader-hexlet-repl-co-assets-professions-nodejs.png',
    'page-loader-hexlet-repl-co-script.js'
]
assets_remote_list = [
    'assets/professions/nodejs.png',
    'assets/application.css',
    'script.js'
]
def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "fixtures", file_name)


def read(file_path):
    with open(file_path, "r") as fl:
        result = fl.read()
    return result

def test_page_load():
    page_url = 'https://page-loader.hexlet.repl.co/'
    with requests_mock.Mocker() as req_mock:
        response_text = read(get_fixture_path('page-loader.html'))
        req_mock.get(page_url, text=response_text)
        for remote_asset in assets_remote_list:
            req_mock.get(os.path.join(page_url, remote_asset), text=' ')
        with TemporaryDirectory() as tmp_dir_name:
            expected_file = os.path.join(tmp_dir_name, 'page-loader-hexlet-repl-co.html')
            assert download(page_url, tmp_dir_name) == expected_file
            assert os.path.isfile(expected_file) == True
            assert read(get_fixture_path('page-loader-local.html')) == read(expected_file)
            for asset in assets_local_list:
                asset_path = os.path.join(tmp_dir_name, assets_folder, asset)
                os.path.isfile(asset_path) == True

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
    target_dir ='/sys/ru-hexlet-io-courses_files'
    with pytest.raises(ValueError) as excinfo:
        download(target_page, temp_dir_name)
    assert 'Can not create a directory {0}'.format(target_dir) in str(excinfo.value)

def test_dir_not_exists():
    target_page = 'https://ru.hexlet.io/courses'
    target_dir ='/sys/ru-hexlet-io_files'
    with pytest.raises(ValueError) as excinfo:
        download(target_page, target_dir)
    assert 'Dir {0} does not exist'.format(target_dir) in str(excinfo.value)
