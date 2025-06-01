from manim import *
import numpy as np

# ------------------------------------------------
# Imposta la cartella di output
config.media_dir = "/Users/olivap/Desktop/LED/Manim"
# ------------------------------------------------

class InclinedPlaneForceDecomposition(Scene):
    def construct(self):
        # -------------------------------
        # Parte 1: Piano inclinato senza attrito
        # -------------------------------

        # Titolo iniziale
        title1 = Text("Piano inclinato senza attrito", font_size=48).to_edge(UP)
        self.play(Write(title1), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(title1), run_time=0.5)

        # 1. PARAMETRI
        theta = PI / 6      # angolo di inclinazione (30°)
        g = 9.81            # accelerazione di gravità (valore simbolico)
        length_plane = 6    # lunghezza del piano inclinato

        # 2. DISEGNO DELLA “TERRA” ORIZZONTALE
        ground = Line(LEFT * 4.2, RIGHT * 4.2).to_edge(DOWN)
        ground.set_stroke(width=4, color=GRAY)

        # 3. DISEGNO DEL PIANO INCLINATO
        incline_start = ground.get_start()  # punto sinistro di “ground”
        direction = np.array([np.cos(theta), np.sin(theta), 0])
        incline_end = incline_start + direction * length_plane
        incline = Line(incline_start, incline_end)
        incline.set_stroke(width=6, color=GRAY)

        # 4. DISEGNO DEL BLOCCO (parte dalla cima del piano), con rotazione
        square_side = 1
        block = Square(side_length=square_side, fill_color=BLUE, fill_opacity=0.7, stroke_color=WHITE)
        block.shift(
            incline_end
            + UP * (square_side / 2) * np.sin(theta)
            + LEFT * (square_side / 2) * np.cos(theta)
        )
        block.rotate(theta, about_point=block.get_bottom())

        # 5. MOSTRO TERRA, PIANO E BLOCCO
        self.play(Create(ground), Create(incline), Create(block), run_time=2)
        self.wait(0.5)

        # 6. VETTORE PESO (m·g)
        weight_start = block.get_center()
        weight_end = weight_start + DOWN * 2
        weight_arrow = Arrow(weight_start, weight_end, buff=0, color=RED, stroke_width=4)
        weight_label = MathTex(r"m\,g", font_size=36, color=RED).next_to(weight_end, DOWN, buff=0.2)
        self.play(Create(weight_arrow), Write(weight_label), run_time=1.5)
        self.wait(0.5)

        # 7. SCOMPOSIZIONE DEL VETTORE PESO
        u_parallel = np.array([np.cos(theta), np.sin(theta), 0])   # verso il basso lungo il piano
        u_normal   = np.array([-np.sin(theta),  np.cos(theta), 0]) # verso il piano

        # 7.1 Componente normale: m·g·cosθ
        comp_norm_len = 2
        comp_norm_vec = -u_normal * comp_norm_len
        comp_norm_end = weight_start + comp_norm_vec
        comp_norm_arrow = Arrow(weight_start, comp_norm_end, buff=0, color=ORANGE, stroke_width=4)
        comp_norm_label = MathTex(r"m\,g\cos\theta", font_size=32, color=ORANGE).next_to(
            comp_norm_end, comp_norm_vec / comp_norm_len, buff=0.2
        )
        self.play(Create(comp_norm_arrow), Write(comp_norm_label), run_time=1.5)
        self.wait(0.3)

        # 7.2 Componente parallela: m·g·sinθ
        comp_par_len = 2
        comp_par_vec = -u_parallel * comp_par_len
        comp_par_end = weight_start + comp_par_vec
        comp_par_arrow = Arrow(weight_start, comp_par_end, buff=0, color=YELLOW, stroke_width=4)
        comp_par_label = MathTex(r"m\,g\sin\theta", font_size=32, color=YELLOW).next_to(
            comp_par_end, comp_par_vec / comp_par_len, buff=0.2
        )
        self.play(Create(comp_par_arrow), Write(comp_par_label), run_time=1.5)
        self.wait(0.5)

        # 8. SCOMPARE m·g
        self.play(FadeOut(weight_arrow), FadeOut(weight_label), run_time=1)
        self.wait(0.3)

        # 9. REAZIONE VINCOLARE N: coda tangente a weight_start
        N_len = comp_norm_len
        N_vec = u_normal * N_len
        N_arrow = Arrow(weight_start, weight_start + N_vec, buff=0, color=ORANGE, stroke_width=4)
        N_label = MathTex(r"N", font_size=32, color=ORANGE).next_to(
            weight_start + N_vec, UP + RIGHT * 0.2, buff=0.1
        )
        self.play(Create(N_arrow), Write(N_label), run_time=1)
        self.wait(0.3)

        # 10. SCOMPARE N e m·g·cosθ
        self.play(
            FadeOut(N_arrow),
            FadeOut(N_label),
            FadeOut(comp_norm_arrow),
            FadeOut(comp_norm_label),
            run_time=1
        )
        self.wait(0.5)

        # 11. EQUAZIONE DI MOTO: m·g·sinθ = m·a
        eq1 = MathTex(r"m\,g\sin\theta = m\,a", font_size=36).to_edge(RIGHT, buff=1).shift(DOWN * 0.5)
        self.play(Write(eq1), run_time=1)
        self.wait(0.5)

        # 12. SEMPLIFICAZIONE: a = g·sinθ (rimane fissa)
        eq2 = MathTex(r"a = g\sin\theta", font_size=40).move_to(eq1)
        self.play(TransformMatchingTex(eq1, eq2), run_time=1.5)
        self.wait(0.3)

        # 13. FORMULE INTEGRATE IMMEDIATE
        v_eq = MathTex(r"v(t) = g\sin\theta\,t", font_size=36).next_to(eq2, DOWN, buff=0.3)
        x_eq = MathTex(r"x(t) = \tfrac{1}{2}\,g\sin\theta\,t^2", font_size=36).next_to(v_eq, DOWN, buff=0.3)
        self.play(Write(v_eq), Write(x_eq), run_time=1)
        self.wait(0.3)

        # 14. ANIMAZIONE DEL BLOCCO CHE SCIVOLA CON a = g·sinθ
        t_final = np.sqrt(2 * length_plane / (g * np.sin(theta)))
        initial_center = block.get_center()

        def update_block(mob):
            t_val = t_tracker.get_value()
            s = -0.5 * g * np.sin(theta) * t_val**2
            new_pos = initial_center + u_parallel * s
            mob.move_to(new_pos)

        t_tracker = ValueTracker(0)
        block.add_updater(update_block)
        self.play(t_tracker.animate.set_value(t_final), run_time=3)
        block.remove_updater(update_block)
        self.wait(1)

        # 15. SCOMPAIONO LE SCRITTE DELLA PARTE 1
        self.play(
            FadeOut(eq2),
            FadeOut(v_eq),
            FadeOut(x_eq),
            run_time=1
        )
        self.wait(0.5)


        # -------------------------------
        # Parte 2: Piano inclinato con attrito
        # -------------------------------

        # 16. ABBANDONA TUTTO (scegliamo di cancellare ogni mobject)
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait(0.5)

        # 17. Titolo per la seconda parte
        title2 = Text("Piano inclinato con attrito", font_size=48).to_edge(UP)
        self.play(Write(title2), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(title2), run_time=0.5)

        # 18. RI-DISEGNO DI TERRA, PIANO E BLOCCO
        ground2 = Line(LEFT * 4.2, RIGHT * 4.2).to_edge(DOWN)
        ground2.set_stroke(width=4, color=GRAY)
        incline2 = Line(ground2.get_start(),
                        ground2.get_start() + np.array([np.cos(theta), np.sin(theta), 0]) * length_plane)
        incline2.set_stroke(width=6, color=GRAY)

        block2 = Square(side_length=square_side, fill_color=BLUE, fill_opacity=0.7, stroke_color=WHITE)
        block2.shift(
            incline2.get_end()
            + UP * (square_side / 2) * np.sin(theta)
            + LEFT * (square_side / 2) * np.cos(theta)
        )
        block2.rotate(theta, about_point=block2.get_bottom())

        self.play(Create(ground2), Create(incline2), Create(block2), run_time=2)
        self.wait(0.5)

        # 19. VETTORE PESO (m·g)
        weight_start2 = block2.get_center()
        weight_end2 = weight_start2 + DOWN * 2
        weight_arrow2 = Arrow(weight_start2, weight_end2, buff=0, color=RED, stroke_width=4)
        weight_label2 = MathTex(r"m\,g", font_size=36, color=RED).next_to(weight_end2, DOWN, buff=0.2)
        self.play(Create(weight_arrow2), Write(weight_label2), run_time=1.5)
        self.wait(0.5)

        # 20. SCOMPOSIZIONE DEL VETTORE PESO
        u_parallel2 = u_parallel
        u_normal2 = u_normal

        comp_norm_vec2 = -u_normal2 * comp_norm_len
        comp_norm_end2 = weight_start2 + comp_norm_vec2
        comp_norm_arrow2 = Arrow(weight_start2, comp_norm_end2, buff=0, color=ORANGE, stroke_width=4)
        comp_norm_label2 = MathTex(r"m\,g\cos\theta", font_size=32, color=ORANGE).next_to(
            comp_norm_end2, comp_norm_vec2 / comp_norm_len, buff=0.2
        )
        self.play(Create(comp_norm_arrow2), Write(comp_norm_label2), run_time=1.5)
        self.wait(0.3)

        comp_par_vec2 = -u_parallel2 * comp_par_len
        comp_par_end2 = weight_start2 + comp_par_vec2
        comp_par_arrow2 = Arrow(weight_start2, comp_par_end2, buff=0, color=YELLOW, stroke_width=4)
        comp_par_label2 = MathTex(r"m\,g\sin\theta", font_size=32, color=YELLOW).next_to(
            comp_par_end2, comp_par_vec2 / comp_par_len, buff=0.2
        )
        self.play(Create(comp_par_arrow2), Write(comp_par_label2), run_time=1.5)
        self.wait(0.5)

        # 21. SCOMPARE m·g
        self.play(FadeOut(weight_arrow2), FadeOut(weight_label2), run_time=1)
        self.wait(0.3)

        # 22. REAZIONE VINCOLARE N E FORZA DI ATTRITO (appaiono insieme)
        N_arrow2 = Arrow(weight_start2, weight_start2 + u_normal2 * N_len, buff=0, color=ORANGE, stroke_width=4)
        N_label2 = MathTex(r"N", font_size=32, color=ORANGE).next_to(
            weight_start2 + u_normal2 * N_len, UP + RIGHT * 0.2, buff=0.1
        )

        mu_d = 0.3
        friction_len = 1.0
        friction_vec2 = u_parallel2 * friction_len
        friction_end2 = weight_start2 + friction_vec2
        friction_arrow2 = Arrow(weight_start2, friction_end2, buff=0, color=BLUE, stroke_width=4)
        friction_label2 = MathTex(r"-\mu_d\,m\,g\cos\theta", font_size=32, color=BLUE).next_to(
            friction_end2, friction_vec2 / friction_len, buff=0.2
        )

        self.play(
            Create(N_arrow2), Write(N_label2),
            Create(friction_arrow2), Write(friction_label2),
            run_time=1.5
        )
        self.wait(0.5)

        # 23. SCOMPARE N e m·g·cosθ
        self.play(
            FadeOut(N_arrow2),
            FadeOut(N_label2),
            FadeOut(comp_norm_arrow2),
            FadeOut(comp_norm_label2),
            run_time=1
        )
        self.wait(0.5)

        # 24. ORA RESTANO SOLO m·g·sinθ E -μ_d m·g·cosθ
        eq_fric1 = MathTex(r"m\,g\sin\theta - \mu_d\,m\,g\cos\theta = m\,a", font_size=36)\
            .to_edge(RIGHT, buff=1).shift(DOWN * 0.5)
        self.play(Write(eq_fric1), run_time=1)
        self.wait(0.5)

        # 25. SEMPLIFICAZIONE: a = g(\sinθ - μ_d cosθ)
        eq_fric2 = MathTex(r"a = g\bigl(\sin\theta - \mu_d\cos\theta\bigr)", font_size=40).move_to(eq_fric1)
        self.play(TransformMatchingTex(eq_fric1, eq_fric2), run_time=1.5)
        self.wait(0.3)

        # 26. FORMULE INTEGRATE: velocità e posizione
        v_eq2 = MathTex(r"v(t) = g\bigl(\sin\theta - \mu_d\cos\theta\bigr)\,t", font_size=36)\
            .next_to(eq_fric2, DOWN, buff=0.3)
        x_eq2 = MathTex(r"x(t) = \tfrac{1}{2}\,g\bigl(\sin\theta - \mu_d\cos\theta\bigr)\,t^2", font_size=36)\
            .next_to(v_eq2, DOWN, buff=0.3)
        self.play(Write(v_eq2), Write(x_eq2), run_time=1)
        self.wait(0.3)

        # 27. ANIMAZIONE DEL BLOCCO CHE SCIVOLA CON a = g( sinθ - μ_d cosθ )
        t_final2 = np.sqrt(2 * length_plane / (g * (np.sin(theta) - mu_d * np.cos(theta))))
        initial_center2 = block2.get_center()

        def update_block_fric(mob):
            t_val = t_tracker_fric.get_value()
            s = -0.5 * g * (np.sin(theta) - mu_d * np.cos(theta)) * t_val**2
            new_pos = initial_center2 + u_parallel2 * s
            mob.move_to(new_pos)

        t_tracker_fric = ValueTracker(0)
        block2.add_updater(update_block_fric)
        self.play(t_tracker_fric.animate.set_value(t_final2), run_time=3)
        block2.remove_updater(update_block_fric)
        self.wait(1)

        # 28. FINE (tutto rimane visibile)
        self.wait(2)