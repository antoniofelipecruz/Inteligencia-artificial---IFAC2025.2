import networkx as nx
import matplotlib.pyplot as plt

# 1. Classe principal da rede semântica
class RedeSemantica:
    
    # inicializa a rede semântica
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.regras = []

    # Adicionar e inicializa conceitos
    def inicializar_conceitos (self, nome):
        # Adicionar um novo conceito (nó) à rede
        if nome not in self.grafo:
            self.grafo.add_node(nome)

    # Adiciona relações
    def adicionar_relacao (self, origem, destino, relacao):
        # Garante que os nós existam antes de adicionar a aresta
        self.inicializar_conceitos(origem)
        self.inicializar_conceitos(destino)
        # Criar uma aresta com rótulo semântico
        self.grafo.add_edge(origem, destino, relation=relacao)

    # Lista relações
    def listar_relacoes (self):
        print("\n--- Relações na Rede Semântica ---")
        for u, v, d in self.grafo.edges(data=True):
            # O d['relation'] deve existir
            relacao = d.get('relation', 'REL_DESCONHECIDA')
            print(f"{u} -- {relacao} --> {v}")

    # Adiciona as regras
    def adicionar_regra (self, condicoes, conclusao):
        # Adicionar uma regra para uso na inferência
        self.regras.append((condicoes, conclusao))

    # Realiza inferência
    def inferir(self):
        novas_relacoes = []
        iniciou_inferencia = True
        while iniciou_inferencia:
            iniciou_inferencia = False
            for condicoes, conclusao in self.regras:
                # Verifica se todas as condições da regra são satisfeitas
                if all(self._existe_relacao(*c) for c in condicoes):
                    # Verifica se a conclusão ainda não existe na rede
                    if not self._existe_relacao(*conclusao):
                        print(f"INFERIDO: {conclusao[0]} -- {conclusao[2]} --> {conclusao[1]}")
                        self.adicionar_relacao(*conclusao)
                        novas_relacoes.append(conclusao)
                        iniciou_inferencia = True # Continua para inferir mais (encadeamento)
        return novas_relacoes # novas relações conclusivas

    # Verifica se uma relação já existe
    def _existe_relacao (self, origem, destino, relacao):
        if (origem, destino) in self.grafo.edges():
            return self.grafo[origem][destino].get('relation') == relacao
        return False

# 2. Base de regras lógicas (REGRAS REESTRUTURADAS PARA INFERÊNCIA MÁXIMA)
def carregar_regras():
    # REGRA 1 (Herança Subclasse -> É_UM)
    # Se Cachorro é 'subclasse' de Mamífero, então Cachorro 'é_um' Mamífero
    regra_heranca = (
        [("Cachorro", "Mamífero", "subclasse")],
        ("Cachorro", "Mamífero", "é_um") 
    )
    
    # REGRA 2 (Transitiva de É_UM)
    # Se Cachorro 'é_um' Mamífero, então Mamífero 'é_um' Animal (Axioma biológico)
    regra_mamifero_animal = (
        [("Cachorro", "Mamífero", "é_um")],
        ("Mamífero", "Animal", "é_um")
    )
    
    # REGRA 3 (Propriedade)
    # Se Mamífero 'é_um' Animal, então Mamífero 'tem_característica' Pelo
    regra_mamifero_pelo = (
        [("Mamífero", "Animal", "é_um")],
        ("Mamífero", "Pelo", "tem_característica")
    )

    # REGRA 4 (Possui + É_UM -> Gosta_de)
    # Se Pessoa 'possui' Cachorro E Cachorro 'é_um' Animal -> Pessoa 'gosta_de' Animal
    regra_gosta_de = (
        [("Pessoa", "Cachorro", "possui"), ("Cachorro", "Animal", "é_um")],
        ("Pessoa", "Animal", "gosta_de")
    )
    
    # REGRA 5 (Necessidade Universal 1)
    # Se Pessoa 'é_um' Ser_Vivo -> Pessoa 'precisa_de' Comida
    regra_precisa_de = (
        [("Pessoa", "Ser_Vivo", "é_um")], 
        ("Pessoa", "Comida", "precisa_de")
    )
    
    # REGRA 6 (Necessidade Universal 2 - Exemplo de Cachorro)
    # Se Cachorro 'é_um' Ser_Vivo -> Cachorro 'precisa_de' Comida
    regra_precisa_de_2 = (
        [("Cachorro", "Ser_Vivo", "é_um")], 
        ("Cachorro", "Comida", "precisa_de")
    )
    
    # REGRA 7 (Localização Específica)
    # Se Pessoa 'é_um' Ser_Vivo -> Pessoa 'mora_em' Casa
    regra_mora_em = (
        [("Pessoa", "Ser_Vivo", "é_um")],
        ("Pessoa", "Casa", "mora_em")
    )

    return [
        regra_heranca,
        regra_mamifero_animal,
        regra_mamifero_pelo,
        regra_gosta_de,
        regra_precisa_de,
        regra_precisa_de_2,
        regra_mora_em
    ]

# 3. Função de visualização gráfica
def exibir_grafo(grafo, titulo="Rede Semântica"):
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(grafo, k=0.3)
    nx.draw(grafo, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=11, font_weight="bold", arrowsize=20)
    edge_labels = nx.get_edge_attributes(grafo, 'relation')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels, label_pos=0.3, font_color='gray')
    plt.title(titulo)
    plt.show()

# 4. Execução principal - main() (BASE FATUAL MÍNIMA)
if __name__ == "__main__":
    # Inicializar a rede
    rede = RedeSemantica()

    # A. Adicionar conceitos
    rede.inicializar_conceitos("Pessoa")
    rede.inicializar_conceitos("Cachorro")
    rede.inicializar_conceitos("Animal")
    rede.inicializar_conceitos("Mamífero")
    rede.inicializar_conceitos("Pelo")
    rede.inicializar_conceitos("Casa")
    rede.inicializar_conceitos("Comida")
    rede.inicializar_conceitos("Ser_Vivo") # Conceito base

    # B. Adicionar relações factuais MÍNIMAS (Axiomas)
    rede.adicionar_relacao("Pessoa", "Cachorro", "possui")
    rede.adicionar_relacao("Cachorro", "Ser_Vivo", "é_um")
    rede.adicionar_relacao("Pessoa", "Ser_Vivo", "é_um")
    rede.adicionar_relacao("Cachorro", "Mamífero", "subclasse")

    print("--- Relações Fatuais Iniciais ---")
    rede.listar_relacoes()

    # C. Carregar e adicionar as regras
    regras = carregar_regras()
    for condicoes, conclusao in regras:
        rede.adicionar_regra(condicoes, conclusao)

    print("\n--- Iniciando Inferência ---")
    # D. Realizar inferência
    novas_relacoes = rede.inferir()

    if novas_relacoes:
        print(f"\nTotal de novas relações inferidas: {len(novas_relacoes)}")
    else:
        print("\nNenhuma nova relação foi inferida.")

    # E. Listar todas as relações (fatuais + inferidas)
    rede.listar_relacoes()

    # F. Exibir o grafo (Visualização)
    try:
        exibir_grafo(rede.grafo, "Rede Semântica Completa com Inferências")
    except Exception as e:
        print(f"\nErro ao exibir o grafo: {e}. Certifique-se de ter 'matplotlib' instalado.")
