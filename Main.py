# TRABALHO FINAL - LINGUAGENS FORMAIS E AUTÔMATOS
# ALUNOS: Lucca Franek Kroeff
#        Matheus Rodrigues Fonseca 
#        Sofia de Moraes Sauter Braga
# =====================================================================================================================

import Functions


ArqAutomato = open(r"C:\Users\lucca\Desktop\Apresentação - Trabalho Final\AFD_formato_definido.txt")
ArqPalavras = open(r"C:\Users\lucca\Desktop\Apresentação - Trabalho Final\Palavras_.txt")
AFD = Functions.Le_AFD(ArqAutomato)
ListaPalavras = Functions.Le_Lista(AFD, ArqPalavras)

print('\n')
Resultado = Functions.Aceita_Ou_Rejeita(AFD, ListaPalavras, AFD.estado_inicial)
print("Lista de palavras aceitas pelo AFD dado:")
print(Resultado)
print('\n')

Vazio = Functions.Verifica_AFD_Vazio(AFD, AFD.estado_inicial)
print("O autômato é vazio?")
print(Vazio)
print('\n')

print("Transições ANTES da minimização: ")
print(AFD.nome)
print(AFD.estados)
print(AFD.simbolos)
print(AFD.estado_inicial)
print(AFD.estado_final)
print(AFD.transicoes)

print('\n')

Functions.Minimizacao(AFD)
print("Transições APÓS minimização: ")
print(AFD.nome)
print(AFD.estados)
print(AFD.simbolos)
print(AFD.estado_inicial)
print(AFD.estado_final)
print(AFD.transicoes)
