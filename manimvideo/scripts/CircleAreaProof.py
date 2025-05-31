from manim import *
import numpy as np

# ------------------------------------------------
# Imposta la cartella di output
config.media_dir = "/Users/olivap/Desktop/LED/Manim"
# ------------------------------------------------

class CircleAreaProof(Scene):
    def construct(self):
        # Parametri
        R = 2
        N = 16
        angle = 2 * PI / N
        half = N // 2
        base_width = R * angle
        y_bottom = -R / 2
        y_top    = +R / 2

        # 1) Cerchio
        circle = Circle(radius=R, stroke_width=4)
        self.play(Create(circle), run_time=2)

        # 2) Raggio + label
        radius_line  = Line(ORIGIN, RIGHT * R, stroke_width=3)
        radius_label = MathTex("R").next_to(radius_line.get_end() * 1.18, UP * 0.38)
        self.play(Create(radius_line), Write(radius_label), run_time=1)

        # 3) Ispessisco circonferenza + L = 2πR
        length_label = MathTex("L = 2\\pi R").to_corner(UR)
        self.play(circle.animate.set_stroke(width=6), Write(length_label), run_time=1.5)
        self.wait(0.5)

        # 4) Genero i 16 spicchi centrali, colori metà “classici” metà tenui
        sectors = VGroup(*[
            Sector(
                radius=R,
                angle=angle,
                start_angle=i * angle,
                stroke_width=1,
                fill_opacity=0.8,
                fill_color=(
                    BLUE      if i < half and i % 2 == 0 else
                    GREEN     if i < half and i % 2 == 1 else
                    "#ff9999" if (i - half) % 2 == 0   else
                    "#9999ff"
                )
            )
            for i in range(N)
        ])
        self.play(Create(sectors), run_time=2)
        self.wait(0.5)

        # 5) Dispongo la prima metà in basso…
        first_half  = VGroup(*sectors[:half])
        second_half = VGroup(*sectors[half:])
        bottom_positions = [
            np.array([-(PI * R)/2 + (k + 0.5)*base_width, y_bottom, 0])
            for k in range(half)
        ]
        top_positions = [
            np.array([-(PI * R)/2 + k*base_width, y_top, 0])
            for k in range(half)
        ]
        self.play(*[
            first_half[k].animate
                         .rotate(-PI/2 - (k * angle + angle/2))
                         .move_to(bottom_positions[k])
            for k in range(half)
        ], run_time=3)
        self.wait(0.3)

        # …il cerchio e il raggio spariscono
        self.play(FadeOut(circle), FadeOut(radius_line), FadeOut(radius_label), run_time=1)
        self.wait(0.3)

        # dispongo la seconda metà in alto e la faccio cadere
        self.play(*[
            second_half[k].animate
                          .rotate(PI/2 - ((half + k) * angle + angle/2))
                          .move_to(top_positions[k])
            for k in range(half)
        ], run_time=3)
        self.play(*[
            second_half[k].animate.shift(DOWN * R)
            for k in range(half)
        ], run_time=2)
        self.wait(0.5)

        # 6) Etichette b e h (rimangono sempre in scena)
        b_label = MathTex("b = \\pi R").next_to(first_half, DOWN, buff=0.2)
        h_label = MathTex("h = R")\
                      .next_to(VGroup(first_half, second_half), RIGHT, buff=0.2)\
                      .rotate(PI/2)
        self.play(Write(b_label), Write(h_label), run_time=1)
        self.wait(1)

        # 7) A = b·h → πR·R → πR² in alto a sinistra
        eq1 = MathTex("A", "=", "b", "\\times", "h").scale(1.2).to_corner(UL)
        eq2 = MathTex("A", "=", "\\pi R", "\\times", "R").scale(1.2).to_corner(UL)
        eq3 = MathTex("A", "=", "\\pi R^2").scale(1.2).to_corner(UL)
        self.play(Write(eq1), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(eq1, eq2), run_time=1.5)
        self.wait(1)
        self.play(TransformMatchingTex(eq2, eq3), run_time=1)
        self.wait(1.5)

        # 8) Demo: N = 32 → 48 → 56 → 112 → 224
        demo_text = MathTex(r"N = 32 \to 48 \to 56 \to 112 \to 224").to_corner(DR)
        self.play(Write(demo_text), run_time=1)

        sectors_old = sectors
        for idx, new_N in enumerate([32, 48, 56, 112, 224]):
            new_angle      = 2 * PI / new_N
            new_half       = new_N // 2
            new_base_width = R * new_angle

            # rimuovo il rettangolo precedente
            self.play(FadeOut(sectors_old), run_time=0.5)

            # genero i nuovi spicchi
            sectors = VGroup(*[
                Sector(
                    radius=R,
                    angle=new_angle,
                    start_angle=i * new_angle,
                    stroke_width=1,
                    fill_opacity=0.8,
                    fill_color=(
                        BLUE      if i < new_half and i % 2 == 0 else
                        GREEN     if i < new_half and i % 2 == 1 else
                        "#ff9999" if (i - new_half) % 2 == 0   else
                        "#9999ff"
                    )
                )
                for i in range(new_N)
            ])

            # disposizioni
            bpos = [
                np.array([-(PI * R)/2 + (k + 0.5)*new_base_width, y_bottom, 0])
                for k in range(new_half)
            ]
            tpos = [
                np.array([-(PI * R)/2 + k*new_base_width,      y_top,    0])
                for k in range(new_half)
            ]

            # disegno e disposizione
            self.play(Create(sectors), run_time=1.5)
            self.play(
                *[
                    sectors[k].animate
                              .rotate(-PI/2 - (k * new_angle + new_angle/2))
                              .move_to(bpos[k])
                    for k in range(new_half)
                ] + [
                    sectors[new_half + k].animate
                              .rotate(PI/2 - ((new_half + k) * new_angle + new_angle/2))
                              .move_to(tpos[k])
                              .shift(DOWN * R)
                    for k in range(new_half)
                ],
                run_time=3
            )

            # mantengo visibile per 2s
            self.wait(2)

            sectors_old = sectors

        # 9) L’ultimo rettangolo (N=224) resta a schermo più a lungo
        self.wait(3)