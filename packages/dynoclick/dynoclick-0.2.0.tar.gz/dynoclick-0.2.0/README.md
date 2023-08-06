## Description

Simple CLI commands loader for [click](http://click.pocoo.org)

## Install

    pip install dyno-click

## Examples

Static modules:

```python
from dynoclick import DynoCli

cli = DynoCli(['test', 'test1'])
cli()
```

Dynamic discovery:

```python
import pip
from dynoclick import DynoCli

modules = [x.key for x in pip.get_installed_distributions()
                       if x.key.startswith('someprefix_')
cli = DynoCli(modules)
cli()

```
