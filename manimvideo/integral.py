from manim import *

class GraphAreaPlot(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 5],
            y_range=[0, 6],
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            tips=False,
        )

        labels = ax.get_axis_labels()

        curve_1 = ax.plot(lambda x: 4 * x - x ** 2, x_range=[-0.1, 4.1], color=BLUE_C)

        riemann_area = ax.get_riemann_rectangles(curve_1, x_range=[1, 2], dx=0.01, color=BLUE, fill_opacity=0.5)

        self.add(ax, labels, curve_1, riemann_area)
