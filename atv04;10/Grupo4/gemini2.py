import random
from statistics import mean
import time

# =============================================================
# PARÂMETROS DA DIMENSÃO INSTÁVEL (Caverna do Eco Mortal)
# =============================================================
HP_INICIAL = 30
CICLOS_MAXIMOS = 3
NUMERO_DE_SIMULACOES = 90000

# Definição das Ações e seus Efeitos Quânticos
ACOES = {
    "Fuga_Desesperada": {
        "mod_eco": +2,
        "mod_sombra": -2,
        "limiar_resiliencia": 12,
        "desc": "Uma corrida caótica. Aumenta massivamente o Eco, mas pode levar a uma saída rápida."
    },
    "Sombra_Silenciosa": {
        "mod_eco": -1,
        "mod_sombra": +2,
        "limiar_resiliencia": 8,
        "desc": "Movimentos furtivos. Reduz o Eco e confunde as Sombras."
    },
    "Confronto_Direto": {
        "mod_eco": +1,
        "mod_sombra": -1,
        "limiar_resiliencia": 10,
        "desc": "Enfrentar o horror. Aumenta o Eco, mas mantém o controle da situação."
    }
}

# ===========================
# DANO DAS SOMBRAS ADAPTATIVAS
# ===========================
def calcular_dano_sombra(rolagem, postura, mod_sombra):
    r = rolagem - mod_sombra
    if postura == "agressiva":
        if r >= 19: return "colapso_instantaneo"
        elif r >= 13: return 8
        elif r >= 7: return 4
        else: return 0
    elif postura == "cautelosa":
        if r >= 20: return "colapso_instantaneo"
        elif r >= 15: return 5
        elif r >= 9: return 2
        else: return 0

# ==================================
# SIMULA UMA ÚNICA LINHA TEMPORAL (PARA ANÁLISE)
# ==================================
def simular_uma_realidade(acao_inicial):
    hp = HP_INICIAL
    eco_mortal = 0
    fragmentos_coragem = 0
    acao_atual = acao_inicial

    for ciclo in range(1, CICLOS_MAXIMOS + 1):
        acao_info = ACOES[acao_atual]
        eco_mortal = max(0, eco_mortal + acao_info["mod_eco"])
        
        teste_resiliencia = random.randint(1, 20)
        
        if fragmentos_coragem > 0 and eco_mortal > 2:
            teste_resiliencia += 5
            fragmentos_coragem -= 1

        if teste_resiliencia >= 20: break
        if teste_resiliencia == 19: fragmentos_coragem += 1
        if teste_resiliencia <= 3: return -1000, "morreu", 0

        limiar_real = acao_info["limiar_resiliencia"] - eco_mortal
        if teste_resiliencia < limiar_real:
            hp -= 10
            if hp <= 0: return -1000, "morreu", 0

        # --- LÓGICA DA SOMBRA CORRIGIDA ---
        utilidade_estimada = {}
        for postura in ("agressiva", "cautelosa"):
            perda_de_utilidade_total = 0
            for _ in range(50):
                dano = calcular_dano_sombra(random.randint(1, 20), postura, acao_info["mod_sombra"])
                if dano == "colapso_instantaneo" or (isinstance(dano, int) and hp - dano <= 0):
                    perda_de_utilidade_total += hp
                elif isinstance(dano, int):
                    perda_de_utilidade_total += dano
            utilidade_estimada[postura] = perda_de_utilidade_total / 50
        
        postura_escolhida = max(utilidade_estimada, key=utilidade_estimada.get)

        dano_sombra = calcular_dano_sombra(random.randint(1, 20), postura_escolhida, acao_info["mod_sombra"])
        if dano_sombra == "colapso_instantaneo": return -1000, "morreu", 0
        
        if isinstance(dano_sombra, int): hp -= dano_sombra
        if hp <= 0: return -1000, "morreu", 0

        if hp <= 10 or eco_mortal >= 4: acao_atual = "Sombra_Silenciosa"
        elif hp >= 25: acao_atual = "Fuga_Desesperada"
        else: acao_atual = "Confronto_Direto"

    if hp > 0:
        utilidade = 1000 + hp + (fragmentos_coragem * 100)
        return utilidade, "sobreviveu", hp
    else: # Caso saia do loop por HP <= 0
        return -1000, "morreu", 0

# ===============================================
# MODO DE JOGO INTERATIVO
# ===============================================
def jogar_partida_interativa():
    hp = HP_INICIAL
    eco_mortal = 0
    fragmentos_coragem = 0
    
    print("\n" + "="*50)
    print(" Você entra na Caverna do Eco Mortal... ")
    print("="*50 + "\n")

    for ciclo in range(1, CICLOS_MAXIMOS + 1):
        print(f"--- CICLO ATUAL: {ciclo}/{CICLOS_MAXIMOS} ---")
        print(f"❤️ HP: {hp} | 🔊 Eco Mortal: {eco_mortal} | ✨ Fragmentos de Coragem: {fragmentos_coragem}")
        
        acao_escolhida = ""
        while acao_escolhida not in ACOES:
            print("\nEscolha sua próxima ação:")
            for i, (nome, info) in enumerate(ACOES.items()):
                print(f"  {i+1}. {nome}: {info['desc']}")
            try:
                escolha = int(input("Digite o número da sua escolha: ")) - 1
                acao_escolhida = list(ACOES.keys())[escolha]
            except (ValueError, IndexError):
                print("Escolha inválida. Tente novamente.")

        acao_info = ACOES[acao_escolhida]
        eco_mortal = max(0, eco_mortal + acao_info["mod_eco"])

        teste_resiliencia = random.randint(1, 20)
        print(f"\nVocê escolheu '{acao_escolhida}'. O Eco agora é {eco_mortal}.")
        
        if fragmentos_coragem > 0:
            if input(f"Você tem {fragmentos_coragem} Fragmento(s). Deseja usar um para +5 no teste? (s/n): ").lower() == 's':
                teste_resiliencia += 5
                fragmentos_coragem -= 1
                print(f"✨ Fragmento consumido! Seu teste agora tem um bônus.")

        print(f"🎲 Você rola o Teste de Resiliência e tira... {teste_resiliencia}!")

        if teste_resiliencia >= 20:
            print("\n🌀 SUCESSO CRÍTICO! Uma fenda na realidade se abre e você escapa!")
            print("="*20 + " VITÓRIA! " + "="*20)
            return
        if teste_resiliencia == 19:
            fragmentos_coragem += 1
            print("🌟 Sorte Pura! Você encontrou um Fragmento de Coragem!")
        if teste_resiliencia <= 3:
            print("\n💀 FALHA CRÍTICA! A realidade colapsa ao seu redor. Você foi apagado.")
            print("="*20 + " DERROTA! " + "="*20)
            return

        limiar_real = acao_info["limiar_resiliencia"] - eco_mortal
        if teste_resiliencia < limiar_real:
            dano_ambiente = 10
            hp -= dano_ambiente
            print(f"📉 Falha parcial (rolou {teste_resiliencia} vs um limiar de {limiar_real}). O eco causa {dano_ambiente} de dano psíquico!")
            if hp <= 0:
                print("\n🧠 Sua mente se desfaz. Fim da linha.")
                print("="*20 + " DERROTA! " + "="*20)
                return
        
        print("\n👻 Uma Sombra Adaptativa se materializa...")
        
        # LÓGICA DA SOMBRA CORRIGIDA TAMBÉM NO MODO INTERATIVO
        utilidade_estimada = {}
        for postura in ("agressiva", "cautelosa"):
            perda_de_utilidade_total = 0
            for _ in range(50):
                dano = calcular_dano_sombra(random.randint(1, 20), postura, acao_info["mod_sombra"])
                if dano == "colapso_instantaneo" or (isinstance(dano, int) and hp - dano <= 0):
                    perda_de_utilidade_total += hp
                elif isinstance(dano, int):
                    perda_de_utilidade_total += dano
            utilidade_estimada[postura] = perda_de_utilidade_total / 50
        
        postura_escolhida = max(utilidade_estimada, key=utilidade_estimada.get)

        print(f"A Sombra analisa sua fraqueza e adota uma postura '{postura_escolhida}'!")

        rolagem_sombra = random.randint(1, 20)
        dano_sombra = calcular_dano_sombra(rolagem_sombra, postura_escolhida, acao_info["mod_sombra"])
        print(f"🎲 A Sombra ataca e rola... {rolagem_sombra}!")
        
        if dano_sombra == "colapso_instantaneo":
            print("💥 A Sombra encontra uma brecha fatal. Você foi apagado da existência.")
            print("="*20 + " DERROTA! " + "="*20)
            return
        
        if isinstance(dano_sombra, int) and dano_sombra > 0:
            hp -= dano_sombra
            print(f"⚔️ Você sofre {dano_sombra} de dano!")
        else:
            print("🛡️ Você consegue evitar o ataque da Sombra!")

        if hp <= 0:
            print("\n💔 Você sucumbiu às Sombras.")
            print("="*20 + " DERROTA! " + "="*20)
            return
            
        print("-" * 50)
    
    print("\nOs 3 ciclos terminaram. Você sobreviveu à provação, emergindo da escuridão.")
    print("="*20 + " VITÓRIA! " + "="*20)


# ===============================================
# EXECUÇÃO PRINCIPAL (SIMULAÇÃO E JOGO)
# ===============================================
def main():
    print("INICIANDO SIMULAÇÃO DE MONTE CARLO NA CAVERNA DO ECO MORTAL...")
    print(f"Analisando {NUMERO_DE_SIMULACOES} futuros possíveis...")

    resultados_finais = {}
    start_time = time.time()

    for acao in ACOES:
        res_util = []
        status_contagem = {"sobreviveu": 0, "morreu": 0}
        
        sims_por_acao = NUMERO_DE_SIMULACOES // len(ACOES)
        for i in range(sims_por_acao):
            util, status, hp_final = simular_uma_realidade(acao)
            res_util.append(util)
            status_contagem[status] += 1
            print(f"\rAnalisando Ação '{acao}': {i+1}/{sims_por_acao} futuros calculados...", end="")
        
        resultados_finais[acao] = {
            "avg_util": mean(res_util),
            "status": status_contagem,
        }
        print()

    duration = time.time() - start_time
    print(f"\nSimulação concluída em {duration:.2f} segundos.")

    print("\n===== RELATÓRIO DAS REALIDADES POSSÍVEIS =====\n")
    for acao, data in resultados_finais.items():
        taxa_sobrevivencia = (data['status']['sobreviveu'] / sum(data['status'].values())) * 100
        print(f"Ação Inicial: {acao}")
        print(f"  - Utilidade Média: {data['avg_util']:.2f} | Taxa de Sobrevivência: {taxa_sobrevivencia:.2f}%")
    
    melhor_acao = max(resultados_finais.items(), key=lambda x: x[1]["avg_util"])
    print(f"\n>>> A ESTRATÉGIA INICIAL ÓTIMA É: {melhor_acao[0]} <<<")

    if input("\nDeseja entrar na Caverna do Eco Mortal e jogar uma partida? (s/n): ").lower() == 's':
        jogar_partida_interativa()
    else:
        print("\nVocê recua das sombras... por enquanto.")

if __name__ == "__main__":
    main()