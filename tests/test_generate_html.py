#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Inria

import unittest

import numpy as np

from uplot.generate_html import generate_html


class TestGenerateHtml(unittest.TestCase):
    def setUp(self):
        t = np.linspace(0.0, 1.0, 10)
        self.data = [t, np.exp(0.42 * t)]
        self.t = t

    def test_generate_html(self):
        test_title = "Test plot"
        opts = {
            "width": 1921,
            "height": 601,
            "title": test_title,
            "scales": {"x": {"time": False}},
            "series": [{}, {"stroke": "red"}],
        }
        html = generate_html(
            opts,
            self.data,
            resize=False,
        )
        self.assertIn("1921", html)
        self.assertIn("601", html)
        self.assertIn(test_title, html)

    def test_resize(self):
        opts = {"series": [{}, {"stroke": "red"}]}
        html = generate_html(opts, self.data, resize=True)
        self.assertIn('window.addEventListener("resize', html)
