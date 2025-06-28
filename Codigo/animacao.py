# Arquivo: animacao.py (Versão Final e Limpa)
from manim import *

# Configurações de cores para consistência
COLOR_Y = BLUE
COLOR_S = GREEN
COLOR_OP = YELLOW
COLOR_RESULT = GOLD

class DQIAlgorithmScene(Scene):
    def construct(self):
        # --- TÍTULO E SETUP INICIAL ---
        title = Text("O Algoritmo DQI em Ação", font_size=48).to_edge(UP)
        problem_eqs = MathTex(r"\text{Problema: }", r"x_1 + x_2 = 0", r",\quad ", r"x_2 + x_3 = 1").next_to(title, DOWN, buff=0.5)
        self.play(Write(title))
        self.play(Write(problem_eqs))
        self.wait(1)

        # Define os registradores que ficarão na tela
        y_register_label = Text("Reg. Erro |y⟩", font_size=24, color=COLOR_Y).to_edge(LEFT, buff=1).shift(UP*1.5)
        y_qubits = VGroup(*[Square(side_length=0.5, color=COLOR_Y) for _ in range(2)]).arrange(RIGHT).next_to(y_register_label, DOWN)
        
        s_register_label = Text("Reg. Síndrome |s⟩", font_size=24, color=COLOR_S).to_edge(LEFT, buff=1).shift(DOWN*1.5)
        s_qubits = VGroup(*[Square(side_length=0.5, color=COLOR_S) for _ in range(3)]).arrange(RIGHT).next_to(s_register_label, DOWN)
        
        self.play(Write(y_register_label), Write(s_register_label))
        self.play(Create(y_qubits), Create(s_qubits))
        self.wait(2)

        # --- PASSO 1: PREPARAÇÃO DO ESTADO INICIAL ---
        self.next_section("Passo 1")
        step1_title = Text("Passo 1: Superposição de Erros", font_size=32).to_edge(UR)
        state_y1 = MathTex(r"|\psi_1\rangle = w_0|00\rangle + \frac{w_1}{\sqrt{2}}(|10\rangle + |01\rangle)", color=COLOR_Y).next_to(y_qubits, RIGHT, buff=0.5)
        
        self.play(Write(step1_title))
        self.play(FadeIn(state_y1, shift=UP))
        self.wait(2)
        # Limpeza do Passo 1
        self.play(FadeOut(step1_title))

        # --- PASSO 2: APLICAR FASE ---
        self.next_section("Passo 2")
        step2_title = Text("Passo 2: Aplicar Fase", font_size=32).to_edge(UR)
        v_vector = MathTex(r"v = \begin{pmatrix} 0 \\ 1 \end{pmatrix}").shift(RIGHT*3.5)
        op_Z = Text("Z", color=COLOR_OP).scale(0.8)

        self.play(Write(step2_title))
        self.play(Write(v_vector))
        self.play(Circumscribe(v_vector[0][3], color=RED))
        self.play(op_Z.animate.move_to(y_qubits[1]))
        self.play(Flash(y_qubits[1], color=COLOR_OP, flash_radius=0.5))
        
        state_y2_text = r"|\psi_2\rangle = w_0|00\rangle + \frac{w_1}{\sqrt{2}}|10\rangle - \frac{w_1}{\sqrt{2}}|01\rangle"
        state_y2 = MathTex(state_y2_text, color=COLOR_Y).move_to(state_y1)
        state_y2.set_color_by_tex("-", RED)
        
        self.play(Transform(state_y1, state_y2), FadeOut(op_Z)) # Transforma o estado e remove o 'Z'
        self.wait(2)
        # Limpeza do Passo 2
        self.play(FadeOut(step2_title), FadeOut(v_vector))

        # --- PASSO 3: CALCULAR SÍNDROME ---
        self.next_section("Passo 3")
        step3_title = Text("Passo 3: Calcular Síndrome s = Bᵀy", font_size=32).to_edge(UR)
        bt_matrix = MathTex(r"B^T = \begin{pmatrix} 1 & 0 \\ 1 & 1 \\ 0 & 1 \end{pmatrix}").shift(RIGHT*3.5, UP*1.5)
        
        self.play(Write(step3_title))
        self.play(FadeIn(bt_matrix))

        cnots = VGroup(
            Arrow(y_qubits[0].get_center(), s_qubits[0].get_center(), buff=0.1, stroke_width=3, color=YELLOW),
            Arrow(y_qubits[0].get_center(), s_qubits[1].get_center(), buff=0.1, stroke_width=3, color=YELLOW),
            Arrow(y_qubits[1].get_center(), s_qubits[1].get_center(), buff=0.1, stroke_width=3, color=YELLOW),
            Arrow(y_qubits[1].get_center(), s_qubits[2].get_center(), buff=0.1, stroke_width=3, color=YELLOW)
        )
        state_s_initial = MathTex("|000\rangle", color=COLOR_S).next_to(s_qubits, RIGHT, buff=0.5)
        
        self.play(FadeIn(state_s_initial))
        self.play(LaggedStart(*[GrowArrow(cnot) for cnot in cnots], lag_ratio=0.5))

        entangled_state_text = VGroup(
            MathTex(r"w_0 |00\rangle_y |000\rangle_s"),
            MathTex(r"+ \frac{w_1}{\sqrt{2}} |10\rangle_y |110\rangle_s"),
            MathTex(r"- \frac{w_1}{\sqrt{2}} |01\rangle_y |011\rangle_s")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7).to_edge(DOWN)
        
        self.play(FadeOut(state_y1, state_s_initial), Write(entangled_state_text)) # Remove estados antigos e escreve o novo
        self.wait(3)
        # Limpeza do Passo 3
        self.play(FadeOut(step3_title), FadeOut(cnots), FadeOut(bt_matrix))

        # --- PASSO 4: DECODIFICAR E DESCOMPUTAR ---
        self.next_section("Passo 4")
        step4_title = Text("Passo 4: Decodificação", font_size=32).to_edge(UR)
        decoder_box = SurroundingRectangle(VGroup(y_qubits, s_qubits), buff=0.5, color=ORANGE)
        decoder_label = Text("Oráculo Decodificador", color=ORANGE, font_size=24).next_to(decoder_box, UP)

        self.play(Write(step4_title))
        self.play(Create(decoder_box), Write(decoder_label))
        
        state_s4 = MathTex(r"|\psi_4\rangle = w_0|000\rangle + \frac{w_1}{\sqrt{2}}|110\rangle - \frac{w_1}{\sqrt{2}}|011\rangle", color=COLOR_S).to_edge(DOWN)
        
        self.play(FadeOut(entangled_state_text), y_qubits.animate.set_opacity(0.3))
        self.play(Write(state_s4))
        self.wait(2)
        # Limpeza do Passo 4
        self.play(FadeOut(step4_title), FadeOut(decoder_box), FadeOut(decoder_label))

        # --- PASSO 5: TRANSFORMADA FINAL E MEDIÇÃO ---
        self.next_section("Passo 5")
        step5_title = Text("Passo 5: Hadamard e Medição", font_size=32).to_edge(UR)
        self.play(Write(step5_title))

        h_gates = VGroup(*[Text("H", color=COLOR_OP).scale(0.8) for _ in s_qubits])
        self.play(LaggedStart(*[h.animate.move_to(q) for h, q in zip(h_gates, s_qubits)]))
        self.play(LaggedStart(*[Flash(q, color=COLOR_OP, flash_radius=0.5) for q in s_qubits]))
        
        # Limpa a tela para o gráfico final
        self.play(FadeOut(h_gates), FadeOut(state_s4), FadeOut(s_register_label), FadeOut(y_register_label), FadeOut(s_qubits), FadeOut(y_qubits.set_opacity(1)))
        
        chart = BarChart(
            values=[1, 8, 1, 1, 1, 1, 8, 1],
            bar_names=["000","001","010","011","100","101","110","111"],
            y_range=[0, 10, 2], y_length=5, x_length=12,
            x_axis_config={"font_size": 24},
        ).move_to(ORIGIN).shift(DOWN*0.5)
        
        chart_label = Text("Probabilidade Relativa de Medição", font_size=24).next_to(chart, UP)
        self.play(Write(chart_label), Create(chart))
        
        correct_solution_1 = SurroundingRectangle(chart.bars[1], color=COLOR_RESULT, buff=0.05)
        correct_solution_2 = SurroundingRectangle(chart.bars[6], color=COLOR_RESULT, buff=0.05)
        self.play(Create(correct_solution_1), Create(correct_solution_2))

        constructive_label = Text("Interferência Construtiva", font_size=24, color=COLOR_RESULT).next_to(chart.bars[1], UP, buff=0.5)
        self.play(Write(constructive_label))

        final_text = Text("Resultado: Alta probabilidade de medir as soluções corretas!", font_size=36, color=GOLD).to_edge(DOWN)
        self.play(FadeOut(step5_title), Write(final_text)) # Remove o último título e mostra a conclusão
        self.wait(4)