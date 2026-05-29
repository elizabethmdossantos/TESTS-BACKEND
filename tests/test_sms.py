import pytest
from src.notificacoes.sms import enviar_sms, enviar_codigo_verificacao

def test_enviar_sms_sucesso(monkeypatch):
    # o monkeypatch serve para simular a variável de ambiente SMS_REMETENTE durante o teste
    # setenv é usado para definir a variável de ambiente SMS_REMETENTE com um número de telefone fictício para o remetente do SMS
    monkeypatch.setenv("SMS_REMETENTE", "+1234567890") 
    destinatario = "+0987654321"
    mensagem = "Bem-vindo ao nosso serviço!"
    # Chamar a função enviar_sms com os parâmetros de destinatário e mensagem, e armazenar o resultado para verificação
    resultado = enviar_sms(destinatario=destinatario, mensagem=mensagem)

    # Verificar se o resultado da função é True, indicando que o SMS foi enviado com sucesso
    assert resultado is True

def test_sem_remetente_levanta_erro(monkeypatch):
    # monkeypatch é usado para manipular o ambiente de teste, permitindo simular a ausência da variável de ambiente SMS_REMETENTE
    # delenv é usado para garantir que a variável de ambiente SMS_REMETENTE não esteja definida durante este teste
    # raising=False evita que um erro seja levantado se a variável já estiver ausente
    monkeypatch.delenv("SMS_REMETENTE", raising=False)
    destinatario = "+0987654321"
    mensagem = "Bem-vindo ao nosso serviço!"
    # Verificar se a função enviar_sms lança um EnvironmentError quando a variável de ambiente SMS_REMETENTE não está configurada
    # O pytest valida se o erro 'EnvironmentError' foi lançado corretamente
    with pytest.raises(EnvironmentError) as exc_info:
        enviar_sms(destinatario=destinatario, mensagem=mensagem)
    
    # Verificar se a mensagem de erro é a esperada, confirmando que o erro foi causado pela ausência da variável de ambiente SMS_REMETENTE
    # exc_info.value contém a mensagem de erro capturada, e a asserção verifica se ela corresponde à mensagem esperada sobre a variável de ambiente obrigatória.
    assert str(exc_info.value) == "A variável de ambiente 'SMS_REMETENTE' é obrigatória."

def test_enviar_codigo_verificacao(mocker):
    # O mocker é usado para criar um mock da função enviar_sms, 
    # permitindo verificar se ela foi chamada com os parâmetros corretos sem realmente enviar um SMS durante o teste
    mock_enviar_sms = mocker.patch('src.notificacoes.sms.enviar_sms')
    telefone = "+0987654321"
    codigo = "123456"
    mensagem_esperada = "Seu código de verificação é: 123456"
    # Chamar a função enviar_codigo_verificacao com os parâmetros de telefone e código, 
    # que deve internamente chamar a função enviar_sms com a mensagem formatada corretamente
    enviar_codigo_verificacao(telefone=telefone, codigo=codigo)
    # Verificar se a função enviar_sms foi chamada exatamente uma vez com os parâmetros corretos de destinatário e mensagem formatada
    mock_enviar_sms.assert_called_once_with(destinatario=telefone, mensagem=mensagem_esperada)

