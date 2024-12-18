#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Plot function with additional defaults and arguments."""

import webbrowser
from typing import List, Optional

import numpy as np

from .color_picker import ColorPicker
from .exceptions import UplotException
from .generate_html import generate_html
from .utils import js
from .write_html_tempfile import write_html_tempfile


def __prepare_data(x, left, right):
    if isinstance(left, np.ndarray) and left.ndim == 1:
        left = [left]
    data = [x, *left]
    if right:
        data.extend(right)
    return data


def __add_default_options(opts: dict) -> None:
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


def __add_series(
    opts: dict,
    data: List[np.ndarray],
    nb_left: int,
    left_labels: Optional[List[str]],
    right_labels: Optional[List[str]],
    time: bool,
) -> None:
    if left_labels is not None and len(left_labels) < nb_left:
        raise UplotException(
            f"Not enough labels in left_labels ({len(left_labels)}) "
            f"to label all {nb_left} left-axis series"
        )

    x_series = {}
    if time:  # set precision of the legend to the millisecond
        x_series["value"] = "{YYYY}-{MM}-{DD} {HH}:{mm}:{ss}.{fff}"

    opts["series"] = [x_series]
    color_picker = ColorPicker()
    for i, _ in enumerate(data[1:]):
        new_series = {
            "show": True,
            "spanGaps": False,
            "stroke": color_picker.get_next_color(),
            "width": js("2 / devicePixelRatio"),
        }

        if left_labels is not None and i < nb_left:
            new_series["label"] = left_labels[i]
        if i >= nb_left:
            if right_labels is not None:
                new_series["label"] = right_labels[i - nb_left]
            new_series["scale"] = "right_axis"

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


def __add_axes(opts: dict) -> None:
    opts["axes"] = [
        {},
        {
            "size": 60,
            "values": js("(u, vals, space) => vals.map(v => v + '')"),
        },
        {
            "grid": {"show": False},
            "scale": "right_axis",
            "side": 1,
            "size": 60,
            "values": js("(u, vals, space) => vals.map(v => v + '')"),
        },
    ]


def plot2(
    x: np.ndarray,
    left: List[np.ndarray],
    right: Optional[List[np.ndarray]] = None,
    resize: bool = True,
    title: Optional[str] = None,
    time: bool = False,
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
        time: If set, x-axis values are treated as timestamps.
        width: Plot width in pixels.
        height: Plot height in pixels.
        left_labels: List of labels for left-axis series.
        right_labels: List of labels for right-axis series.
        kwargs: Other keyword arguments are forward to uPlot as options.
    """
    data = __prepare_data(x, left, right)

    # Prepare options
    opts = kwargs.copy()
    __add_default_options(opts)
    if "id" not in opts:
        opts["id"] = "chart1"
    if title is not None:
        opts["title"] = title
    if time is not None:
        opts["scales"] = {"": {"time": time}}
    if width is not None:
        opts["width"] = width
    if height is not None:
        opts["height"] = height
    if "series" not in opts:
        __add_series(opts, data, len(left), left_labels, right_labels, time)
    if "axes" not in opts:
        __add_axes(opts)

    # Generate and open plot
    html = generate_html(opts, data, resize=resize)
    filename = write_html_tempfile(html)
    webbrowser.open_new_tab(filename)
