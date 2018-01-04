# Copyright (c) 2017 James Kerr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import os
import time

from DataBlock import DataBlock
from collections import defaultdict
import pygal

parser = argparse.ArgumentParser(description="Graphing and Analytics tool for OCAT frametime CSV's")
file_parser = parser.add_argument("input", help="Input Dir/File")
output_parser = parser.add_argument("--output", "-o", help="Output Directory", default="")

# graph args
stylesheet_parser = parser.add_argument("--stylesheet", "-s", help="Stylesheet for formatting the SVG", default="")
height_parser = parser.add_argument("--height", "-v", help="Height in Pixels", type=int, default=1080)
width_parser = parser.add_argument("--width", "-w", help="Width in Pixels", type=int, default=1920)
range_parser = parser.add_argument("--range", "-r", help="Y Axis maximum value", type=float, default=30)
range_min_parser = parser.add_argument("--minRange", "-m", help="Y Axis minimum value", type=float, default=0)
delimit_parser = parser.add_argument("--delimiter", "-d", help="Delimiter character", type=str, default=",")
column_parser = parser.add_argument("--column", "-c", help="Column to graph", type=str, default="MsBetweenPresents")
multiplier_parser = parser.add_argument("--multiplier", "-x", help="Multiplier value (translate ns to ms)", type=int,
                                        default=1)
legend_parser = parser.add_argument("--legend", "-l", help="Chart legend", type=str, default="")

# statistical args
median_enabled_parser = parser.add_argument("--stat-median", help="Median", type=bool, default=True)
geo_mean_enabled_parser = parser.add_argument("--stat-geo-mean", help="Geometric Mean", type=bool, default=True)
min_enabled_parser = parser.add_argument("--stat-min", help="Minimum", type=bool, default=True)
std_enabled_parser = parser.add_argument("--stat-std", help="Standard Deviation", type=bool, default=True)
count_below_enabled_parser = parser.add_argument("--stat-below", help="Count Below", type=int, default=16)
p95_enabled_parser = parser.add_argument("--stat-p95", help="95%", type=bool, default=True)
p99_enabled_parser = parser.add_argument("--stat-p99", help="99%", type=bool, default=True)
p999_enabled_parser = parser.add_argument("--stat-p999", help="99.9%", type=bool, default=True)


args = parser.parse_args()

start = time.time()

files_to_process = []  # List of files to process

if os.path.isdir(args.input):
    for root, dirs, files in os.walk(args.input):
        for file in files:
            if file.endswith(".csv"):
                files_to_process.append(root + file)
else:
    with open(args.input) as file:
        if file.name.endswith(".csv"):
            files_to_process.append(args.input)
        else:
            print("Expected .csv")

data_blocks = []

for file in files_to_process:
    data = DataBlock(file, args)
    data.load()
    data.render()
    data_blocks.append(data)
config = pygal.Config()
if args.stylesheet != "":
    config.css.append('file://' + args.stylesheet)

stats_chart = pygal.HorizontalBar(config)

for x in data_blocks:
    stats = x.stats()
    stats_chart.x_labels = stats[1]
    stats_chart.add(x.name(), stats[0])

stats_chart.width = args.width
stats_chart.height = args.height

stats_chart.render_to_file(args.output + "stats.svg")
stats_chart.render_to_png(args.output + "stats.png")


print("Done in " + str(round(time.time() - start, 2)) + "s")
