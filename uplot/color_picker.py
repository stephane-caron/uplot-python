#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron
# Copyright 2023-2024 Inria

"""Pick plot colors from a circular list."""

from typing import List


class ColorPicker:
    """Pick from a circular list of color strings."""

    COLORS: List[str] = [
        "red",
        "green",
        "blue",
        "magenta",
        "orange",
        "cyan",
        "purple",
        "lime",
        "#AABBCC",
        "#BBAACC",
        "#CCBBAA",
        "#AABBAA",
    ]

    def __init__(self):
        """Initialize color picker."""
        self.reset()

    def get_next_color(self) -> str:
        """Get next color in the list.

        Returns:
            Color string.
        """
        color = self.COLORS[self.__next_color]
        self.__next_color += 1
        return color

    def reset(self) -> None:
        """Reset picker to the first color."""
        self.__next_color = 0
