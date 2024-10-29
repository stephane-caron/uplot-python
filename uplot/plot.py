#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Main plot function."""

import webbrowser
from typing import Iterable, List

from .generate_html import generate_html
from .write_html_tempfile import write_html_tempfile


def plot(opts: dict, data: List[Iterable]) -> None:
    """Plot function with the same API as uPlot's `plot`.

    Args:
        opts: Options dictionary, as expected by uPlot.
        data: List of series, as expected by uPlot.
    """
    html = generate_html(opts, data, autoscale=False)
    filename = write_html_tempfile(html)
    webbrowser.open_new_tab(filename)
