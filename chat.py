import matplotlib.pyplot as plt


class Trend(object):
    def __init__(self, title, xlabel, ylabel, color='g', linewidth=1, chat='line', bar_width=0.8):
        self.color = color
        self.linewidth = linewidth
        self.bar_width = bar_width
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xcoordinates = None
        self.ycoordinates = None
        self.chat_type = chat

    def get_points(self, rate_dict):
        """
        Parse trend object coordinates from related log's date

        :param rate_dict: certain index dict that comes from Log.get_steps_*_*
        :return: None

        """
        concurrency = sorted(map(lambda key: int(key), rate_dict.keys()))
        trans_rate = []
        for i in concurrency:
            rate = rate_dict[str(i)]
            trans_rate.append(rate)

        self.xcoordinates = concurrency
        self.ycoordinates = trans_rate

def plot_trend(*args):
    """
    Plot trend chat for some testing index

    :param args: trend objects that have got coordinates.
    :return: None
    """
    fig = plt.figure()
    num_trend = len(args)
    i = 1
    for trend in args:
        if trend.title == 'Arrive Rate':
            ax = fig.add_subplot(num_trend, 1, i, ylim=(0.0, 1.1))
        else:
            ax = fig.add_subplot(num_trend, 1, i)
        ax.set_title(trend.title)
        ax.set_xlabel(trend.xlabel)
        ax.set_ylabel(trend.ylabel)
        if trend.chat_type == 'line':
            ax.plot(trend.xcoordinates,
                    trend.ycoordinates,
                    'o-',
                    color=trend.color,
                    linewidth=trend.linewidth)
        elif trend.chat_type == 'bar':
            ax.bar(trend.xcoordinates,
                   trend.ycoordinates,
                   color=trend.color,
                   width=trend.bar_width,
                   align='center',
                   linewidth=trend.linewidth)
        i += 1
    fig.tight_layout()

    plt.show()
