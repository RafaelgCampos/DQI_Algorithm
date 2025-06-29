import cirq
import numpy as np
import math

# --- 1. DEFINIÇÃO DO PROBLEMA ---
B = np.array([[1, 1, 0, 1], [0, 1, 0, 1], [0, 1, 1, 1]])
v = np.array([1, 1, 0])
n_qubits = B.shape[1]
m_qubits = B.shape[0]

# --- FUNÇÕES DO CIRCUITO (Passos 1, 2 e 3) ---

def preparar_estado_inicial(qubits):
    return cirq.Circuit(cirq.H.on_each(qubits))

def create_phase_oracle(x_qubits, B_mat, v_vec):
    n_vars = len(x_qubits)
    m_eqs = len(v_vec)
    y_qubits = [cirq.NamedQubit(f'y_{i}') for i in range(m_eqs)]
    phase_qubit = cirq.NamedQubit('phase_ancilla')
    
    compute_Bx = [cirq.CNOT(x_qubits[j], y_qubits[i]) for i in range(m_eqs) for j in range(n_vars) if B_mat[i, j] == 1]
    flip_to_target = [cirq.X(q) for i, q in enumerate(y_qubits) if v_vec[i] == 0]
    apply_phase = [
        cirq.X(phase_qubit), cirq.H(phase_qubit),
        cirq.X(phase_qubit).controlled_by(*y_qubits),
        cirq.H(phase_qubit), cirq.X(phase_qubit)
    ]
    return cirq.Circuit(compute_Bx, flip_to_target, apply_phase, list(reversed(flip_to_target)), list(reversed(compute_Bx)))

def create_diffusion_operator(x_qubits):
    circuit = cirq.Circuit()
    circuit.append(cirq.H.on_each(x_qubits))
    circuit.append(cirq.X.on_each(x_qubits))
    if len(x_qubits) > 1:
      circuit.append(cirq.Z(x_qubits[-1]).controlled_by(*x_qubits[:-1]))
    elif len(x_qubits) == 1:
      circuit.append(cirq.Z(x_qubits[0]))
    circuit.append(cirq.X.on_each(x_qubits))
    circuit.append(cirq.H.on_each(x_qubits))
    return circuit

# --- Montagem do Circuito Principal Completo ---
qubits = cirq.LineQubit.range(n_qubits)
circuit = cirq.Circuit()
circuit.append(preparar_estado_inicial(qubits))

N = 2**n_qubits
def classical_checker(x_idx):
    x_vec = np.array([int(bit) for bit in f'{x_idx:0{n_qubits}b}'])
    return np.array_equal((B @ x_vec) % 2, v)
M = sum(1 for i in range(N) if classical_checker(i))

if M == 0:
    print("O problema não tem soluções.")
    k = 0
else:
    k = int((math.pi / 4) * math.sqrt(N / M))


print(f"--- Construindo o circuito final com {k} iteração(ões) de amplificação ---")

oracle = create_phase_oracle(qubits, B, v)
diffusion = create_diffusion_operator(qubits)
for i in range(k):
    print(f"Adicionando iteração de (Oráculo + Difusor) #{i+1}...")
    circuit.append(oracle)
    circuit.append(diffusion)

# --- VERIFICAÇÃO FINAL (LÓGICA DE ANÁLISE CORRIGIDA) ---
print("\n--- Análise do Vetor de Estado Após a Amplificação ---")

simulator = cirq.Simulator()
result = simulator.simulate(circuit)
full_state_vector = result.final_state_vector

# O simulador nos diz a ordem dos qubits que ele usou
qubit_order = result.qubit_map
# Os qubits da solução são os que não são ancilas
solution_qubits = [q for q in qubit_order if isinstance(q, cirq.LineQubit)]

print("As probabilidades estão concentradas nas soluções corretas")
print("-" * 60)

final_results = {}
for i, amplitude in enumerate(full_state_vector):
    # Considera apenas estados com probabilidade relevante
    probability = np.abs(amplitude)**2
    if probability > 0.001:
        # Para cada estado, verifica se os qubits de ancila estão em |0>
        # (A forma como o oráculo é construído pode deixar as ancilas em outros estados,
        # mas a amplitude para os estados de solução estará onde as ancilas são 0)
        
        # Converte o índice do estado em um dicionário de valores de qubit
        qubit_values = cirq.big_endian_int_to_bits(i, bit_count=len(qubit_order))
        qubit_value_map = dict(zip(qubit_order, qubit_values))
        
        # Verifica se todas as ancilas são 0
        ancillas_are_zero = True
        for q in qubit_order:
            if not isinstance(q, cirq.LineQubit): # Se não for um qubit de solução...
                if qubit_value_map[q] != 0:
                    ancillas_are_zero = False
                    break
        
        if ancillas_are_zero:
            # Reconstrói o valor da solução a partir dos qubits de solução
            solution_bits = [qubit_value_map[q] for q in solution_qubits]
            solution_idx = cirq.big_endian_bits_to_int(solution_bits)
            
            basis_state = f'|{solution_idx:0{n_qubits}b}⟩'
            # Acumula a probabilidade caso haja múltiplas entradas (não deve acontecer aqui)
            final_results[basis_state] = final_results.get(basis_state, 0) + probability

# Ordena e exibe os resultados
sorted_results = sorted(final_results.items(), key=lambda item: item[1], reverse=True)

for basis_state, probability in sorted_results:
    idx = int(basis_state.strip('|⟩'), 2)
    is_solution = classical_checker(idx)
    marker = "✅ SOLUÇÃO CORRETA" if is_solution else "❌"
    print(f"Estado: {basis_state} | Probabilidade: {probability*100:5.2f}% {marker}")

print("-" * 60)