#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron
# Copyright 2023-2024 Inria

"""Plot Python iterables with µPlot."""

__version__ = "0.0.1"

from .plot import plot
from .pyplot import pyplot

__all__ = [
    "plot",
    "pyplot",
]
