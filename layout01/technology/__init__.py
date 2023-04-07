from fnpcell.pdk.technology.all import register_technology
from .tech import TECH as _TECH

get_technology = register_technology(_TECH)
