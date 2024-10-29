/*
 * Copyright 2022 Stéphane Caron
 *
 * This file incorporates work covered by the following copyright and permission
 * notice:
 *
 *     Copyright (c) 2021, Leon Sorokin
 *     All rights reserved. (MIT Licensed)
 *
 *     uPlot.js (μPlot)
 *     A small, fast chart for time series, lines, areas, ohlc & bars
 *     https://github.com/leeoniya/uPlot (v1.6.16)
 */

function wheelZoomPlugin(opts) {
    let factor = opts.factor || 0.75;
    let xMin, xMax, yMin, yMax, xRange, yRange;

    function clamp(nRange, nMin, nMax, fRange, fMin, fMax) {
        if (nRange > fRange) {
            nMin = fMin;
            nMax = fMax;
        }
        else if (nMin < fMin) {
            nMin = fMin;
            nMax = fMin + nRange;
        }
        else if (nMax > fMax) {
            nMax = fMax;
            nMin = fMax - nRange;
        }
        return [nMin, nMax];
    }

    return {
        hooks: {
            ready: u => {
                xMin = u.scales.x.min;
                xMax = u.scales.x.max;
                yMin = u.scales.y.min;
                yMax = u.scales.y.max;

                xRange = xMax - xMin;
                yRange = yMax - yMin;

                let over = u.over;
                let rect = over.getBoundingClientRect();

                // wheel drag pan
                over.addEventListener("mousedown", e => {
                    if (e.button == 1) {
                        e.preventDefault();
                        let left0 = e.clientX;
                        let top0 = e.clientY;
                        let scXMin0 = u.scales.x.min;
                        let scXMax0 = u.scales.x.max;
                        let xUnitsPerPx = u.posToVal(1, 'x') - u.posToVal(0, 'x');
                        let scYMin0 = u.scales.y.min;
                        let scYMax0 = u.scales.y.max;
                        let yUnitsPerPx = u.posToVal(1, 'y') - u.posToVal(0, 'y');

                        function onmove(e) {
                            e.preventDefault();
                            let left1 = e.clientX;
                            let dx = xUnitsPerPx * (left1 - left0);
                            let top1 = e.clientY;
                            let dy = yUnitsPerPx * (top1 - top0);
                            u.setScale('x', {
                                min: scXMin0 - dx,
                                max: scXMax0 - dx,
                            });
                            u.setScale('y', {
                                min: scYMin0 - dy,
                                max: scYMax0 - dy,
                            });
                        }

                        function onup(e) {
                            document.removeEventListener("mousemove", onmove);
                            document.removeEventListener("mouseup", onup);
                        }

                        document.addEventListener("mousemove", onmove);
                        document.addEventListener("mouseup", onup);
                    }
                });

                // wheel scroll zoom
                over.addEventListener("wheel", e => {
                    e.preventDefault();

                    let {left, top} = u.cursor;

                    let leftPct = left/rect.width;
                    let btmPct = 1 - top/rect.height;
                    let xVal = u.posToVal(left, "x");
                    let yVal = u.posToVal(top, "y");
                    let oxRange = u.scales.x.max - u.scales.x.min;
                    let oyRange = u.scales.y.max - u.scales.y.min;

                    let nxRange = e.deltaY < 0 ? oxRange * factor : oxRange / factor;
                    let nxMin = xVal - leftPct * nxRange;
                    let nxMax = nxMin + nxRange;
                    [nxMin, nxMax] = clamp(nxRange, nxMin, nxMax, xRange, xMin, xMax);

                    let nyRange = e.deltaY < 0 ? oyRange * factor : oyRange / factor;
                    let nyMin = yVal - btmPct * nyRange;
                    let nyMax = nyMin + nyRange;
                    [nyMin, nyMax] = clamp(nyRange, nyMin, nyMax, yRange, yMin, yMax);

                    u.batch(() => {
                        u.setScale("x", {
                            min: nxMin,
                            max: nxMax,
                        });

                        u.setScale("y", {
                            min: nyMin,
                            max: nyMax,
                        });
                    });
                });
            }
        }
    };
}
