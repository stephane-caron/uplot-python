#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Main plot function."""

import webbrowser
from typing import Iterable, List

from .generate_html import generate_html
from .write_html_tempfile import write_html_tempfile


def plot(opts: dict, data: List[Iterable]) -> None:
    html = generate_html(opts, data)
    filename = write_html_tempfile(html)
    webbrowser.open_new_tab(filename)
