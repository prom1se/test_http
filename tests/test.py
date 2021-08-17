import requests
from requests.auth import HTTPBasicAuth


resp = requests.post('http://0.0.0.0:9000/api/upload', auth=HTTPBasicAuth('bad_user', 'some_pwd'))
print(resp.status_code, resp.reason)

base_url = 'http://0.0.0.0:9000/api'
auth = HTTPBasicAuth('test_user', 'test_pwd')
file_hash = '4c2e9e6da31a64c70623619c449a040968cdbea85945bf384fa30ed2d5d24fa3'
print(requests.post(f'{base_url}/upload', auth=auth, data='Some text').content)
print(requests.post(f'{base_url}/upload', auth=auth, data='Some text 22').content)
print(requests.get(f'{base_url}/download', auth=auth, params=file_hash).content)
print(requests.get(f'{base_url}/download', auth=auth, params='ffff').content)
print(requests.delete(f'{base_url}/delete', auth=auth, params=file_hash).reason)
print(requests.delete(f'{base_url}/delete', auth=auth, params='file_hash').reason)
