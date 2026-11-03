"""One module per topic; every module in this folder is imported, its @marker functions register themselves."""
import importlib
import os
import pkgutil

for _m in sorted(m.name for m in pkgutil.iter_modules([os.path.dirname(__file__)])):
    importlib.import_module(f"{__name__}.{_m}")
