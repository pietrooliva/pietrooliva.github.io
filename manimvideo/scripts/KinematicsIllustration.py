from manim import *
import numpy as np

# ------------------------------------------------
# Imposta la cartella di output
config.media_dir = "/Users/olivap/Desktop/LED/Manim"
# ------------------------------------------------

class KinematicsIllustration(Scene):
    def construct(self):
        # Parametri
        T_max = 4.5            # intervallo di tempo [0, T_max]
        x0     = 4             # posizione iniziale
        v0     = 1.5           # velocità iniziale
        a0     = 2             # accelerazione costante

        # 1. PREPARO LE SCRITTE A DESTRA (non ancora mostrate)
        # Caso A: QUIETE
        boxedA = MathTex(r"\text{Quiete: }x(t)=x_0", font_size=40)\
            .to_edge(RIGHT, buff=1.5).shift(UP * 1.8)
        boxA = SurroundingRectangle(boxedA, buff=0.1)
        eqA1 = MathTex(r"v(t) = \frac{d x}{d t} = 0", font_size=34)\
            .next_to(boxedA, DOWN, buff=0.3).to_edge(RIGHT, buff=2)
        eqA2 = MathTex(r"a(t) = \frac{d v}{d t} = 0", font_size=34)\
            .next_to(eqA1, DOWN, buff=0.2).to_edge(RIGHT, buff=2)

        # Caso B: MOTO RETTILINEO UNIFORME
        boxedB = MathTex(r"\text{Moto Rettilineo Uniforme: }v(t)=v_0", font_size=40)\
            .to_edge(RIGHT, buff=1).shift(UP * 1.8)
        boxB = SurroundingRectangle(boxedB, buff=0.1)
        eqB1 = MathTex(r"x(t) = \int v_0\,dt = v_0\,t + x_0", font_size=34)\
            .next_to(boxedB, DOWN, buff=0.3).to_edge(RIGHT, buff=2)
        eqB2 = MathTex(r"a(t) = \frac{d v}{d t} = 0", font_size=34)\
            .next_to(eqB1, DOWN, buff=0.2).to_edge(RIGHT, buff=2)

        # Caso C: MOTO UNIFORMEMENTE ACCELERATO
        boxedC = MathTex(r"\text{Moto Rettilineo Uni.te Accelerato: }a(t)=a_0", font_size=36)\
            .to_edge(RIGHT, buff=0.5).shift(UP * 1.8)
        boxC = SurroundingRectangle(boxedC, buff=0.1)
        eqC1 = MathTex(r"v(t) = \int a_0\,dt = a_0\,t + v_0", font_size=34)\
            .next_to(boxedC, DOWN, buff=0.3).to_edge(RIGHT, buff=2)
        eqC2 = MathTex(r"x(t) = \int v(t)\,dt = \tfrac{1}{2}a_0\,t^2 + v_0\,t + x_0", font_size=34)\
            .next_to(eqC1, DOWN, buff=0.2).to_edge(RIGHT, buff=2)

        # 2. CONFIGURAZIONE DEGLI ASSI (tacche e freccette piccole, includi i tick)
        axes_config = {
            "include_numbers": False,
            "include_ticks": True,
            "include_tip": True,
            "tip_length": 0.03,
            "tip_width": 0.09,
            "tick_size": 0.06
        }

        # Calcolo massimi per non far sconfinare le curve:
        x_max = x0 + v0 * T_max + 0.5 * a0 * T_max**2  # massimo di x(t) in C
        v_max = v0 + a0 * T_max                          # massimo di v(t) in C
        a_max = max(a0, 4)                              # y_range minimo 4

        # Asse x(t): in alto, y_range fino a x_max
        axes_x = Axes(
            x_range=[0, T_max, 1],
            y_range=[0, x_max, x_max / 6],
            x_length=5,
            y_length=2,
            axis_config=axes_config,
            x_axis_config=axes_config,
            y_axis_config=axes_config,
        ).to_edge(LEFT, buff=1).shift(UP * 2.2)

        # Asse v(t): al centro, y_range fino a v_max
        axes_v = Axes(
            x_range=[0, T_max, 1],
            y_range=[0, v_max, v_max / 5],
            x_length=5,
            y_length=2,
            axis_config=axes_config,
            x_axis_config=axes_config,
            y_axis_config=axes_config,
        ).to_edge(LEFT, buff=1).shift(UP * 0.1)

        # Asse a(t): in basso, y_range fino a a_max
        axes_a = Axes(
            x_range=[0, T_max, 1],
            y_range=[0, a_max, 1],
            x_length=5,
            y_length=2,
            axis_config=axes_config,
            x_axis_config=axes_config,
            y_axis_config=axes_config,
        ).to_edge(LEFT, buff=1).shift(DOWN * 2)

        # 3. ETICHETTE DEGLI ASSI (in alto a sinistra, vicino al tip)
        # Calcolo posizione del tip per ogni asse:
        tip_x = axes_x.c2p(0, x_max)  # punto top sul bordo superiore di axes_x
        label_x = MathTex(r"x(t)", font_size=28).next_to(tip_x, UP * (-0.2) + LEFT * 0.5)

        tip_v = axes_v.c2p(0, v_max)
        label_v = MathTex(r"v(t)", font_size=28).next_to(tip_v, UP * (-0.2) + LEFT * 0.5)

        tip_a = axes_a.c2p(0, a_max)
        label_a = MathTex(r"a(t)", font_size=28).next_to(tip_a, UP * (-0.2) + LEFT * 0.5)

        # 4. MOSTRO TUTTI GLI ASSI E LE ETICHETTE
        self.play(
            Create(axes_x), Create(label_x),
            Create(axes_v), Create(label_v),
            Create(axes_a), Create(label_a),
            run_time=2
        )
        self.wait(0.5)

        # 5. CASO A: QUIETE
        # 5.1 Box e formule di A
        self.play(Create(boxA), Write(boxedA), run_time=1)
        self.wait(0.3)
        self.play(Write(eqA1), Write(eqA2), run_time=1)
        self.wait(0.5)

        # 5.2 Intercetta x0: dot e label
        dot_x0 = Dot(axes_x.c2p(0, x0), color=BLUE)
        label_x0 = MathTex(r"x_0", font_size=24).next_to(dot_x0, LEFT, buff=0.1)
        self.play(Create(dot_x0), Write(label_x0), run_time=0.5)
        self.wait(0.2)

        # 5.3 Disegno x(t)=x0 su axes_x
        x_const = axes_x.plot(
            lambda t: x0,
            x_range=[0, T_max],
            color=BLUE,
            stroke_width=5
        )
        self.play(Create(x_const), run_time=2)
        self.wait(0.3)

        # 5.4 Disegno v(t)=0 su axes_v
        v_zero = axes_v.plot(
            lambda t: 0,
            x_range=[0, T_max],
            color=GREEN,
            stroke_width=5
        )
        self.play(Create(v_zero), run_time=1.5)
        self.wait(0.3)

        # 5.5 Disegno a(t)=0 su axes_a
        a_zero = axes_a.plot(
            lambda t: 0,
            x_range=[0, T_max],
            color=RED,
            stroke_width=5
        )
        self.play(Create(a_zero), run_time=1.5)
        self.wait(0.5)

        # 5.6 Rimuovo elementi di A (ma lascio dot_x0 e label_x0)
        self.play(
            *[FadeOut(mob) for mob in [x_const, v_zero, a_zero, boxA, boxedA, eqA1, eqA2]],
            run_time=1
        )
        self.wait(0.5)

        # 6. CASO B: MOTO RETTILINEO UNIFORME
        # 6.1 Box e formule di B
        self.play(Create(boxB), Write(boxedB), run_time=1)
        self.wait(0.3)
        self.play(Write(eqB1), Write(eqB2), run_time=1)
        self.wait(0.5)

        # 6.2 Intercetta v0: dot e label
        dot_v0 = Dot(axes_v.c2p(0, v0), color=GREEN)
        label_v0 = MathTex(r"v_0", font_size=24).next_to(dot_v0, LEFT, buff=0.1)
        self.play(Create(dot_v0), Write(label_v0), run_time=0.5)
        self.wait(0.2)

        # 6.3 Disegno x(t)=x0 + v0*t su axes_x
        x_lin = axes_x.plot(
            lambda t: x0 + v0 * t,
            x_range=[0, T_max],
            color=BLUE,
            stroke_width=5
        )
        self.play(Create(x_lin), run_time=2)
        self.wait(0.3)

        # 6.4 Disegno v(t)=v0 su axes_v
        v_const = axes_v.plot(
            lambda t: v0,
            x_range=[0, T_max],
            color=GREEN,
            stroke_width=5
        )
        self.play(Create(v_const), run_time=1.5)
        self.wait(0.3)

        # 6.5 Disegno a(t)=0 su axes_a
        a_zero2 = axes_a.plot(
            lambda t: 0,
            x_range=[0, T_max],
            color=RED,
            stroke_width=5
        )
        self.play(Create(a_zero2), run_time=1.5)
        self.wait(0.5)

        # 6.6 Rimuovo elementi di B (ma lascio dot_v0 and label_v0)
        self.play(
            *[FadeOut(mob) for mob in [x_lin, v_const, a_zero2, boxB, boxedB, eqB1, eqB2]],
            run_time=1
        )
        self.wait(0.5)

        # 7. CASO C: MOTO UNIFORMEMENTE ACCELERATO
        # 7.1 Box e formule di C
        self.play(Create(boxC), Write(boxedC), run_time=1)
        self.wait(0.3)
        self.play(Write(eqC1), Write(eqC2), run_time=1)
        self.wait(0.5)

        # 7.2 Intercetta a0: dot e label
        dot_a0 = Dot(axes_a.c2p(0, a0), color=RED)
        label_a0 = MathTex(r"a_0", font_size=24).next_to(dot_a0, LEFT, buff=0.1)
        self.play(Create(dot_a0), Write(label_a0), run_time=0.5)
        self.wait(0.2)

        # 7.3 Disegno x(t)=x0 + v0*t + ½ a0*t^2 su axes_x
        x_quad = axes_x.plot(
            lambda t: x0 + v0*t + 0.5*a0*t*t,
            x_range=[0, T_max],
            color=BLUE,
            stroke_width=5
        )
        self.play(Create(x_quad), run_time=2)
        self.wait(0.3)

        # 7.4 Disegno v(t)=v0 + a0*t su axes_v
        v_lin2 = axes_v.plot(
            lambda t: v0 + a0 * t,
            x_range=[0, T_max],
            color=GREEN,
            stroke_width=5
        )
        self.play(Create(v_lin2), run_time=1.5)
        self.wait(0.3)

        # 7.5 Disegno a(t)=a0 su axes_a
        a_const = axes_a.plot(
            lambda t: a0,
            x_range=[0, T_max],
            color=RED,
            stroke_width=5
        )
        self.play(Create(a_const), run_time=1.5)
        self.wait(0.5)

        # 7.6 Non rimuovo i grafici e i testi di C: rimangono visibili

        # 8. FINE
        self.wait(2)