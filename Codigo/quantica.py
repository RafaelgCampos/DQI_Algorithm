import cirq
import numpy as np

# --- 1. Definição do Problema (Agora você pode mudar aqui!) ---
B = np.array([[1, 1, 0], [0, 1, 1]])
v = np.array([1, 0])  # <--- Valor modificado
n = B.shape[1]  # Número de variáveis (colunas de B)
m = B.shape[0]  # Número de equações (linhas de B)
l = 1

# Soluções corretas para v=[0,0]: x=(0,0,0) e x=(1,1,1)
solucoes_corretas = [int('100', 2), int('011', 2)]

# --- Função Auxiliar ---
def ket_state_vector(index, num_qubits):
    state_vector = np.zeros(2**num_qubits, dtype=np.complex64)
    state_vector[index] = 1
    return state_vector

# --- 2. Oráculo Decodificador (Específico para a matriz B deste exemplo) ---
def syndrome_decoder_oracle(y_qubits, s_qubits):
    # ATENÇÃO: Esta lógica é 'hard-coded' para a matriz B específica.
    # Mudar B exigiria reescrever este decodificador.
    yield cirq.X(s_qubits[2])
    yield cirq.CCX(s_qubits[0], s_qubits[1], y_qubits[0])
    yield cirq.X(s_qubits[2])
    
    yield cirq.X(s_qubits[0])
    yield cirq.CCX(s_qubits[1], s_qubits[2], y_qubits[1])
    yield cirq.X(s_qubits[0])

# --- 3. Construção do Circuito DQI (Agora dinâmico!) ---
def build_dqi_circuit(v_vec, B_mat):
    y_qubits = cirq.LineQubit.range(m)
    s_qubits = cirq.LineQubit.range(m, m + n)
    circuit = cirq.Circuit()

    # --- PASSO 2: Aplicar Fase (Dinâmico) ---
    for i, v_i in enumerate(v_vec):
        if v_i == 1:
            circuit.append(cirq.Z(y_qubits[i]))
    circuit.append(cirq.Moment())

    # --- PASSO 3: Calcular Síndrome (Dinâmico) ---
    B_transpose = B_mat.T
    # Para cada linha s_j de Bᵀ...
    for j in range(n):
        # ...aplica CNOT de y_i para s_j se Bᵀ_ji for 1
        for i in range(m):
            if B_transpose[j, i] == 1:
                circuit.append(cirq.CNOT(y_qubits[i], s_qubits[j]))
    circuit.append(cirq.Moment())

    # --- PASSO 4: Decodificar (ainda hard-coded para este B) ---
    circuit.append(syndrome_decoder_oracle(y_qubits, s_qubits))
    circuit.append(cirq.Moment())

    # --- PASSO 5: Hadamard Final ---
    circuit.append(cirq.H.on_each(s_qubits))
    
    return circuit

# --- 4. Execução e Análise ---

# Constrói o circuito passando os parâmetros do problema
dqi_circuit = build_dqi_circuit(v, B)

# Preparação do Estado Inicial (igual a antes)
state_y_00 = ket_state_vector(0, m)
state_y_01 = ket_state_vector(1, m)
state_y_10 = ket_state_vector(2, m)
initial_y_state = (state_y_00 + state_y_01 + state_y_10) / np.sqrt(3)
initial_s_state = ket_state_vector(0, n)
initial_state_vector = np.kron(initial_y_state, initial_s_state)

# Simula o circuito
simulator = cirq.Simulator()
result = simulator.simulate(dqi_circuit, initial_state=initial_state_vector)
final_amplitudes = result.final_state_vector

print(f"--- Análise para o problema com v = {v.tolist()} ---")
probabilities = np.abs(final_amplitudes)**2
solution_probs = np.zeros(2**n)
for i, prob in enumerate(probabilities):
    solution_index = i % (2**n)
    solution_probs[solution_index] += prob
    
sorted_indices = np.argsort(solution_probs)[::-1]

for idx in sorted_indices:
    prob = solution_probs[idx]
    if prob < 0.001: continue
    
    solucao_bin = f'{idx:0{n}b}'
    is_correta = "✅ Solução Perfeita" if idx in solucoes_corretas else ""
    print(f"Solução x = {solucao_bin} : Probabilidade de {prob*100:.2f}% {is_correta}")