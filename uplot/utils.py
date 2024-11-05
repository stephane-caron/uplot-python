#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Utility functions."""


def js(code: str) -> str:
    """Wrap a code string so that it is processed as output JavaScript.

    Args:
        code: Code string to wrap.

    Returns:
        Wrapped string.
    """
    return f"<script>{code}</script>"
