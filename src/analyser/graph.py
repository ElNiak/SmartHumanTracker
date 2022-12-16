import matplotlib.pyplot as plt


class Graph:

    def __init__(self, data, leg_x, leg_y, title, is_plot, legend):
        """
        :param data:
        :param leg_x: legend axis x
        :param leg_y: legend axis y
        :param title:
        :param is_plot:
        """
        self.data = data
        self.leg_x = leg_x
        self.leg_y = leg_y
        self.legend = legend
        self.is_plot = is_plot
        self.x_val = [x[0] for x in data]
        self.y_val = [x[1] for x in data]
        self.plt = plt
        # figsize 14,14 for better quality
        self.fig = self.plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111)
        self.ax.grid()
        self.plt.title(title)
        self.plt.xlabel(leg_x)
        self.plt.ylabel(leg_y)

    def create_graph(self):
        """
        :return: create the graph must be call after create the object
        """
        if self.is_plot:
            self.ax.plot(self.x_val, self.y_val, label=self.legend)
        else:
            self.ax.scatter(self.x_val, self.y_val, label=self.legend)

    def add_data(self, data, legend):
        x_val = [x[0] for x in data]
        y_val = [x[1] for x in data]
        if self.is_plot:
            self.ax.plot(x_val, y_val, label=legend)
        else:
            self.ax.scatter(x_val, y_val, label=legend)

    def add_vertical_line(self, list_vertical, legend):
        """
        :param legend:
        :param list_vertical:
        :return: create and show the graph
        """
        for xv in list_vertical:
            self.ax.axvline(xv, color='r', linestyle='--')

    def add_area(self, list_interval, color, hatch):

        if color == "blue":
            min = 1
            max = 0.95
        else:
            min = 0.95
            max = 0.9

        for xv in list_interval:
            self.ax.axvspan(xv[0], xv[1], ymin=min, ymax=max, alpha=0.5, facecolor = color)

    def show_graph(self):
        """
        Show the graph after its creation
        :return:
        """
        self.fig.legend(loc="upper left")
        self.plt.show()
