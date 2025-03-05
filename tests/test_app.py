#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import mock

import pytest

from app import create_app
from config import Config


class TestConfig(Config):
    pass

@pytest.fixture
def client():
    app = create_app(TestConfig)
    app.app_context().push()

    with app.test_client() as client:
        yield client

def test_app(
    client,
):
    # GET: should always fail with 405 method not allowed
    with mock.patch.dict('os.environ', {
        'API_KEY': 'test',
        'MQTT_HOST': 'testhost',
        'MQTT_PORT': '1883',
    }):
        with mock.patch('paho.mqtt.publish.single') as mock_publish_single:
            rv = client.get(
                '/',
                headers={'Authorization': 'Bearer test', 'Content-Type': 'application/json'},
                json={'topic': 'test', 'message': 'test message'},
            )
            assert rv.status_code == 405
            assert not mock_publish_single.called

    # POST: should always fail with no API_KEY set
    with mock.patch.dict('os.environ', {}):
        with mock.patch('paho.mqtt.publish.single') as mock_publish_single:
              rv = client.post('/')
              assert rv.status_code == 401
              assert not mock_publish_single.called

    # standard test
    with mock.patch.dict('os.environ', {
        'API_KEY': 'test',
        'MQTT_HOST': 'testhost',
        'MQTT_PORT': '1883',
    }):
        with mock.patch('paho.mqtt.publish.single') as mock_publish_single:

            rv = client.post(
                '/',
                headers={'Authorization': 'Bearer test', 'Content-Type': 'application/json'},
                json={'topic': 'test', 'message': 'test message'},
            )
            assert rv.status_code == 200
            mock_publish_single.assert_called_once_with(
                'test',
                b'{"message": "test message", "topic": "test"}',
                hostname='testhost',
                port=1883
            )

    # standard test using query string for api key
    with mock.patch.dict('os.environ', {
        'API_KEY': 'foo',
        'MQTT_HOST': 'testhost',
        'MQTT_PORT': '1883',
    }):
        with mock.patch('paho.mqtt.publish.single') as mock_publish_single:
            rv = client.post(
                '/',
                headers={'Content-Type': 'application/json'},
                json={'topic': 'test', 'message': 'test message'},
                query_string={'api_key': 'asdf'}
            )
            assert rv.status_code == 401
            assert not mock_publish_single.called

            rv = client.post(
                '/',
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                data='topic=test&message=test+message',
                query_string={'api_key': 'foo'}
            )
            assert rv.status_code == 200
            assert not mock_publish_single.called

            rv = client.post(
                '/',
                headers={'Content-Type': 'application/json'},
                json={'topic': 'test', 'message': 'test message'},
                query_string={'api_key': 'foo'}
            )
            assert rv.status_code == 200
            mock_publish_single.assert_called_once_with(
                'test',
                b'{"message": "test message", "topic": "test"}',
                hostname='testhost',
                port=1883
            )
