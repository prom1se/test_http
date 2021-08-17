# test_http

for test run server:
```
cd ./test_http/server
export PORT=9000;python api_server.py
```
and in other terminal:
```
cd ./test_http/tests
python test.py
```

expected output:
```
401 User not found
b'4c2e9e6da31a64c70623619c449a040968cdbea85945bf384fa30ed2d5d24fa3'
b'32497c9961b74f5a925cd419a55ed7c38640c77139cb84f19397fc071f05e1f7'
b'Some text'
b''
OK
File not found
```