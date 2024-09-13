__version__ = "0.0.0"

from .exceptions import TemplatrException, InvalidFormatter
from .formatter import VariableFormatter, load_formatter
from .template import load_json_template, load_yaml_template, Template
from .variable import Variable

print("Adding fake things")

__all__ = [
    "TemplatrException",
    "InvalidFormatter",
    "VariableFormatter",
    "load_formatter",
    "load_json_template",
    "load_yaml_template",
    "Template",
    "Variable",
]
