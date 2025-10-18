# --- Classes (Nós da Rede Semântica) ---

class Escola:
    """Representa a entidade Escola."""
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco

    def __str__(self):
        return f"Escola: {self.nome} ({self.endereco})"

class Livro:
    """Representa a entidade Livro."""
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor

    def __str__(self):
        return f"Livro: '{self.titulo}' (Autor: {self.autor})"

class Estudante:
    """Representa a entidade Estudante e suas relações."""
    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = matricula
        self.escola = None  # Relação 'estuda em'
        self.livros_lidos = [] # Relação 'lê'

    def estuda_em(self, escola: Escola):
        """Define a relação 'estuda em'."""
        self.escola = escola

    def le_livro(self, livro: Livro):
        """Adiciona um livro à lista de 'livros lidos', definindo a relação 'lê'."""
        if livro not in self.livros_lidos:
            self.livros_lidos.append(livro)
    
    def estudar(self):
        """Um método de exemplo para o Estudante."""
        if self.escola:
            print(f"{self.nome} está estudando na {self.escola.nome}.")
        else:
            print(f"{self.nome} precisa se matricular em uma escola!")
            
    def info_relacoes(self):
        """Exibe as relações do estudante para simular a navegação na rede semântica."""
        print(f"\n--- Relações de {self.nome} (Matrícula: {self.matricula}) ---")
        
        # Relação 1: estuda em
        if self.escola:
            print(f"-> estuda em: {self.escola}")
        
        # Relação 2: lê
        if self.livros_lidos:
            print(f"-> lê {len(self.livros_lidos)} livro(s):")
            for livro in self.livros_lidos:
                print(f"    - {livro.titulo}")
        else:
            print("-> não leu nenhum livro ainda.")


# --- Criação das Instâncias (Objetos Concretos) ---

# 1. Instâncias de Escola
escola_a = Escola("Colégio Padrão", "Rua das Flores, 100")

# 2. Instâncias de Livro
livro1 = Livro("Python para Iniciantes", "Guido van Rossum")
livro2 = Livro("Estruturas de Dados", "Donald Knuth")
livro3 = Livro("A Arte de Escrever", "Stephen King")

# 3. Instância de Estudante
estudante1 = Estudante("Alice Silva", "2024001")


# --- Estabelecimento das Relações (Criação da Rede Semântica) ---

# Estudante estuda em uma Escola
estudante1.estuda_em(escola_a)

# Estudante lê Livros
estudante1.le_livro(livro1)
estudante1.le_livro(livro2)


# --- Visualização da Rede Semântica (Navegação nas Relações) ---

estudante1.estudar()
estudante1.info_relacoes()

# Exemplo de outro objeto na rede
print(f"\nDetalhes do Objeto Escola: {escola_a}")
print(f"Detalhes do Objeto Livro: {livro3}")
