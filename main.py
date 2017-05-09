import argparse
import csv
import os
import time

import pygal

parser = argparse.ArgumentParser(description="Graphing and Analytics tool for OCAT frametime CSV's")
file_parser = parser.add_argument("input", help="Input File")
output_parser = parser.add_argument("output", help="Output Directory")
stylesheet_parser = parser.add_argument("--stylesheet", "-s", help="Stylesheet for formatting the SVG")
png_parser = parser.add_argument("--png", "-p", help="PNG Output", type=bool, default=False)
height_parser = parser.add_argument("--height", "-h", help="Height in Pixels", type=int, default=1080)
width_parser = parser.add_argument("--width", "-w", help="Width in Pixels", type=int, default=1920)

args = parser.parse_args()

start = time.time()
time_series = []

with open(args.input, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        try:
            time_series.append(float(row[10]))
        except ValueError as e:
            pass
csv_file.close()

print("Loaded file in " + str(time.time() - start) + "s \r\n Setting up")

config = pygal.Config()
config.css.append('file://' + args.stylesheet)
chart = pygal.Line(config)

chart.add("", time_series)  # Legend isn't being rendered so the name doesnt matter
chart.width = args.width
chart.height = args.height
chart.show_legend = False
chart.show_dots = False
chart.range = [0, 30]
print("Rendering")
output_file = os.path.splitext(args.input)[0] + ".csv"
chart.render_to_file(output_file)

if args.png:
    chart.render_to_png(os.path.splitext(args.input)[0] + ".png")

time_between = time.time() - start
print("Completed in {}s".format(time_between))
