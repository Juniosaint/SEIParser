from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Este algorítmo lê as páginas web resultantes de quaisquer pesquisa feita no SEI e cria planilha .csv estruturada
# com nome do parecer, link do parecer, unidade geradora, número do processo e data do parecer.

print("Este algorítmo lê as páginas web resultantes de quaisquer pesquisa feita no SEI e cria planilha .csv estruturada com nome do parecer, link do parecer, unidade geradora, número do processo e data do parecer.")

print("Verficar se o endereço do algorítmo está correto para a máquina em questão!")

uf=[] #unidade geradora
proc_num=[] #número do processo SEI
proc_link=[] #link do processo
proc_nome=[] #nome do processo
parecer_nome=[] #nome do parecer
parecer_link=[] #link do parecer
parecer_data=[] #data do parecer


query = "inicio"
while (query != "FIM" or query != "fim" or query != "Fim"): 
    query = input("Entre com o nome do arquivo ou digite 'fim': ")
    if (query == "FIM" or query == "fim" or query == "Fim"):
        break
    driver = webdriver.Firefox()
    link_texto = "CAMINHO ABSOLUTO PARA A PASTA ONDE AS PAGINAS FORAM SALVAS" + query + ".htm" #CORRIGIR PARA .HTML se for preciso
    driver.get(link_texto)
    content = driver.page_source

    soup = BeautifulSoup(content, features="html.parser")
    is_parecer = False
    is_processo = True
    i=1
    h=0
    for table in soup.findAll('table', attrs={'class':'resultado'}):
              
        for a in table.findAll('a', attrs={'class':'protocoloNormal'}):
            if (i%3==0):
                i=i+1
            elif (is_processo):
                #print("Número do processo: ")
                #print(a.string)
                proc_num.append(a.string)
                #print("Link do processo: ")
                #print(a.get('href'))
                proc_link.append(a.get('href'))
                i=i+1
                is_processo = False
                is_parecer = True        
            elif (is_parecer):
                #print("Parecer: ")
                #print(a.string)
                parecer_nome.append(a.string)
                #print("Link pro parecer: ")
                #print(a.get('href'))
                parecer_link.append(a.get('href'))
                i= i+1
                is_processo = True
                is_parecer = False
        if (i%3 != 0):
            for a in table.findAll('a', attrs={'class':'ancoraSigla'}):
                uf.append(a.get('title'))
            j=0
            for td in table.findAll('td'):
                j = j+1
                if (j%6==0):
                    texto = str(td)
                    texto = texto.split(" ")
                    texto = texto[1].split("<")
                    parecer_data.append(texto[0])
                    h = h+1
    print(proc_num)
    driver.quit()   

nome_planilha = input("Entre com o nome da planilha que conterá o resultado da busca: ")
    
df = pd.DataFrame({'Número do processo':proc_num,'Link do processo':proc_link, \
'Nome do parecer':parecer_nome, 'Link do parecer':parecer_link, 'Unidade Geradora':uf, 'Data do parecer':parecer_data})
df.to_csv(nome_planilha + '.csv', index=False, encoding='utf-8', mode='a')

print("Foi criado um arquivo com nome " + nome_planilha + ".csv no diretório deste algorítmo com o resultado da busca.")   