"""Unit tests for CLI API commands."""
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

import requests
from cli.commands import cli


def make_response(status_code, payload):
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = payload

    def raise_for_status():
        if status_code >= 400:
            raise requests.exceptions.HTTPError()
        return None

    response.raise_for_status = raise_for_status
    return response


class TestCliApiCommands:
    def test_api_list_success(self):
        runner = CliRunner()
        payload = {
            'status': 'success',
            'data': {
                'items': [
                    {
                        'id': 'item-1',
                        'name': 'Test Product',
                        'sku': 'TEST-001',
                        'quantity': 5,
                        'price': 10.0,
                        'category': 'Test',
                        'barcode': '1234567890123',
                        'description': 'A test product'
                    }
                ],
                'total': 1,
                'page': 1,
                'per_page': 20,
                'pages': 1
            }
        }

        with patch('cli.commands.requests.request') as mock_request:
            mock_request.return_value = make_response(200, payload)
            result = runner.invoke(cli, ['api', 'list'])

        assert result.exit_code == 0
        assert 'Test Product' in result.output

    def test_api_get_success(self):
        runner = CliRunner()
        payload = {
            'status': 'success',
            'data': {
                'id': 'item-1',
                'name': 'Test Product',
                'sku': 'TEST-001',
                'quantity': 5,
                'price': 10.0,
                'category': 'Test',
                'barcode': '1234567890123',
                'description': 'A test product'
            }
        }

        with patch('cli.commands.requests.request') as mock_request:
            mock_request.return_value = make_response(200, payload)
            result = runner.invoke(cli, ['api', 'get', 'item-1'])

        assert result.exit_code == 0
        assert 'Test Product' in result.output
        assert 'SKU: TEST-001' in result.output

    def test_api_add_success(self):
        runner = CliRunner()
        payload = {
            'status': 'success',
            'data': {
                'id': 'item-2',
                'name': 'New Product'
            }
        }

        with patch('cli.commands.requests.request') as mock_request:
            mock_request.return_value = make_response(201, payload)
            result = runner.invoke(cli, ['api', 'add', 'New Product', 'NEW-001'])

        assert result.exit_code == 0
        assert 'Item created successfully' in result.output
        assert 'New Product' in result.output

    def test_api_update_success(self):
        runner = CliRunner()
        payload = {
            'status': 'success',
            'data': {
                'id': 'item-1',
                'name': 'Test Product'
            }
        }

        with patch('cli.commands.requests.request') as mock_request:
            mock_request.return_value = make_response(200, payload)
            result = runner.invoke(cli, ['api', 'update', 'item-1', '--price', '12.49'])

        assert result.exit_code == 0
        assert 'Item updated successfully' in result.output

    def test_api_delete_success(self):
        runner = CliRunner()
        payload = {'status': 'success', 'message': 'Item deleted'}

        with patch('cli.commands.requests.request') as mock_request:
            mock_request.return_value = make_response(200, payload)
            result = runner.invoke(cli, ['api', 'delete', 'item-1', '--force'])

        assert result.exit_code == 0
        assert 'Item deleted successfully' in result.output

    def test_api_find_success(self):
        runner = CliRunner()
        payload = {
            'status': 'success',
            'data': {
                'items': [
                    {
                        'id': 'item-1',
                        'name': 'Test Product',
                        'sku': 'TEST-001',
                        'quantity': 5,
                        'price': 10.0,
                        'category': 'Test',
                        'barcode': '1234567890123',
                        'description': 'A test product'
                    }
                ],
                'count': 1,
                'query': 'Test'
            }
        }

        with patch('cli.commands.requests.request') as mock_request:
            mock_request.return_value = make_response(200, payload)
            result = runner.invoke(cli, ['api', 'find', 'Test'])

        assert result.exit_code == 0
        assert 'Test Product' in result.output

    def test_api_request_failure(self):
        runner = CliRunner()

        with patch('cli.commands.requests.request') as mock_request:
            mock_request.side_effect = requests.exceptions.RequestException('Connection failed')
            result = runner.invoke(cli, ['api', 'list'])

        assert result.exit_code == 0
        assert 'Error:' in result.output
        assert 'Connection failed' in result.output
