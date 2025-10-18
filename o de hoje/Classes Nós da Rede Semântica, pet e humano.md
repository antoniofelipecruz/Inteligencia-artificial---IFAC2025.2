# --- Classes (Nós da Rede Semântica) ---

class Animal:
    """Superclasse abstrata que representa um animal e a relação 'precisa de comida'."""
    def __init__(self, especie):
        self.especie = especie
        
    def precisa_de_comida(self, comida):
        print(f"[{self.especie}] precisa de {comida.nome}.")

class Comida:
    """Nó Comida."""
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo
        
    def __str__(self):
        return f"{self.nome} ({self.tipo})"

class Cachorro(Animal):
    """Nó Cachorro. Herda a relação 'é um' de Animal."""
    def __init__(self, nome, raca):
        super().__init__("Cachorro")
        self.nome = nome
        self.raca = raca
        self.alimentado = False # Estado para a inferência
        
    def latir(self):
        print(f"{self.nome} da raça {self.raca} está latindo!")

class Cidade:
    """Nó Cidade."""
    def __init__(self, nome):
        self.nome = nome

class Casa:
    """Nó Casa. Tem a relação 'localizada em'."""
    def __init__(self, endereco, cidade: Cidade):
        self.endereco = endereco
        self.cidade = cidade  # Relação 'localizada em'

class Pessoa:
    """Nó Pessoa. Tem as relações 'possui' e 'mora em'."""
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
        self.casa = None         # Relação 'mora em'
        self.cachorros = []      # Relação 'possui'

    def morar_em(self, casa: Casa):
        """Define a relação 'mora em'."""
        self.casa = casa

    def possuir_cachorro(self, cachorro: Cachorro):
        """Define a relação 'pertence a' (ou 'possui')."""
        self.cachorros.append(cachorro)
        print(f"{self.nome} agora possui {cachorro.nome}.")

    # --- INFERÊNCIA LÓGICA ---
    def alimentar_cachorro(self, cachorro: Cachorro, comida: Comida):
        """
        Inferência: Se Humano possui Cachorro, e Cachorro é um Animal, 
        então o Humano é responsável por alimentar o Cachorro.
        """
        if cachorro in self.cachorros:
            # Ação resultante da inferência
            print(f"\n[INFERÊNCIA ATIVADA]")
            print(f"Como {self.nome} possui {cachorro.nome}, a responsabilidade de alimentação é dele(a).")
            
            cachorro.precisa_de_comida(comida) # Animal precisa de Comida
            print(f"-> {self.nome} alimenta {cachorro.nome} com {comida}.")
            cachorro.alimentado = True
        else:
            print(f"{self.nome} não possui {cachorro.nome} e não pode alimentá-lo.")


# --- Criação da Rede Semântica (Instâncias e Relações) ---

# Nós Base
comida_cao = Comida("Ração Premium", "Seca")
cidade_rb = Cidade("Rio Branco")

# Construindo a hierarquia
casa_principal = Casa("Av. Brasil, 456", cidade_rb)
cachorro_bruce = Cachorro("Bruce", "Labrador")

# Nó Pessoa e suas Relações
humano_joao = Pessoa("João", 30)
humano_joao.morar_em(casa_principal)
humano_joao.possuir_cachorro(cachorro_bruce)


# --- Testando as Relações e a Inferência ---

# 1. Relação Base: Cachorro é um Animal (Herança)
cachorro_bruce.latir()
cachorro_bruce.precisa_de_comida(comida_cao) # Animal precisa de Comida

# 2. Relação Inferida (Humano possui Cachorro -> Humano alimenta)
humano_joao.alimentar_cachorro(cachorro_bruce, comida_cao)

# 3. Navegando a Rede (para verificar a relação 'mora em' e 'localizada em')
print(f"\n[Navegação da Rede]")
print(f"{humano_joao.nome} mora em {humano_joao.casa.endereco}.")
print(f"A casa está localizada em {humano_joao.casa.cidade.nome}.")
