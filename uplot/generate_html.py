#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron
# Copyright 2023 Inria

"""Generate an HTML page containing the output plot."""

import json
from datetime import datetime
from importlib import resources
from typing import List

import numpy as np


def __array2string(array: np.ndarray) -> str:
    """Get string representation of a NumPy array suitable for uPlot.

    Args:
        array: NumPy array to convert to JavaScript.

    Returns:
        String representation of the array.
    """
    return np.array2string(array, separator=",").replace("nan", "null")


def generate_html(opts: dict, data: List[np.ndarray], resize: bool) -> str:
    """Generate plot in an HTML page.

    Args:
        opts: uPlot option dictionary.
        data: List of NumPy arrays, one for each series in the plot.

    Returns:
        HTML contents of the page.
    """
    with resources.path("uplot.static", "uPlot.min.css") as path:
        uplot_min_css = path
    with resources.path("uplot.static", "uPlot.iife.js") as path:
        uplot_iife_js = path
    with resources.path("uplot.static", "uPlot.mousewheel.js") as path:
        uplot_mwheel_js = path

    date = datetime.now().strftime("%Y%m%d-%H%M%S")
    title = opts.get("title", f"Plot from {date}")

    data_string = ""
    for array in data:
        data_string += f"""
                {__array2string(array)},"""

    if "class" not in opts:
        opts["class"] = "uplot-chart"
    if resize:
        opts["width"] = 123456789
        opts["height"] = 987654321
    s = json.dumps(opts)
    s = s.replace("123456789", "window.innerWidth - 20")
    s = s.replace("987654321", "window.innerHeight - 20")
    opts_string = s

    html = f"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="{uplot_min_css}">
        <style>
            div.uplot-chart {{
                background-color: white;
                padding: 10px 0px;  // appear in Right Click -> Take Screenshot
            }}
        </style>
    </head>
    <body>
        <script src="{uplot_iife_js}"></script>
        <script src="{uplot_mwheel_js}"></script>
        <script>
            const {{ linear, stepped, bars, spline, spline2 }} = uPlot.paths;

            let data = [{data_string}
            ];

            const lineInterpolations = {{
                linear: 0,
                stepAfter: 1,
                stepBefore: 2,
                spline: 3,
            }};

            const _stepBefore = stepped({{align: -1}});
            const _stepAfter = stepped({{align:  1}});
            const _linear = linear();
            const _spline = spline();

            function paths(u, seriesIdx, idx0, idx1, extendGap, buildClip) {{
                let s = u.series[seriesIdx];
                let interp = s.lineInterpolation;

                let renderer = (
                    interp == lineInterpolations.linear ? _linear :
                    interp == lineInterpolations.stepAfter ? _stepAfter :
                    interp == lineInterpolations.stepBefore ? _stepBefore :
                    interp == lineInterpolations.spline ? _spline :
                    null
                );

                return renderer(
                    u, seriesIdx, idx0, idx1, extendGap, buildClip
                );
            }}

            let opts = {opts_string};
            let uplot = new uPlot(opts, data, document.body);"""
    if resize:
        html += """

            window.addEventListener("resize", e => {
                uplot.setSize({
                    width: window.innerWidth - 20,
                    height: window.innerHeight - 150,
                });
            });"""
    html += """
        </script>
    </body>
</html>"""
    return html
