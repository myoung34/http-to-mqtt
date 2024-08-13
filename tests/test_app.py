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
    with mock.patch.dict('os.environ', {}):
      rv = client.get('/')
      assert rv.status_code == 405
    with mock.patch.dict('os.environ', {}):
          rv = client.post('/')
          assert rv.status_code == 401
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