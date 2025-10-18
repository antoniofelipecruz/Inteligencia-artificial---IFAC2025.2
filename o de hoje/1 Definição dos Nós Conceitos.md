# --- 1. Definição dos Nós (Conceitos e Instâncias) ---

# Os nós da rede semântica e seus atributos (dados)
NOS_DADOS = {
    # Conceito: Estudante
    "alice": {"tipo": "Estudante", "matricula": "2024001", "nome": "Alice Silva"},
    
    # Conceito: Escola
    "colegio_padrao": {"tipo": "Escola", "endereco": "Rua das Flores, 100", "nome": "Colégio Padrão"},
    
    # Conceito: Livro
    "python_livro": {"tipo": "Livro", "titulo": "Python para Iniciantes", "autor": "Guido van Rossum"},
    "estrutura_livro": {"tipo": "Livro", "titulo": "Estruturas de Dados", "autor": "Donald Knuth"}
}

# --- 2. Definição das Arestas (Relações) ---

# As arestas definem as conexões entre os nós.
# Formato: (Nó_Origem, Relação, Nó_Destino)
ARESTAS = [
    ("alice", "ESTUDA_EM", "colegio_padrao"),
    ("alice", "LÊ", "python_livro"),
    ("alice", "LÊ", "estrutura_livro")
]

# --- 3. Função para Navegar na Rede Semântica ---

def navegar_rede_semantica(nome_no):
    """Exibe as informações do nó e suas conexões."""
    
    # 1. Obter e exibir os dados do Nó de Origem
    no_origem = NOS_DADOS.get(nome_no)
    if not no_origem:
        return f"Erro: Nó '{nome_no}' não encontrado."

    print(f"\n--- Nó: {nome_no.upper()} ({no_origem['tipo']}) ---")
    for chave, valor in no_origem.items():
        if chave != "tipo":
            print(f"  - {chave.capitalize()}: {valor}")
    
    print("\n--- Relações do Nó (Arestas) ---")

    # 2. Iterar sobre as arestas para encontrar relações
    encontradas = False
    for origem, relacao, destino in ARESTAS:
        if origem == nome_no:
            no_destino = NOS_DADOS.get(destino, {})
            tipo_destino = no_destino.get('tipo', 'Desconhecido')
            nome_destino = no_destino.get('nome') or no_destino.get('titulo') or destino
            
            print(f"-> {relacao}: {nome_destino} (Tipo: {tipo_destino})")
            encontradas = True
            
    if not encontradas:
        print("Nenhuma relação de saída encontrada.")

# --- Execução e Consulta da Rede ---

# Consultando o nó "alice" para ver suas relações
navegar_rede_semantica("alice")

# Consultando um nó que é destino de uma relação (para verificar seus dados)
navegar_rede_semantica("python_livro")
