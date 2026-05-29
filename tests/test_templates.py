import pytest
from src.notificacoes.templates import boas_vindas, recuperacao_senha, confirmacao_pedido

def test_boas_vindas_retorna_assunto_corpo():
    nome_usuario = "Elizabeth" # Define um nome de usuário para o teste
    templates = boas_vindas(nome=nome_usuario) # Chama a função boas_vindas com o nome de usuário e armazena o resultado em templates
    assert "assunto" in templates # Verifica se a chave "assunto" está presente no dicionário retornado por boas_vindas
    assert "corpo" in templates # Verifica se a chave "corpo" está presente no dicionário retornado por boas_vindas
    assert nome_usuario in templates["corpo"] # Verifica se o nome do usuário está presente no corpo da mensagem retornada por boas_vindas, garantindo que a personalização da mensagem esteja correta

def test_recuperacao_senha_contem_link():
    nome_usuario = "Maria" # Define um nome de usuário para o teste
    link_teste = "https://exemplo.com/recuperar-senha" # Define um link de teste para recuperação de senha
    templates = recuperacao_senha(nome=nome_usuario, link=link_teste) # Chama a função recuperacao_senha com o nome de usuário e o link de teste, e armazena o resultado em templates
    assert link_teste in templates["corpo"] # Verifica se o link de teste está presente no corpo da mensagem retornada por recuperacao_senha, garantindo que o link de recuperação de senha seja incluído corretamente na mensagem

def test_confirmacao_pedido_contem_valor():
    nome_usuario = "Gustavo" # Define um nome de usuário para o teste
    numero_pedido = "12345" # Define um número de pedido para o teste
    valor = 99.99 # Define um valor para o teste
    texto_valor_esperado = "R$99.99" # Define o texto do valor esperado formatado como moeda brasileira, para verificar se o valor é formatado corretamente na mensagem de confirmação de pedido
    templates = confirmacao_pedido(nome=nome_usuario, numero_pedido=numero_pedido, valor=valor) # Chama a função confirmacao_pedido com os parâmetros e armazena o resultado em templates
    assert numero_pedido in templates["corpo"] # Verifica se o número do pedido está presente no corpo da mensagem retornada por confirmacao_pedido
    assert texto_valor_esperado in templates["corpo"] # Verifica se o texto do valor esperado está presente no corpo da mensagem retornada por confirmacao_pedido