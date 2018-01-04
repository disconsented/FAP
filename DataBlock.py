import csv
import functools
import os

import pygal
import numpy


class DataBlock:

    def __init__(self, file_path, args):
        self.__args = args
        self.__file_name = file_path
        self.__x_axis = []
        self.__time_series = []
        self.__total_time = 0
        self.__column_ms_between = 0
        self.__column_total_time = 0

    def name(self):
        split = self.__file_name.split("/")
        return os.path.splitext(split[len(split)-1])[0].replace("_", " ")

    def load(self):
        with open(self.__file_name, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=self.__args.delimiter)
            for row in reader:
                if reader.line_num == 1:
                    self.__column_ms_between = row.index(self.__args.column)
                    self.__column_total_time = row.index('TimeInSeconds')
                else:
                    try:
                        self.__time_series.append(float(row[self.__column_ms_between]) * self.__args.multiplier)
                        self.__total_time += float(row[self.__column_ms_between])
                        self.__x_axis.append(float(row[self.__column_total_time]))
                    except ValueError as e:
                        pass
        csv_file.close()

    def render(self):
        config = pygal.Config()
        if self.__args.stylesheet != "":
            config.css.append('file://' + self.__args.stylesheet)
        config.x_labels_major_every = int(len(self.__time_series) / 100)
        config.show_minor_x_labels = False
        config.x_label_rotation = 45

        chart = pygal.Line(config)
        chart.x_labels = self.__x_axis

        chart.add(self.__args.legend, self.__time_series)
        chart.width = self.__args.width
        chart.height = self.__args.height
        chart.show_legend = False
        chart.show_dots = False

        # Attempts to select the range based on .95 + .99 percentile if a range value is not specified
        if self.__args.range > -1:
            chart.range = [self.__args.minRange, self.__args.range]
        else:
            chart.range = [self.min(), self.percentile(.99) + self.percentile(.95)]
        print("Rendering from " + self.__file_name)

        if self.__args.output != "":
            try:
                os.makedirs(self.__args.output)
            except FileExistsError:
                print("Output dir already exists")
            chart.render_to_file(self.__args.output + os.path.basename(os.path.splitext(self.__file_name)[0] + ".svg"))
            chart.render_to_png(self.__args.output + os.path.basename(os.path.splitext(self.__file_name)[0] + ".png"))
            # if self.args.png:
            #     chart.render_to_png(args.output + os.path.basename(os.path.splitext(filename)[0] + ".png"))
        else:
            chart.render_to_file(os.path.splitext(self.__file_name)[0] + ".svg")
            chart.render_to_png(os.path.splitext(self.__file_name)[0] + ".png")
            # if self.args.png:
            #     chart.render_to_png(os.path.splitext(filename)[0] + ".svg")

    @functools.lru_cache(maxsize=128, typed=False)
    def stats(self):
        names = []
        statistics = []

        if self.__args.stat_below > -1:
            names.append("Count Below {}".format(self.__args.stat_below))
            statistics.append(self.count_below(self.__args.stat_below))
        if self.__args.stat_geo_mean:
            names.append("Geometric Mean")
            statistics.append(self.geo_mean_overflow())
        if self.__args.stat_min:
            names.append("Minimum")
            statistics.append(self.min())
        if self.__args.stat_median:
            names.append("Median")
            statistics.append(self.percentile(50))
        if self.__args.stat_p95:
            names.append("95%")
            statistics.append(self.percentile(95))
        if self.__args.stat_p99:
            names.append("99%")
            statistics.append(self.percentile(99))
        if self.__args.stat_p999:
            names.append("99.9%")
            statistics.append(self.percentile(99.9))
        if self.__args.stat_std:
            names.append("Standard Deviation")
            statistics.append(self.std())

        print("{} {} {}".format(self.name(), self.std(), len(self.__time_series)))
        return statistics, names

    @functools.lru_cache(maxsize=128, typed=False)
    def geo_mean_overflow(self):
        a = numpy.log(self.__time_series)
        return numpy.exp(a.sum()/len(a))

    @functools.lru_cache(maxsize=128, typed=False)
    def percentiles(self):
        percentiles = []
        for percentile in [50, 95, 99, 99.9]:
            percentiles.append(numpy.percentile(self.__time_series, percentile))
        return percentiles

    def percentile(self, percentile):
        return numpy.percentile(self.__time_series, percentile)

    @functools.lru_cache(maxsize=128, typed=False)
    def min(self):
        return min(self.__time_series)

    @functools.lru_cache(maxsize=128, typed=False)
    def max(self):
        return max(self.__time_series)

    @functools.lru_cache(maxsize=128, typed=False)
    def total(self):
        return len(self.__time_series)

    @functools.lru_cache(maxsize=128, typed=False)
    def std(self):
        return numpy.std(self.__time_series)

    @functools.lru_cache(maxsize=128, typed=False)
    def variance(self):
        return numpy.var(self.__time_series)

    @functools.lru_cache(maxsize=128, typed=False)
    def count_below(self, threshold):
        count = 0
        for frame_time in self.__time_series:
            if frame_time > threshold:
                count += 1
        return count
