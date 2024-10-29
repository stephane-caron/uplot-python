#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron
# Copyright 2023-2024 Inria

"""Python wrapper for μPlot time series."""

__version__ = "1.0.0"

from .plot import plot
from .plot2 import plot2

__all__ = [
    "plot",
    "plot2",
]
