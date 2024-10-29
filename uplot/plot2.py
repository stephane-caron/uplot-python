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


def add_series(
    opts: dict,
    data: List[np.ndarray],
    left_labels: Optional[List[str]],
    right_labels: Optional[List[str]],
) -> None:
    opts["series"] = [{}]
    color_picker = ColorPicker()
    for i, series in enumerate(data[1:]):
        new_series = {
            "show": True,
            "spanGaps": False,
            "stroke": color_picker.get_next_color(),
            "width": js("2 / devicePixelRatio"),
        }

        def find_in_lists(
            i: int,
            left_list: Optional[List[str]],
            right_list: Optional[List[str]],
        ) -> Optional[str]:
            if left_list is not None:
                if i < len(left_list):
                    return left_list[i]
                i -= len(left_labels)
            if right_list is not None and i >= 0:
                return right_list[i]
            return None

        label = find_in_lists(i, left_labels, right_labels)
        if label is not None:
            new_series["label"] = label

        # scale = find_in_lists(i, left_scales, right_scales)
        # if scale is not None:
        #     new_series["scale"] = scale

        new_series["value"] = js(
            "(self, rawValue) => Number.parseFloat(rawValue).toPrecision(2)"
        )

        # Last, we hack the wrapper to append `paths` after "lineInterpolation"
        new_series["lineInterpolation"] = js(
            "lineInterpolations.stepAfter, paths"
        )
        opts["series"].append(new_series)


def plot2(
    x: np.ndarray,
    left: List[np.ndarray],
    right: Optional[List[np.ndarray]] = None,
    resize: bool = True,
    title: Optional[str] = None,
    timestamped: Optional[bool] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    left_labels: Optional[List[str]] = None,
    right_labels: Optional[List[str]] = None,
    **kwargs,
) -> None:
    """Plot function with additional defaults and parameters.

    Args:
        x: Values for the x-axis.
        left: Values for the left y-axis.
        right: Values for the (optional) right y-axis.
        resize: If set (default), scale plot to page width and height.
        title: Plot title.
        timestamped: If set, x-axis values are treated as timestamps.
        width: Plot width in pixels.
        height: Plot height in pixels.
        kwargs: Other keyword arguments are forward to uPlot as options.
    """
    data = prepare_data(x, left, right)

    # Prepare options
    opts = kwargs.copy()
    add_default_options(opts)
    if "id" not in opts:
        opts["id"] = "chart1"
    if title is not None:
        opts["title"] = title
    if timestamped is not None:
        opts["scales"] = {"x": {"time": timestamped}}
    if width is not None:
        opts["width"] = width
    if height is not None:
        opts["height"] = height
    if "series" not in opts:
        add_series(opts, data, left_labels, right_labels)

    # Generate and open plot
    html = generate_html(opts, data, resize=resize)
    filename = write_html_tempfile(html)
    webbrowser.open_new_tab(filename)
