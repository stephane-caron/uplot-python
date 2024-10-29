#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

import numpy as np
import uplot

if __name__ == "__main__":
    t = np.arange(10)
    uplot.plot(t, np.exp(0.42 * t))
