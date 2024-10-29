#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron
# Copyright 2023-2024 Inria

"""Plot time series."""

import tempfile
from datetime import datetime


def write_html_tempfile(html: str) -> str:
    """Write string to an HTML file.

    Args:
        html: HTML content.

    Returns:
        Name of the output temporary file.
    """
    filename: str = ""
    with tempfile.NamedTemporaryFile(
        mode="w+",
        prefix=f"plot-{datetime.now().strftime('%Y%m%d-%H%M%S')}-",
        suffix=".html",
        delete=False,
    ) as output_file:
        output_file.write(html)
        filename = f"file://{output_file.name}"
    return filename
