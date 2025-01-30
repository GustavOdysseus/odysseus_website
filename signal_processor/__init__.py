# Copyright (c) 2021-2024 Oleg Polakow. All rights reserved.

"""Custom signal generators built with the signal factory.

You can access all the indicators by `vbt.*`."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vectorbtpro.signals.generators.ohlcstcx import *
    from vectorbtpro.signals.generators.ohlcstx import *
    from vectorbtpro.signals.generators.rand import *
    from vectorbtpro.signals.generators.randnx import *
    from vectorbtpro.signals.generators.randx import *
    from vectorbtpro.signals.generators.rprob import *
    from vectorbtpro.signals.generators.rprobcx import *
    from vectorbtpro.signals.generators.rprobnx import *
    from vectorbtpro.signals.generators.rprobx import *
    from vectorbtpro.signals.generators.stcx import *
    from vectorbtpro.signals.generators.stx import *
# Copyright (c) 2021-2024 Oleg Polakow. All rights reserved.

"""Modules for working with signals."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vectorbtpro.signals.accessors import *
    from vectorbtpro.signals.factory import *
    from vectorbtpro.signals.generators import *
    from vectorbtpro.signals.nb import *

__exclude_from__all__ = [
    "enums",
]
# signal_processor/__init__.py
import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
root_dir = str(Path(__file__).parent.resolve())
if root_dir not in sys.path:
    sys.path.append(root_dir)

from typing import Type, Dict, Any, Union, Tuple, List, Optional
import numpy as np
import pandas as pd
from crewai_tools import BaseTool
from pydantic import BaseModel, Field, ConfigDict
import vectorbtpro as vbt