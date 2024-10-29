#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Additional plot function."""

import webbrowser
from typing import List, Optional

import numpy as np

from .color_picker import ColorPicker
from .generate_html import generate_html
from .utils import js
from .write_html_tempfile import write_html_tempfile


def prepare_data(x, left, right):
    if isinstance(left, np.ndarray) and left.ndim == 1:
        left = [left]
    data = [x, *left]
    if right:
        data.extend(right)
    return data


def add_default_options(opts: dict) -> None:
    if "cursor" not in opts:
        opts["cursor"] = {
            "drag": {
                "x": True,
                "y": True,
                "uni": 50,
            }
        }
    if "plugins" not in opts:
        opts["plugins"] = [
            js("wheelZoomPlugin({factor: 0.75})"),
        ]


def plot2(
    x: np.ndarray,
    left: List[np.ndarray],
    right: Optional[List[np.ndarray]] = None,
    resize: bool = True,
    title: Optional[str] = None,
    time: Optional[bool] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    **kwargs,
) -> None:
    """Plot function with additional defaults and parameters.

    Args:
        x: Values for the x-axis.
        left: Values for the left y-axis.
        right: Values for the (optional) right y-axis.
        resize: If set (default), scale plot to page width and height.
        title: Plot title.
        time: If set, the x-axis is treated as a timestamp.
        width: Plot width in pixels.
        height: Plot height in pixels.
        kwargs: Other keyword arguments are forward to uPlot as options.
    """
    data = prepare_data(x, left, right)

    # Prepare options
    opts = kwargs.copy()
    add_default_options(opts)
    if title is not None:
        opts["title"] = title
    if time is not None:
        opts["scales"] = {"x": {"time": time}}
    if width is not None:
        opts["width"] = width
    if height is not None:
        opts["height"] = height
    if "series" not in opts:
        opts["series"] = [{}]
        color_picker = ColorPicker()
        for series in data[1:]:
            opts["series"].append(
                {
                    "stroke": color_picker.get_next_color(),
                }
            )

    # Generate and open plot
    html = generate_html(opts, data, resize=resize)
    filename = write_html_tempfile(html)
    webbrowser.open_new_tab(filename)