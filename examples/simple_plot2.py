#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

import numpy as np

import uplot

if __name__ == "__main__":
    t = np.arange(10)
    uplot.plot2(
        t,
        [np.exp(0.1 * t), np.exp(-10.0 * t), np.cos(t)],
        title="Simple plot",
        time=False,
        left_labels=["exp(0.1 t)", "exp(-K t)", "cos(t)"],
    )
