#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Main class to manipulate dictionary-series data."""

import logging
import sys
import webbrowser
from typing import BinaryIO, Dict, List, Optional, TextIO, Union

import numpy as np
from numpy.typing import NDArray

from .generate_html import generate_html
from .write_tmpfile import write_tmpfile


def plot(
    self,
    opts: dict,
    data: List[Iterable[float, int]],
) -> None:
    html = generate_html(
        times,
        left_series,
        right_series,
        title,
        left_axis_unit,
        right_axis_unit,
        timestamped=self.__time is not None,
    )
    filename = write_tmpfile(html)
    webbrowser.open_new_tab(filename)
