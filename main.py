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

from CSVData import CSVData

parser = argparse.ArgumentParser(description="Graphing and Analytics tool for OCAT frametime CSV's")
file_parser = parser.add_argument("input", help="Input Dir/File")
output_parser = parser.add_argument("--output", "-o", help="Output Directory", default="")
stylesheet_parser = parser.add_argument("--stylesheet", "-s", help="Stylesheet for formatting the SVG", default="")
height_parser = parser.add_argument("--height", "-v", help="Height in Pixels", type=int, default=1080)
width_parser = parser.add_argument("--width", "-w", help="Width in Pixels", type=int, default=1920)
range_parser = parser.add_argument("--range", "-r", help="Y Axis maximum value", type=float, default=30)
range_min_parser = parser.add_argument("--minRange", "-m", help="Y Axis minimum value", type=float, default=0)
delimit_parser = parser.add_argument("--delimiter", "-d", help="Delimiter character", type=str, default=",")
column_parser = parser.add_argument("--column", "-c", help="Column to graph", type=int, default=10)
multiplier_parser = parser.add_argument("--multiplier", "-x", help="Multiplier value (translate ns to ms)", type=int,
                                        default=1)
legend_parser = parser.add_argument("--legend", "-l", help="Chart legend", type=str, default="")

args = parser.parse_args()

start = time.time()

files_to_process = []  # List of files to process

if os.path.isdir(args.input):
    for file in os.listdir(args.input):
        if ".csv" in file:
            files_to_process.append(args.input + file)
else:
    if ".csv" in args.input:
        files_to_process.append(args.input)
    else:
        print("Expected .csv")

data_blocks = []

for file in files_to_process:
    data = CSVData(file, args)
    data.load()
    data.render()
    data_blocks.append(data)

print("Done in " + str(round(time.time() - start, 2)) + "s")
