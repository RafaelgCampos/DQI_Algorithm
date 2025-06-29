# animacao_final_transform.py
from manim import *
import numpy as np
import math

class GroverFullAlgorithmViz(Scene):
    def construct(self):
        # --- 1. CONFIGURAÇÃO DA CENA ---
        N_QUBITS = 3
        N_STATES = 2**N_QUBITS
        SOLUTIONS = [0, 7]
        
        title = MarkupText("Visualização do Algoritmo de Grover", font_size=36).to_edge(UP)
        explanation = MarkupText(
            "Vamos visualizar os 3 passos do algoritmo para encontrar <i>x</i> em <i>Bx=0</i>.",
            font_size=24
        ).next_to(title, DOWN, buff=0.2)
        
        self.play(Write(explanation))
        self.wait(1)
        
        # --- FUNÇÃO AUXILIAR PARA CRIAR GRÁFICOS ---
        # Isso evita repetição de código
        def create_chart(values):
            chart = BarChart(
                values=values,
                y_range=[-1.0, 1.0, 0.25],
                y_length=6,
                x_length=10,
                y_axis_config={"font_size": 20},
            ).scale(0.85).to_edge(LEFT, buff=0.5)
            
            labels = VGroup(*[
                Text(f"{i:0{N_QUBITS}b}", font_size=18).next_to(chart.bars[i], DOWN, buff=0.15)
                for i in range(N_STATES)
            ])
            chart.add(labels)
            return chart

        # --- PASSO 1: SUPERPOSIÇÃO ---
        self.play(explanation.animate.become(
            MarkupText("<b>Passo 1:</b> Superposição Uniforme", font_size=24).move_to(explanation)
        ))
        
        uniform_amplitudes = np.full(N_STATES, 1 / np.sqrt(N_STATES))
        barchart = create_chart(uniform_amplitudes) # Cria o primeiro gráfico visível
        self.play(Create(barchart), run_time=1.5)
        self.wait(2)

        # --- PASSO 2: AÇÃO DO ORÁCULO ---
        self.play(explanation.animate.become(
            MarkupText("<b>Passo 2:</b> Oráculo de Fase inverte a fase das soluções", font_size=24).move_to(explanation)
        ))
        
        oracle_amplitudes = uniform_amplitudes.copy()
        for sol_idx in SOLUTIONS:
            oracle_amplitudes[sol_idx] *= -1
            
        # Cria o gráfico alvo da transformação (invisível por enquanto)
        oracle_barchart_target = create_chart(oracle_amplitudes)
        for sol_idx in SOLUTIONS:
            oracle_barchart_target.bars[sol_idx].set_color(RED)

        # Anima a transformação do gráfico original para o gráfico alvo
        self.play(Transform(barchart, oracle_barchart_target), run_time=2)
        self.wait(2)

        # --- PASSO 3: DIFUSÃO (AMPLIFICAÇÃO) ---
        self.play(explanation.animate.become(
            MarkupText("<b>Passo 3:</b> Difusão amplifica as soluções marcadas", font_size=24).move_to(explanation)
        ))
        
        mean_val = np.mean(oracle_amplitudes)
        mean_line = DashedLine(
            start=barchart.coords_to_point(barchart.x_axis.x_min, mean_val),
            end=barchart.coords_to_point(barchart.x_axis.x_max, mean_val),
            color=YELLOW
        )
        mean_label = Tex("Média", font_size=24, color=YELLOW).next_to(mean_line, LEFT, buff=0.1)
        
        self.play(Create(mean_line), Write(mean_label))
        self.wait(1.5)

        amplified_amplitudes = (mean_val + (mean_val - oracle_amplitudes)) / 2
        
        # Cria o gráfico final da transformação
        amplified_barchart_target = create_chart(amplified_amplitudes)
        for i in range(N_STATES):
            if i in SOLUTIONS:
                amplified_barchart_target.bars[i].set_color(GREEN)
            else:
                amplified_barchart_target.bars[i].set_color(BLUE)

        # Anima a transformação do gráfico do oráculo para o gráfico final
        self.play(
            Transform(barchart, amplified_barchart_target),
            FadeOut(mean_line), 
            FadeOut(mean_label),
            run_time=2.5
        )
        
        self.play(explanation.animate.become(
            MarkupText("<b>Resultado Final:</b> A probabilidade está concentrada nas soluções!", font_size=24).move_to(explanation)
        ))
        
        self.wait(5)