import matplotlib.pyplot as plt
plt.style.use('ggplot')

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

BLOCK_HEIGHT = 3
BLOCK_SPACING = 2
GROUP_SPACING = 10

@static_vars(seen={}, count=0)
def simple_color_map(event):
    """A simple color map which returns a new color for each distinct name used."""
    if event.name not in simple_color_map.seen:
        next_col = 'C' + str(simple_color_map.count)
        simple_color_map.count += 1
        simple_color_map.seen[event.name] = next_col
    return simple_color_map.seen[event.name]

def text_color_for(event, color_map):
    """Get the text color for the event from the color map."""
    return color_map(event)

def block_color_for(event, color_map):
    """Get the block color for the event from the color map."""
    return color_map(event)

def mid_point(start, end):
    """Get the midpoint between two values."""
    return float(start + end) / 2

class TimeEvent(object):
    """Simple data object to hold a single time event."""
    def __init__(self, start, end, name, stream, category):
        self.start = start
        self.end = end
        self.name = name
        self.stream = stream
        self.category = category

class TimeLine(object):
    """Class to create and draw a timeline graph of a number of time events."""
    def __init__(self, events):
        self.events = events
        self.categories = set(x.category for x in events)
        self.streams = set(x.stream for x in events)
        self.axes = []
        self.figure = None
        self.stream_map = {}
        self.category_map = {}

    def make_axes(self):
        self.axes = []
        self.figure = plt.figure(figsize=(8, 6), dpi=96)
        n_cats = len(self.categories)
        for i, cat in enumerate(self.categories):
            if i == 0:
                first_axes = self.figure.add_subplot(n_cats, 1, 1)
                new_axes = first_axes
            else:
                new_axes = self.figure.add_subplot(
                    n_cats, 1, i + 1, sharex=first_axes)
            self.category_map[cat] = new_axes
            self.axes += [new_axes]
        return self

    def make_maps(self):
        for i, stream in enumerate(self.streams):
            stream_begin = i * (BLOCK_HEIGHT + BLOCK_SPACING)
            stream_end = stream_begin + BLOCK_HEIGHT
            self.stream_map[stream] = (stream_begin, stream_end)
        return self

    def axes_for(self, event):
        if not self.figure:
            self.make_axes()
        return self.category_map[event.category]

    def stream_dims_for(self, event):
        if not self.stream_map:
            self.make_maps()
        return self.stream_map[event.stream]

    def draw_event(self, event, block_color_map, text_color_map, axes):
        x = [event.start, event.end]
        y1, y2 = self.stream_dims_for(event)
        color = block_color_for(event, block_color_map)
        axes.fill_between(x=x, y1=y1, y2=y2, color=color)

        text_x = mid_point(x[0], x[1])
        text_y = mid_point(y1, y2)
        color = text_color_for(event, text_color_map)
        axes.text(x=text_x, y=text_y, s=event.name, color=color,
                  horizontalalignment='center',
                  verticalalignment='center',
                 )

    def get_yticks(self):
        base_streams = [(name, mid_point(x[0], x[1])) for name, x in
                        self.stream_map.iteritems()]
        names, ticks = zip(*base_streams)
        return names, ticks


def plot_events(events, block_colors, text_colors):
    tl = TimeLine(events)
    tl.make_maps()
    for event in events:
        axes = tl.axes_for(event)
        tl.draw_event(event, block_colors, text_colors, axes)
    names, ticks = tl.get_yticks()
    for i, cat in enumerate(tl.categories):
        axes = tl.category_map[cat]
        axes.set_ylabel(cat)
        axes.set_yticks(ticks)
        axes.set_yticklabels(names)
        if i != len(tl.categories) - 1:
            plt.setp(axes.get_xticklabels(), visible=False)
    return tl.figure

#def plot(x, y, colors, streams, labels, categories):
#    pass

EV = [
    TimeEvent(0, 1, 'name', 'stream1', 'cat1'),
    TimeEvent(0.5, 1.5, 'name2', 'stream2', 'cat1'),
    TimeEvent(1.2, 1.8, 'name3', 'stream1', 'cat1'),
    TimeEvent(2, 4, 'name4', 'stream2', 'cat1'),
    TimeEvent(2, 4, 'name5', 'stream1', 'cat1'),
    TimeEvent(0, 1, 'name', 'stream1', 'cat2'),
    TimeEvent(0.5, 1.5, 'name2', 'stream2', 'cat2'),
    TimeEvent(1.2, 1.8, 'name3', 'stream1', 'cat2'),
    TimeEvent(2, 4, 'name4', 'stream2', 'cat2'),
    TimeEvent(2, 4, 'name5', 'stream1', 'cat2'),
]
plot_events(EV, simple_color_map, lambda x: 'black')
plt.show()
