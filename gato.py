# Instalar (caso ainda não tenha): pip install kanren

from kanren import run, var, Relation, facts

# Criamos uma relação chamada "é_gato"
gato = Relation()
facts(gato, ("Hansel",), ("Joana",), ("TOM",))

# Criamos outra relação chamada "é_mamifero"
mamifero = Relation()
facts(mamifero, ("Hansel",),("TOM",))

# Agora, queremos descobrir quem é mamifero
x = var()
resultado = run(0, x, mamifero(x))
resultado2 = run(0, x, gato(x))
resultado3 = run(0, x, gato(x),mamifero(x))

print("Quem é mamifero:", resultado)
print("Quem é gato:", resultado2)
print("Quem é gato e mamifero:", resultado3)


'''
Comentário:

Cada fato é declarado com facts().

A consulta run() busca todos os valores de x que satisfazem a condição.

Assim, o sistema “raciocina” logicamente sobre os fatos declarados.

'''
