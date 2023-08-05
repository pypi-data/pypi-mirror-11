# zaim
Python bindings for the Zaim API

# How to use
For functions that require no authentication
```python
>>> import zaim
>>> api = zaim.Api()
>>> api.account()
```

For functions that require authentication
```python
>>> import zaim
>>> api = zaim.Api(consumer_key='consumer_key',
                   consumer_secret='consumer_secret',
                   access_token='access_token',
                   access_token_secret='access_token_secret')
>>> api.verify()
```

# Test
```
$ cd /path/to/zaim
$ export PYTHONPATH=$PYTHONPATH:/path/to/zaim/zaim
$ python tests/test_zaim.py
```

# Acknowledgements
- A part of the codes is originally from [here](https://github.com/konomae/zaimpy).
