# TRABALHO FINAL - LINGUAGENS FORMAIS E AUTÔMATOS
# ALUNOS: Lucca Franek Kroeff
#        Matheus Rodrigues Fonseca 
#        Sofia de Moraes Sauter Braga
# =====================================================================================================================

from itertools import combinations, product

# =====================================================================================================================

#============================= CLASSE AFD =============================================================================

# =====================================================================================================================
class AFD:

    def __init__(self, nome, estados, estado_inicial, simbolos, estado_final, transicoes):
        self.nome = nome
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.simbolos = simbolos
        self.estado_final = estado_final
        self.transicoes = transicoes

# =====================================================================================================================

#======================== FUNÇÃO PARA LER AFD =========================================================================

# =====================================================================================================================

def Le_AFD(Arquivo):

    Transicoes = {}    #vetor que conterá todas as transições presentes no autômato

    line = Arquivo.readline()[:-1]

                                    #Nome do AFD
    Automato_Nome = line

                                    #Conjunto de estados do AFD
    line = Arquivo.readline()[3:-1] #3 remove o 'S: ' no início e -1 remove o \n do fim
    line = line.replace(" ", '')
    Estados = line.split(',')

                                    #Conjunto de símbolos do AFD
    line = Arquivo.readline()[3:-1] #3 remove o 'A: ' no início e -1 remove o \n do fim
    line = line.replace(" ", '')
    Simbolos = line.split(',')

                                    #Estado inicial
    line = Arquivo.readline()[3:-1] #3 remove o 'i: ' no início e -1 remove o \n do fim
    line = line.replace(" ", '')
    Estado_Inicial = line
    
                                    #Conjunto de estados finais
    line = Arquivo.readline()[3:-1] #3 remove o 'F: ' no início e -1 remove o \n do fim
    line = line.replace(" ", '')
    Estado_Final = line.split(',')

    line = Arquivo.readline() #A primeira linha antes das transições é '\n'

    for i in Estados:
        Transicoes[i] = []      #Cada estado começa com transições vazias

                                    #Transições
    line = Arquivo.readline()[1:-1] #1 remove o '(' no início e -1 remove o '\n' do fim

    #As transições são um dicionário que relaciona um estado a uma lista de tuplas (a,qx) em que a é um símbolo e qx é um estado 
    while(line != ''):
        line = line.replace(" ", '')
        line = line.replace(')','')
        line = line.split(',')
        Transicoes[line[0]].append((line[1], line[2]))
        line = Arquivo.readline()[1:-1]

    return AFD(Automato_Nome, Estados, Estado_Inicial, Simbolos, Estado_Final, Transicoes)

# =====================================================================================================================

#================================ FUNÇÃO QUE DADO UM ARQUIVO DE PALAVRAS RETORNA UMA LISTA ============================

# =====================================================================================================================
def Le_Lista(AFD, Arquivo):
    Lista = []
    for line in Arquivo:
        line = line.split()
        if(line == []): 
             if AFD.estado_inicial in AFD.estado_final:      
                Lista.append("")     
        else:
            Lista.append(line[0])
    
    return Lista
# =====================================================================================================================

#================================ FUNÇÃO QUE DADA UMA PALVARA ACEITA OU REJEITA =======================================

# =====================================================================================================================
def Aceita_Ou_Rejeita_Palavra(AFD, Palavra, estado_inicial):
    
    if(Palavra == ''):    #inicialmente testamos se a linguagem é vazia
        for i in AFD.estado_final:
            if(i == estado_inicial):
                return "ACEITA"
        return "REJEITA"
            
    for letra in Palavra:   #aqui vemos se todas as letras presentes na palavra dada existem no alfabeto
        Palavra_Valida = 1    #primeiro supomos que todas as letras da palavra existem no alfabeto
        for i in AFD.simbolos:
            if(letra != i):
                Palavra_Valida = 0    #se pelo menos uma das letras da palavra nao existir no alfabeto, eh pq a palavra nao eh valida
            else:
                Palavra_Valida = 1
                break
        if(Palavra_Valida == 0):
            break

    if(Palavra_Valida == 0):
        return "REJEITA"
        
    EstadoAtual = estado_inicial
    for letra in Palavra:   #parte do código que fará as transições dentro do autômato dado os símbolos da palavra
        indef = 1
        for i in AFD.transicoes[EstadoAtual]:
            if i[0] == letra:
                EstadoAtual = i[1]
                indef = 0
                break
        if(indef == 1):
            return "REJEITA"
    if EstadoAtual in AFD.estado_final:
        return "ACEITA"
    return "REJEITA"
# =====================================================================================================================

#========================= FUNÇÃO QUE DADO UMA LISTA DE PALAVRAS ACEITA OU REJEITA ====================================

# =====================================================================================================================
def Aceita_Ou_Rejeita(AFD, ListaPalavras, estado_inicial):
    ListaAceitas = []
    for Palavra in ListaPalavras:
        Resultado = Aceita_Ou_Rejeita_Palavra(AFD, Palavra, estado_inicial)
        if(Resultado == "ACEITA"):
            ListaAceitas.append(Palavra)
    
    return ListaAceitas
# =====================================================================================================================

#========================= FUNÇÃO QUE DADO UM AFD VERIFICA SE A LINGUAGEM É VAZIA OU NÃO ==============================

# =====================================================================================================================
def Verifica_AFD_Vazio(AFD, estado_inicial):
    NumeroEstados = len(AFD.estados)
    Contador = 0

    while(Contador < NumeroEstados):
        Lista =  [''.join(i) for i in product(AFD.simbolos, repeat = Contador)]
        Contador += 1
    
        for i in Lista:
            Resultado = Aceita_Ou_Rejeita_Palavra(AFD, i, estado_inicial)
            if(Resultado == "ACEITA"):
                return "FALSE"
    return "TRUE"


#Função que recebe um estado e um AFD e remove o estado do AFD
#Remove da lista de estados, transições e estado final, se estiver
def RemoveEstado(AFD, estado):
    TransicoesRemover = []

    AFD.estados.remove(estado)
    del AFD.transicoes[estado]
    if estado in AFD.estado_final:
        AFD.estado_final.remove(estado)

    #Remover de uma lista durante um loop nela da problema
    #Então é guardadas as transições a serem removidas e depois são removidas
    for key, item in AFD.transicoes.items():
        for j in item:
            if j[1] == estado:
                TransicoesRemover.append((key, j))
    for key, j in TransicoesRemover:
        AFD.transicoes[key].remove(j)



# =====================================================================================================================

#========================= FUNÇÃO QUE DADO UM AFD DELETA ESTADOS INALCANÇÁVEIS DELE ===================================

# =====================================================================================================================

def DelInalc(AFD):
    visitados = {}

    #Ver se os estados forem alcançados a partir do inicial
    for i in AFD.estados:
        visitados[i] = 0
    
    #Insere o estado inicial na lista com os estados que vão ser visitados
    lista = [("", AFD.estado_inicial)]
    
    #Enquanto a lista não for vazia, visita cada estado e adiciona na lista
    #os estados que podem ser alcançados por ele
    while(len(lista) > 0):
        x = lista.pop(0)
        if visitados[x[1]] == 1:
            continue
        else:
            visitados[x[1]] = 1
            lista = lista + AFD.transicoes[x[1]]

    #Remove os estados que não foram alcançados
    estados = AFD.estados.copy()
    for i in estados:
        if visitados[i] == 0:
            RemoveEstado(AFD, i)


# =====================================================================================================================

#========================= FUNÇÃO QUE DADO UM AFD FAZ COM QUE ELE SEJA UMA FUNÇÃO TOTAL ===============================

# =====================================================================================================================


def FuncaoTotal(AFD):
    lista = []

    #Cria um estado de dump
    AFD.estados.append("dump")
    AFD.transicoes["dump"] = []
    for estado in AFD.estados:
        #Insere cada transição de um esado em uma lista
        for i in AFD.transicoes[estado]:
            lista.append(i[0])

        #Se a transição para alguma letra não está na lista, insere transição para dump
        for letra in AFD.simbolos:
            if letra not in lista:
                AFD.transicoes[estado].append((letra, 'dump'))
        lista.clear()


# =====================================================================================================================

#========================= FUNÇÕES AUXILIARES PARA A EQUIVALÊNCIA DE ESTADOS ==========================================

# =====================================================================================================================

#Função para marcar os estados da lista de dependencia
def MarcarLista(lista, estado):

    #Se o estado está marcado, não faz nada
    if lista[estado] == [('0','0')]:
        return

    #Para cada par de estados da lista de dependências, marca os pares das listas deles
    for i in lista[estado]:
        lista[estado].remove(i)
        MarcarLista(lista, i)
    lista[estado] = [('0','0')]


#Função que recebe uma lista de dependências, um par de estados a partir de transições de um par de estados chaves e os estados chaves
#A lista de dependências é um dicionário em que cada chave é um par de estados e os itens são lista de pares (q0,q1) -> [(qa,qb)...]
#E verifica se eles são equivalentes, se não forem, chama MarcarLista para marcar o par
def VerificaLista(lista, estadoTransicao, estadoChave):
    if not lista[estadoTransicao] or lista[estadoTransicao][0] != ('0','0'):

        #Se o par de estados não estiver marcado, insere na lista
        lista[estadoTransicao].append(estadoChave)

    else:
        #Se o par estiver marcado, marcar todos os pares da lista de dependencias de estados
        MarcarLista(lista, estadoChave)



#Essa função recebe um AFD e uma tupla de estados, e une esses estados em apenas um, adicionando todas as transições do
#segundo estado no primeiro e removendo o segundo estado
def UnirEstados(AFD, i):
    #Se o i[1] for o inicial, troca com o primeiro pois o segundo é deletado
    if i[1] == AFD.estado_inicial:
        i = (i[1], i[0])

    #Para cada transição no i[1], que não está no primeiro, adiciona ao primeiro
    #(Isso faz com que o autômato fique não-determinístico, mas como os esados são equivalentes
    # esse não determinismo deve sumir, com os próximos passos)
    for j in AFD.transicoes[i[1]]:
        if j not in AFD.transicoes[i[0]]:
            AFD.transicoes[i[0]].append(j)

    addTransicoes = [] #Lista para salvar as transições que precisarão ser adicionadas
                       # na parte abaixo, pois não se pode modificar AFD.transicoes enquanto itera sobre ele

    #Para cada transição que leva ao i[1], adiciona ela ao i[0]
    for keys, item in AFD.transicoes.items():
        if keys == i[0] or keys == i[1]:        #Não verifica as transições dos estados a serem unificados
            continue
        #Busca os estados em que levam uma transição para o i[1], se encontrar, adiciona essa transição ao i[0]
        for j in item:
            if j[1] == i[1]:
                addTransicoes.append((keys, j[0], i[0]))
    for j in addTransicoes:
         if (j[1], j[2]) not in AFD.transicoes[j[0]]:
            AFD.transicoes[j[0]].append((j[1], j[2]))

    #Remove o estado i[1]
    RemoveEstado(AFD, i[1])

#Essa função verifica todos os pares de estados não marcados em Equivalencia e une eles
def Unificacao(AFD, lista):
    for i in lista.keys():
        if lista[i] == [('0','0')]:
            continue
        if(i[0] in AFD.estados) and (i[1] in AFD.estados):
            UnirEstados(AFD, i)

# =====================================================================================================================

#============= FUNÇÃO QUE DADO UM AFD, VERIFICA CADA PAR DE ESTADOS EM BUSCA DE ESTADOS EQUIVALENTES E JUNTA ELES =====

# =====================================================================================================================

def Equivalencia(AFD):

    #listaDependencias é um dicionário de listas com as chaves sendo pares de estados sem repetição
    listaDependencias = {i:[] for i in combinations(AFD.estados, 2)}

    for i, j in listaDependencias.keys():     #Analisa cada par de estados
        #Se um dos estados for final e o outro não, marca ele com [('0','0')]
        #[('0','0')] aqui se refere a estados não equivalentes
        if (i in AFD.estado_final and j not in AFD.estado_final) or (i not in AFD.estado_final and j in AFD.estado_final):
            listaDependencias[(i,j)] = [('0','0')]

    #Para cada par (p,q)
    for estados in listaDependencias.keys():

        #Para cada símbolo, procura a transição de cada estado do par e bota o estado em 'i' e 'j'
        for simbolo in AFD.simbolos:

            #Se o par foi marcado, vai pro próximo
            if listaDependencias[estados] and listaDependencias[estados][0] == ('0','0'):
                break

            #Busca para qual estado a transição do primeiro estado com o simbolo leva e bota em i
            for transicoes in AFD.transicoes[estados[0]]:
                if transicoes[0] == simbolo:
                    i = transicoes[1]
                    break
                
            #Busca para qual estado a transição do segundo estado com o simbolo leva e bota em j
            for transicoes in AFD.transicoes[estados[1]]:
                if transicoes[0] == simbolo:
                    j = transicoes[1]
                    break
            #Se o par leva para o mesmo estado, pula
            if i == j:
                continue
            #Se o par (i,j) não está na lista, inverte porque (j,i) deve estar
            if (i,j) not in listaDependencias.keys():
                i,j = j,i

            #Verifica se (i,j) foram marcados, se sim marca todos em listaDependencia[estados]
            #Se não foram marcados, adiciona o par de estados na listaDependencia[(i,j)]
            VerificaLista(listaDependencias, (i,j), estados)
    #Une todos os pares de estados não marcados
    Unificacao(AFD, listaDependencias)


#Função que remove todos os estados que não tem caminho para um estado final
def ExclusaoInutil(AFD):
    for i in AFD.estados:
        if i in AFD.estado_final:
            continue
        #Para cada estado não final, verifica se existe palavras que podem ser formadas
        #a partir desse estado
        if Verifica_AFD_Vazio(AFD, i) == 'TRUE':
            RemoveEstado(AFD, i)

def Minimizacao(AFD):
    #Requisitos para algoritmo do autômato mínimo:
    #1 Ser um Autômato Finito determinístico (por definição é)

    #2 Função total
    FuncaoTotal(AFD)    #Adiciona transição onde não tem

    #3 Somente estados alcançáveis a partir do inicial
    DelInalc(AFD)       #Remove estados inalcançáveis

    #Etapas de minimização:
    #1 Teste de equivalência de estados
    #2 Unificação de estados equivalentes
    Equivalencia(AFD)   #Une estados equivalentes

    #3 Exclusão de estados inúteis
    ExclusaoInutil(AFD) #Exclui estados inúteis