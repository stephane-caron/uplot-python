#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

import numpy as np

__MAX_INT = np.iinfo(np.int64).max


def array2string(array: np.ndarray) -> str:
    """Get string representation of a NumPy array suitable for uPlot.

    Args:
        array: NumPy array to convert to JavaScript.

    Returns:
        String representation of the array.
    """
    array_str = np.array2string(
        array,
        precision=64,
        separator=",",
        threshold=__MAX_INT,
    )
    return array_str.replace("nan", "null")


def js(code: str) -> str:
    """Wrap a code string so that it is processed as output JavaScript.

    Args:
        code: Code string to wrap.

    Returns:
        Wrapped string.
    """
    return f"<script>{code}</script>"
