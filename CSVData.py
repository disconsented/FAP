import csv
import os

import pygal


class CSVData:
    x_axis = []
    time_series = []
    file_name = ""
    total_time = 0
    args = None

    def __init__(self, file_path, args):
        self.args = args
        self.file_name = file_path

    def load(self):
        with open(self.file_name, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=self.args.delimiter)
            for row in reader:
                try:
                    self.time_series.append(float(row[self.args.column]) * self.args.multiplier)
                    self.total_time += float(row[self.args.column])
                    self.x_axis.append(float(row[9]))
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
            # if self.args.png:
            #     chart.render_to_png(args.output + os.path.basename(os.path.splitext(filename)[0] + ".png"))
        else:
            chart.render_to_file(os.path.splitext(self.file_name)[0] + ".svg")
            # if self.args.png:
            #     chart.render_to_png(os.path.splitext(filename)[0] + ".svg")
