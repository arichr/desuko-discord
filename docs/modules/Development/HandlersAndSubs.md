# Handlers and subscribers

* **Handlers** are functions that can be "subscribed" by other functions.
* **Subscribers** are functions that have "subscribed" to a handler.

Handlers can have multiple subscribers, and subscribers can bind to multiple handlers.

## Subscribers
```python
def __init__(self, loader):
    # Subscribe a function to desuko.bot.register_slash (the handler).
    # You should always provide a full import path. Relative ones
    # are not supported.
    loader.subscribe('desuko.bot.register_slash', self.sub)

def sub(self):
    print('I will be executed after desuko.bot.register_slash!')
```

!!! warning
    Subscribers are stored in `set`. Thus, they **don't** have an execution order.

## Handlers
*handler_tutorial.py*:
```python
def __init__(self, loader):
    # loader.handler() returns a function that calls a provided one
    # and its subscribers.
    self.handler = loader.handler(self._inner_handler_func)
    loader.subscribe('handler_tutorial.handler', self.sub)

def _inner_handler_func(self):
    print('I will be executed first!')

def sub(self):
    print('I will be executed after self._inner_handler_func()!')
```

**Execution order:**

1. `__init__()`
2. `handler_tutorial.handler()`
3. `self._inner_handler_func()`
4. Subscribers of `handler_tutorial.handler()`

## Asyncronious functions

Subscribers can be asynchronous **only** if their handler is also asynchronous.

```python
def __init__(self, loader):
    self.handler = loader.handler(self._inner_handler_func)
    loader.subscribe('handler_tutorial.handler', self.sub)

def _inner_handler_func(self):
    print('I will be executed first!')

async def sub(self):
    print('I will not be executed at all!')
```
*...will raise an exception.*

```python
def __init__(self, loader):
    self.handler = loader.handler(self._inner_handler_func, return_async=True)
    loader.subscribe('handler_tutorial.handler', self.sub)

async def _inner_handler_func(self):
    print('I will be executed first!')

async def sub(self):
    print('I will be executed after self._inner_handler_func()!')
```
*...will execute normally.*

!!! note
    To work with asynchronous handlers, specify `return_async=True` when creating them.
