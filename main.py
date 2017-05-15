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
import csv
import time

import os
import pygal

parser = argparse.ArgumentParser(description="Graphing and Analytics tool for OCAT frametime CSV's")
file_parser = parser.add_argument("input", help="Input Dir")
output_parser = parser.add_argument("--output", "-o", help="Output Directory", default="")
stylesheet_parser = parser.add_argument("--stylesheet", "-s", help="Stylesheet for formatting the SVG", default="")
height_parser = parser.add_argument("--height", "-v", help="Height in Pixels", type=int, default=1080)
width_parser = parser.add_argument("--width", "-w", help="Width in Pixels", type=int, default=1920)
range_parser = parser.add_argument("--range", "-r", help="Y Axis maximum value", type=int, default=30)

args = parser.parse_args()

start = time.time()

for file in os.listdir(args.input):
    if ".csv" in file:
        filename = args.input + file

        time_series = []

        with open(filename, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                try:
                    time_series.append(float(row[10]))
                except ValueError as e:
                    pass
        csv_file.close()

        print("Loaded file in " + str(time.time() - start) + "s \r\n Setting up")

        config = pygal.Config()
        if args.stylesheet != "":
            config.css.append('file://' + args.stylesheet)
        chart = pygal.Line(config)

        chart.add("", time_series)  # Legend isn't being rendered so the name doesnt matter TODO: Change this
        chart.width = args.width
        chart.height = args.height
        chart.show_legend = False
        chart.show_dots = False
        chart.range = [0, args.range]
        print("Rendering")

        if args.output != "":
            try:
                os.makedirs(args.output)
            except FileExistsError:
                print("Output dir already exists")
            chart.render_to_file(args.output + os.path.basename(os.path.splitext(filename)[0] + ".svg"))
            # if args.png:
            #     chart.render_to_png(args.output + os.path.basename(os.path.splitext(filename)[0] + ".png"))
        else:
            chart.render_to_file(os.path.splitext(filename)[0] + ".svg")
            # if args.png:
            #     chart.render_to_png(os.path.splitext(filename)[0] + ".svg")

time_between = time.time() - start
print("Completed in {}s".format(time_between))
