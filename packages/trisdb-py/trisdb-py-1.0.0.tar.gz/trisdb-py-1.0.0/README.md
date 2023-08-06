trisdb-py
=========

The Python interface to TrisDb

### Installation
```
sudo pip install trisdb-py
```

### Usage
```python
>>> from trisdb import *

>>> # Connect and insert some data
>>> db = TrisDbConnection('localhost', 1205)
>>> db.create('Alice', 'loves', 'pizza')
>>> db.create('Kate', 'likes', 'football')

>>> # Print all records
>>> result = db.get('*')
>>> for i in result:
>>>    print i['subject'] + '-' + i['predicate'] + '-' + i['object']

>>> # Who likes football?
>>> result = db.gets('*', 'likes', 'football')
>>> for i in result:
>>>    print i

>>> # Batch insert using MULTI
>>> m = db.multi()
>>> for i in range(0,10):
>>>     m.create('key'+str(i), 'value', 'value'+str(i))
>>> db.execute(m)

>>> # Clear all data from DB and close connection
>>> db.clear()
>>> db.close()
```
