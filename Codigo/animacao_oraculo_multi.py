# animacao_oraculo_multi.py
from manim import *
import numpy as np

class MultiQubitOracleViz(Scene):
    def construct(self):
        # --- 1. CONFIGURAÇÃO DA CENA ---
        N_QUBITS = 3
        N_STATES = 2**N_QUBITS
        SOLUTIONS = [0, 7]
        NON_SOLUTION_EXAMPLE = 5
        SOLUTION_EXAMPLE = 7
        

        explanation = MarkupText(
            "O Oráculo avalia <u>todos</u> os estados na superposição simultaneamente.",
            font_size=24
        ).to_edge(UP, buff=0.5)
        
        # --- Layout da Cena ---
        barchart_group = VGroup()
        barchart = BarChart(
            values=np.zeros(N_STATES),
            y_range=[-0.5, 0.5, 0.25],
            y_length=6,
            x_length=10,
            y_axis_config={"font_size": 20},
        ).scale(0.9).to_edge(LEFT, buff=0.5)
        
        bar_labels_text = VGroup(*[
            Text(f"{i:0{N_QUBITS}b}", font_size=18).next_to(barchart.bars[i], DOWN, buff=0.15)
            for i in range(N_STATES)
        ])
        barchart.add(bar_labels_text)

        self.play(Write(explanation))
        self.play(Create(barchart_group))
        self.wait(2)
        
        # --- PASSO 1: SUPERPOSIÇÃO ---
        self.play(explanation.animate.become(
            MarkupText("<b>Passo 1:</b> O sistema é colocado em uma superposição uniforme.", font_size=24).move_to(explanation)
        ))
        
        uniform_amplitudes = np.full(N_STATES, 1 / np.sqrt(N_STATES))
        self.play(barchart.animate.change_bar_values(uniform_amplitudes), run_time=1.5)
        self.wait(2)

        # --- PASSO 2: AÇÃO DO ORÁCULO ---
        self.play(explanation.animate.become(
            MarkupText("<b>Passo 2:</b> O Oráculo 'marca' as soluções com uma fase negativa (-1).", font_size=24).move_to(explanation)
        ))

        scanner = SurroundingRectangle(barchart.bars[NON_SOLUTION_EXAMPLE], color=YELLOW, buff=0.05)
        check_text = Text(f"Verificando |{NON_SOLUTION_EXAMPLE:03b}>", font_size=28).next_to(barchart_group, RIGHT, buff=0.5)
        result_text = Text("Não é solução. Nenhuma mudança.", font_size=28, color=GRAY).next_to(check_text, DOWN)
        
        self.play(Create(scanner), Write(check_text))
        self.wait(0.5)
        self.play(Write(result_text))
        self.wait(1.5)
        self.play(FadeOut(scanner), FadeOut(check_text), FadeOut(result_text))

        scanner.become(SurroundingRectangle(barchart.bars[SOLUTION_EXAMPLE], color=YELLOW, buff=0.05))
        check_text.become(Text(f"Verificando |{SOLUTION_EXAMPLE:03b}>", font_size=28).move_to(check_text))
        result_text.become(Text("É SOLUÇÃO! Aplicar fase (-1).", font_size=28, color=RED)).next_to(check_text, DOWN)

        self.play(Create(scanner), Write(check_text))
        self.wait(0.5)
        self.play(Write(result_text))
        
        marked_amplitudes = uniform_amplitudes.copy()
        marked_amplitudes[SOLUTION_EXAMPLE] *= -1
        marked_amplitudes[0] *= -1
        
        # CORREÇÃO AQUI: Animação de cor e valor separadas
        self.play(
            barchart.bars[SOLUTION_EXAMPLE].animate.set_color(RED),
            barchart.animate(lag_ratio=0).change_bar_values(marked_amplitudes),
            run_time=1.5
        )
        self.wait(2)
        self.play(FadeOut(scanner), FadeOut(check_text), FadeOut(result_text))

        self.play(explanation.animate.become(
            MarkupText("O processo é feito em paralelo para todos os estados.", font_size=24).move_to(explanation)
        ))
        
        final_oracle_amplitudes = uniform_amplitudes.copy()
        new_colors = [BLUE] * N_STATES
        for sol_idx in SOLUTIONS:
            final_oracle_amplitudes[sol_idx] *= -1
            new_colors[sol_idx] = RED
        
        # --- CORREÇÃO PRINCIPAL AQUI ---
        # Criamos uma lista de animações de cor
        color_animations = [
            barchart.bars[i].animate.set_color(new_colors[i])
            for i in range(N_STATES)
        ]

        final_oracle_amplitudes[0] *= -1
        
        # Executamos a mudança de valores e a lista de animações de cores juntas
        self.play(
            barchart.animate.change_bar_values(final_oracle_amplitudes),
            *color_animations,
            run_time=1.5
        )
        self.wait(3)

        self.play(explanation.animate.become(
            MarkupText("Resultado: Apenas as soluções foram 'etiquetadas' com a fase negativa.", font_size=24).move_to(explanation)
        ))
        self.wait(4)