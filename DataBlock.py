import csv
import os

import pygal
import numpy


class DataBlock:
    x_axis = []
    time_series = []
    file_name = ""
    total_time = 0
    args = None
    column_ms_between = 0
    column_total_time = 0

    def __init__(self, file_path, args):
        self.args = args
        self.file_name = file_path

    def name(self):
        split = self.file_name.split("/")
        return os.path.splitext(split[len(split)-1])[0].replace("_", " ")

    def load(self):
        with open(self.file_name, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=self.args.delimiter)
            for row in reader:
                if reader.line_num == 1:
                    self.column_ms_between = row.index(self.args.column)
                    self.column_total_time = row.index('TimeInSeconds')
                else:
                    try:
                        self.time_series.append(float(row[self.column_ms_between]) * self.args.multiplier)
                        self.total_time += float(row[self.column_ms_between])
                        self.x_axis.append(float(row[self.column_total_time]))
                    except ValueError as e:
                        pass
        csv_file.close()

    def render(self):
        config = pygal.Config()
        if self.args.stylesheet != "":
            config.css.append('file://' + self.args.stylesheet)
        config.x_labels_major_every = int(len(self.time_series) / 100)
        config.show_minor_x_labels = False
        config.x_label_rotation = 45

        chart = pygal.Line(config)
        chart.x_labels = self.x_axis

        chart.add(self.args.legend, self.time_series)
        chart.width = self.args.width
        chart.height = self.args.height
        chart.show_legend = False
        chart.show_dots = False
        chart.range = [self.args.minRange, self.args.range]
        print("Rendering from " + self.file_name)

        if self.args.output != "":
            try:
                os.makedirs(self.args.output)
            except FileExistsError:
                print("Output dir already exists")
            chart.render_to_file(self.args.output + os.path.basename(os.path.splitext(self.file_name)[0] + ".svg"))
            chart.render_to_png(self.args.output + os.path.basename(os.path.splitext(self.file_name)[0] + ".png"))
            # if self.args.png:
            #     chart.render_to_png(args.output + os.path.basename(os.path.splitext(filename)[0] + ".png"))
        else:
            chart.render_to_file(os.path.splitext(self.file_name)[0] + ".svg")
            chart.render_to_png(os.path.splitext(self.file_name)[0] + ".png")
            # if self.args.png:
            #     chart.render_to_png(os.path.splitext(filename)[0] + ".svg")

    def geo_mean_overflow(self):
        a = numpy.log(self.time_series)
        return numpy.exp(a.sum()/len(a))

    def quartiles(self):
        quartiles = []
        for quartile in [50, 95, 99, 99.9]:
            quartiles.append(numpy.percentile(self.time_series, quartile))
        return quartiles

    def min(self):
        return min(self.time_series)

    def max(self):
        return max(self.time_series)

    def total(self):
        return len(self.time_series)

    def std(self):
        return numpy.std(self.time_series)

    def variance(self):
        return numpy.var(self.time_series)

    def count_below(self, threshold):
        count = 0
        for frame_time in self.time_series:
            if frame_time > threshold:
                count += 1
        return count
