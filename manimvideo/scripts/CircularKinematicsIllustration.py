from manim import *
import numpy as np

# ------------------------------------------------
# Imposta la cartella di output
config.media_dir = "/Users/olivap/Desktop/LED/Manim"
# ------------------------------------------------

class CircularKinematicsIllustration(Scene):
    def construct(self):
        # Parametri
        T_max = 4.5             # intervallo di tempo [0, T_max]
        theta0 = PI / 4         # angolo iniziale (es. 45°)
        omega0 = 1.5            # velocità angolare iniziale
        alpha0 = 0.5            # accelerazione angolare costante

        # 1. PREPARO LE SCRITTE A DESTRA (non mostrate subito)
        # Caso A: QUIETE CIRCOLARE
        boxedA = MathTex(
            r"\text{Quiete: }\theta(t)=\theta_0",
            font_size=40
        ).to_edge(RIGHT, buff=2).shift(UP * 1.8)
        boxA = SurroundingRectangle(boxedA, buff=0.1)
        eqA1 = MathTex(
            r"\omega(t) = \frac{d \theta}{d t} = 0",
            font_size=34
        ).next_to(boxedA, DOWN, buff=0.3).to_edge(RIGHT, buff=2)
        eqA2 = MathTex(
            r"\alpha(t) = \frac{d \omega}{d t} = 0",
            font_size=34
        ).next_to(eqA1, DOWN, buff=0.2).to_edge(RIGHT, buff=2)

        # Caso B: MOTO CIRCOLARE UNIFORME
        boxedB = MathTex(
            r"\text{Moto Circolare Uniforme: }\omega(t)=\omega_0",
            font_size=40
        ).to_edge(RIGHT, buff=0.8).shift(UP * 1.8)
        boxB = SurroundingRectangle(boxedB, buff=0.1)
        eqB1 = MathTex(
            r"\theta(t) = \int \omega_0\,dt = \omega_0\,t + \theta_0",
            font_size=34
        ).next_to(boxedB, DOWN, buff=0.3).to_edge(RIGHT, buff=2)
        eqB2 = MathTex(
            r"\alpha(t) = \frac{d \omega}{d t} = 0",
            font_size=34
        ).next_to(eqB1, DOWN, buff=0.2).to_edge(RIGHT, buff=2)

        # Caso C: MOTO CIRCOLARE UNIFORMEMENTE ACCELERATO
        boxedC = MathTex(
            r"\text{Moto Circolare Uni.te Accelerato: }\alpha(t)=\alpha_0",
            font_size=36
        ).to_edge(RIGHT, buff=0.5).shift(UP * 1.8)
        boxC = SurroundingRectangle(boxedC, buff=0.1)
        eqC1 = MathTex(
            r"\omega(t) = \int \alpha_0\,dt = \alpha_0\,t + \omega_0",
            font_size=34
        ).next_to(boxedC, DOWN, buff=0.3).to_edge(RIGHT, buff=2)
        eqC2 = MathTex(
            r"\theta(t) = \int \omega(t)\,dt = \tfrac{1}{2}\,\alpha_0\,t^2 + \omega_0\,t + \theta_0",
            font_size=34
        ).next_to(eqC1, DOWN, buff=0.2).to_edge(RIGHT, buff=2)

        # 2. CONFIGURAZIONE DEGLI ASSI (tacche e freccette piccole, includi i tick)
        axes_config = {
            "include_numbers": False,
            "include_ticks": True,
            "include_tip": True,
            "tip_length": 0.02,
            "tip_width": 0.08,
            "tick_size": 0.04,
        }

        # Calcolo massimi per non far sconfinare le curve:
        theta_max = theta0 + omega0 * T_max + 0.5 * alpha0 * T_max**2
        omega_max = omega0 + alpha0 * T_max

        # Asse θ(t): in alto, y_range fino a theta_max
        axes_theta = Axes(
            x_range=[0, T_max, 1],
            y_range=[0, theta_max, theta_max / 6],  # 6 tacche verticali
            x_length=5,
            y_length=2,
            axis_config=axes_config,
            x_axis_config=axes_config,
            y_axis_config=axes_config,
        ).to_edge(LEFT, buff=1).shift(UP * 2.2)

        # Asse ω(t): al centro, y_range fino a omega_max
        axes_omega = Axes(
            x_range=[0, T_max, 1],
            y_range=[0, omega_max, omega_max / 5],  # 5 tacche verticali
            x_length=5,
            y_length=2,
            axis_config=axes_config,
            x_axis_config=axes_config,
            y_axis_config=axes_config,
        ).to_edge(LEFT, buff=1).shift(UP * 0.1)

        # Asse α(t): in basso, y_range fino a 2*alpha0 con step = alpha0
        axes_alpha = Axes(
            x_range=[0, T_max, 1],
            y_range=[0, alpha0 * 2, alpha0],  # tacche a 0, α0, 2α0
            x_length=5,
            y_length=2,
            axis_config=axes_config,
            x_axis_config=axes_config,
            y_axis_config=axes_config,
        ).to_edge(LEFT, buff=1).shift(DOWN * 2)

        # 3. ETICHETTE DEGLI ASSI (in alto a sinistra, vicino al tip)
        # Calcolo posizione del tip per ogni asse:
        tip_theta = axes_theta.c2p(0, theta_max)  # punto top sul bordo superiore
        label_theta = MathTex(r"\theta(t)", font_size=28).next_to(tip_theta, UP * (-0.2) + LEFT * 0.5)

        tip_omega = axes_omega.c2p(0, omega_max)
        label_omega = MathTex(r"\omega(t)", font_size=28).next_to(tip_omega, UP * (-0.2) + LEFT * 0.5)

        tip_alpha = axes_alpha.c2p(0, alpha0 * 2)
        label_alpha = MathTex(r"\alpha(t)", font_size=28).next_to(tip_alpha, UP * (-0.2) + LEFT * 0.5)

        # 4. MOSTRO TUTTI GLI ASSI E LE ETICHETTE
        self.play(
            Create(axes_theta), Create(label_theta),
            Create(axes_omega), Create(label_omega),
            Create(axes_alpha), Create(label_alpha),
            run_time=2
        )
        self.wait(0.5)

        # 5. CASO A: QUIETE CIRCOLARE
        # 5.1 Box e formule di A
        self.play(Create(boxA), Write(boxedA), run_time=1)
        self.wait(0.3)
        self.play(Write(eqA1), Write(eqA2), run_time=1)
        self.wait(0.5)

        # 5.2 Intercetta θ0: dot e label
        dot_theta0 = Dot(axes_theta.c2p(0, theta0), color=BLUE)
        label_theta0 = MathTex(r"\theta_0", font_size=24).next_to(dot_theta0, LEFT, buff=0.1)
        self.play(Create(dot_theta0), Write(label_theta0), run_time=0.5)
        self.wait(0.2)

        # 5.3 Disegno θ(t)=θ0 su axes_theta
        theta_const = axes_theta.plot(
            lambda t: theta0,
            x_range=[0, T_max],
            color=BLUE,
            stroke_width=5
        )
        self.play(Create(theta_const), run_time=2)
        self.wait(0.3)

        # 5.4 Disegno ω(t)=0 su axes_omega
        omega_zero = axes_omega.plot(
            lambda t: 0,
            x_range=[0, T_max],
            color=GREEN,
            stroke_width=5
        )
        self.play(Create(omega_zero), run_time=1.5)
        self.wait(0.3)

        # 5.5 Disegno α(t)=0 su axes_alpha
        alpha_zero = axes_alpha.plot(
            lambda t: 0,
            x_range=[0, T_max],
            color=RED,
            stroke_width=5
        )
        self.play(Create(alpha_zero), run_time=1.5)
        self.wait(0.5)

        # 5.6 Rimuovo elementi di A (ma lascio dot_theta0 e label_theta0)
        self.play(
            *[FadeOut(mob) for mob in [theta_const, omega_zero, alpha_zero, boxA, boxedA, eqA1, eqA2]],
            run_time=1
        )
        self.wait(0.5)

        # 6. CASO B: MOTO CIRCOLARE UNIFORME
        # 6.1 Box e formule di B
        self.play(Create(boxB), Write(boxedB), run_time=1)
        self.wait(0.3)
        self.play(Write(eqB1), Write(eqB2), run_time=1)
        self.wait(0.5)

        # 6.2 Intercetta ω0: dot e label
        dot_omega0 = Dot(axes_omega.c2p(0, omega0), color=GREEN)
        label_omega0 = MathTex(r"\omega_0", font_size=24).next_to(dot_omega0, LEFT, buff=0.1)
        self.play(Create(dot_omega0), Write(label_omega0), run_time=0.5)
        self.wait(0.2)

        # 6.3 Disegno θ(t)=θ0 + ω0·t su axes_theta
        theta_lin = axes_theta.plot(
            lambda t: theta0 + omega0 * t,
            x_range=[0, T_max],
            color=BLUE,
            stroke_width=5
        )
        self.play(Create(theta_lin), run_time=2)
        self.wait(0.3)

        # 6.4 Disegno ω(t)=ω0 su axes_omega
        omega_const = axes_omega.plot(
            lambda t: omega0,
            x_range=[0, T_max],
            color=GREEN,
            stroke_width=5
        )
        self.play(Create(omega_const), run_time=1.5)
        self.wait(0.3)

        # 6.5 Disegno α(t)=0 su axes_alpha
        alpha_zero2 = axes_alpha.plot(
            lambda t: 0,
            x_range=[0, T_max],
            color=RED,
            stroke_width=5
        )
        self.play(Create(alpha_zero2), run_time=1.5)
        self.wait(0.5)

        # 6.6 Rimuovo elementi di B (ma lascio dot_omega0 e label_omega0)
        self.play(
            *[FadeOut(mob) for mob in [theta_lin, omega_const, alpha_zero2, boxB, boxedB, eqB1, eqB2]],
            run_time=1
        )
        self.wait(0.5)

        # 7. CASO C: MOTO CIRCOLARE UNIFORMEMENTE ACCELERATO
        # 7.1 Box e formule di C
        self.play(Create(boxC), Write(boxedC), run_time=1)
        self.wait(0.3)
        self.play(Write(eqC1), Write(eqC2), run_time=1)
        self.wait(0.5)

        # 7.2 Intercetta α0: dot e label
        dot_alpha0 = Dot(axes_alpha.c2p(0, alpha0), color=RED)
        label_alpha0 = MathTex(r"\alpha_0", font_size=24).next_to(dot_alpha0, LEFT, buff=0.1)
        self.play(Create(dot_alpha0), Write(label_alpha0), run_time=0.5)
        self.wait(0.2)

        # 7.3 Disegno θ(t)=θ0 + ω0·t + ½·α0·t² su axes_theta
        theta_quad = axes_theta.plot(
            lambda t: theta0 + omega0 * t + 0.5 * alpha0 * t * t,
            x_range=[0, T_max],
            color=BLUE,
            stroke_width=5
        )
        self.play(Create(theta_quad), run_time=2)
        self.wait(0.3)

        # 7.4 Disegno ω(t)=ω0 + α0·t su axes_omega
        omega_lin2 = axes_omega.plot(
            lambda t: omega0 + alpha0 * t,
            x_range=[0, T_max],
            color=GREEN,
            stroke_width=5
        )
        self.play(Create(omega_lin2), run_time=1.5)
        self.wait(0.3)

        # 7.5 Disegno α(t)=α0 su axes_alpha
        alpha_const = axes_alpha.plot(
            lambda t: alpha0,
            x_range=[0, T_max],
            color=RED,
            stroke_width=5
        )
        self.play(Create(alpha_const), run_time=1.5)
        self.wait(0.5)

        # 7.6 Non rimuovo i grafici e i testi di C: rimangono visibili

        # 8. FINE
        self.wait(2)