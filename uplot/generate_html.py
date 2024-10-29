#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron
# Copyright 2023 Inria

"""Generate an HTML page containing the output plot."""

from importlib import resources
from math import isnan
from typing import Dict, Iterable, List

import numpy as np
from numpy.typing import NDArray

from .color_picker import ColorPicker


def __ensure_floats(series: Iterable) -> List[float]:
    return [float(x) for x in series]


def __escape_null(series: Iterable) -> str:
    """Escape undefined values in a series.

    Args:
        series: Series to filter.

    Returns:
        String representation of the series.
    """
    return (
        "["
        + ", ".join(
            map(
                lambda x: (
                    str(int(x))
                    if isinstance(x, bool)
                    else (
                        str(x)
                        if isinstance(x, (int, float)) and not isnan(x)
                        else x if isinstance(x, str) else "null"
                    )
                ),
                series,
            )
        )
        + "]"
    )


def generate_html(
    opts: dict,
    data: List[Iterable[float, int]],
) -> str:
    """Generate plot in an HTML page.

    Returns:
        HTML contents of the page.
    """
    with resources.path("foxplot.uplot", "uPlot.min.css") as path:
        uplot_min_css = path
    with resources.path("foxplot.uplot", "uPlot.iife.js") as path:
        uplot_iife_js = path
    with resources.path("foxplot.uplot", "uPlot.mousewheel.js") as path:
        uplot_mwheel_js = path

    color_picker = ColorPicker()
    right_axis_label = f" {right_axis_unit}" if right_axis_unit else ""
    left_labels = list(left_axis.keys())
    right_labels = list(right_axis.keys())
    labels = left_labels + [r for r in right_labels if r not in left_labels]
    series_from_label = {}
    series_from_label.update(left_axis)
    series_from_label.update(right_axis)
    html = f"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="{uplot_min_css}">
        <style>
            div.my-chart {{
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

            let data = ["""
    for label in data.keys():
        html += f"""
                {__escape_null(data[label])},"""
    html += """
            ];

            const lineInterpolations = {
                linear: 0,
                stepAfter: 1,
                stepBefore: 2,
                spline: 3,
            };

            const _stepBefore = stepped({align: -1});
            const _stepAfter = stepped({align:  1});
            const _linear = linear();
            const _spline = spline();

            function paths(u, seriesIdx, idx0, idx1, extendGap, buildClip) {
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
            }

            let opts = {"""
    html += f"""
                title: "{title}","""
    html += """
                id: "chart1",
                class: "my-chart",
                width: window.innerWidth - 20,
                height: window.innerHeight - 150,
                cursor: {
                    drag: {
                        x: true,
                        y: true,
                        uni: 50,
                    }
                },
                plugins: [
                    wheelZoomPlugin({factor: 0.75})
                ],"""
    html += f"""
                scales: {{
                    x: {{
                        time: {"true" if timestamped else "false"},
                    }},
                }},
                series: ["""
    html += f"""
                    {{
                        value: (self, rawValue) => Number.parseFloat(rawValue -
                        {times[0]}).toPrecision(4),
                    }},"""
    for label in labels:
        html += f"""
                    {{
                        // initial toggled state (optional)
                        show: true,
                        spanGaps: false,

                        // in-legend display
                        label: "{label}","""
        if label in right_labels:
            html += f"""
                        value: (self, rawValue) =>
                            Number.parseFloat(rawValue).toPrecision(2) +
                            "{right_axis_label}",
                        scale: "{right_axis_unit}","""
        else:  # label in left_labels
            html += f"""
                        value: (self, rawValue) =>
                            Number.parseFloat(rawValue).toPrecision(2) +
                            "{left_axis_label}","""
        html += f"""
                        // series style
                        stroke: "{color_picker.get_next_color()}",
                        width: 2 / devicePixelRatio,
                        lineInterpolation: lineInterpolations.stepAfter,
                        paths,
                    }},"""
    html += """
                ],
                axes: [
                    {},
                    {"""
    html += f"""
                        size: {60 + 10 * len({left_axis_label})},
                        values: (u, vals, space) => vals.map(
                            v => v + "{left_axis_label}"
                        ),"""
    html += """
                    },
                    {
                        side: 1,"""
    html += f"""
                        scale: "{right_axis_unit}",
                        size: {60 + 10 * len({right_axis_label})},
                        values: (u, vals, space) => vals.map(
                            v => v + "{right_axis_label}"
                        ),"""
    html += """
                        grid: {show: false},
                    },
                ],
            };

            let uplot = new uPlot(opts, data, document.body);

            // resize with window
            window.addEventListener("resize", e => {
                uplot.setSize({
                    width: window.innerWidth - 20,
                    height: window.innerHeight - 150,
                });
            });
        </script>
    </body>
</html>"""
    return html
