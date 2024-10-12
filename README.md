Templatr
===

A simple python library used to be able to define a text to send in any format.
It allows you to define your template with a simple object notation and the way to resolve that value from any object and or dict to fill in those values for you.

Table of Contents
---

- [Installation](#installation)
- [Usage](#usage)
- [Contributions](#contributions)
- [Issues](#issues)

[Installation](#table-of-contents)
---

We publish packages to pypi whenver we create a release which happens on merges.

```bash
pip install templatr # install from pypi
```

[Usage](#table-of-contents)
---

In order to begin making templates you can pull in the Template and Variable class and programatically create a template.

```python
from templatr import Template, Variable

template = Template(
    text="{data}"
    variables=[
        Variable(key="data")
    ]
)
```

However if you know the structure of the objects you can also define a yaml file like this.

```yaml
# template.yml
text: |
    Some template that has a variable {x}
variables:
    - key: x
      path: path.to.value
```

Then load it up either with your own yaml library or use the built in `load_yaml_template` function

```python
from templatr import load_yaml_template

template = load_yaml_template("path/to/yaml/file")

# or...
with open("path/to/yaml/file", "r") as fp:
    template = load_yaml_template(fp)
```

Using a template is as easy as `format(some_data)`

```python
template = ... # however you want to make your template
data = {} # but could also be a popo (plain old python object)

text = template.format(data)  # Fill out text template with data.

# do whatever you want with text.
```

While this is a simple use case the value comes from the `VariableFormatter` class that you can implement to define how you want to format values from the object. i.e. list of items and join them with a comma easily into a template

```python
from templatr import Template, Variable
from templatr.formatters import ListFormatter

template = Template(
    text="Here are the items of the day:\n{items}",
    variables=[
        Variable(
            key="items",
            formatter=ListFormatter(
                seperator=", "
            )
        )
    ]
)

data = {"items": ["Mac N Cheese", "Pizza Pie"]}

text = template.format(data) 
"""
text contains:
Here are the items of the day:
Mac N Cheese, Pizza Pie
"""
```

If you have some custom behavior for what you want to do with you can create your own VariableFormatter objects by implmenting the format method.

```python
# module.py
from templatr.formatter import VariableFormatter
import math
class CustomFormatter(VariableFormatter):
    def format(self, value: float):
        # do whatever you want to transform the value you expect for it.
        return math.round(value)
```

Then you can import and use that formatter with a template like this: 

```yaml
# template.yaml
text: |
    Some template that uses the formatter: {value}
variables:
    - key: value
      path: some.value
      formatter:
        cls: module.CustomFormatter
```

If you formatter has args and or kwargs you can just pass them through the same template
```yaml
# ... template text and other variables
    - key: field
      path: some.field
      formatter:
        cls: module.CustomFormatterWithArgs
        args:
            - First Arg
    - key: other_field
      path: other.field
      formatter:
        cls: module.CustomFormatterWithKwargs
        kwargs: 
            key: arg
```

This will create your formatter correctly dynamically and load it from the fully qualified module that you specified similar to the behavior of the log configuration.

[Contributions](#table-of-contents)
---

If you would like to contribute please fork the repo and refer to the docs on styling and coding principles. We will try our best to look at them as soon as we can and notify you when we merge. All PR's require our code to remain at least 90% code coverage and we have a tool that will post to your pr how much code coverage your branch is currently at.

There is also a python code security scanner that we use called bandit that will give you a rundown of what concerns your code might have from a security perspective.

Beyond that we have a labeler that will automagically apply labels to your pr based on its name/what files that you have modified.


[Issues](#templatr)
---

If you have any issues please feel free to use any of our templates to open one up and we will try to get to them as soon as we can. We love any feedback and want to help empower you however we can.