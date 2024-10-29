#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

import numpy as np

import uplot

if __name__ == "__main__":
    t = np.linspace(0.0, 1.0, 10)
    data = [
        t,
        np.exp(0.42 * t),
    ]
    opts = {
        "width": 1920,
        "height": 600,
        "title": "Simple plot",
        "scales": {
            "x": {
                "time": False,
            },
        },
        "series": [
            {},
            {
                "stroke": "red",
                "fill": "rgba(255,0,0,0.1)",
            },
        ],
    }
    uplot.plot(opts, data)
