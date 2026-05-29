import pytest
# Ajuste o import abaixo de acordo com a estrutura real do seu projeto
from notificacoes.gerenciador import GerenciadorDeNotificacoes

# 1. test_notificar_usuario_retorna_dict_com_campos_corretos
def test_notificar_usuario_retorna_dict_com_campos_corretos(mocker):
    # Usamos mocks para evitar chamadas reais de email e sms dentro do gerenciador
    mocker.patch("notificacoes.servico.enviar_email", return_value=True)
    mocker.patch("notificacoes.sms.enviar_codigo_verificacao", return_value=True)
    
    gerenciador = GerenciadorDeNotificacoes()
    
    registro = gerenciador.notificar_usuario(
        nome="Elizabeth", 
        email="elizabeth@exemplo.com", 
        telefone="+123456789"
    )
    
    # Verifica que o retorno é um dicionário e possui todas as chaves esperadas
    assert isinstance(registro, dict)
    assert "nome" in registro
    assert "email" in registro
    assert "telefone" in registro
    assert "email_enviado" in registro
    assert "sms_enviado" in registro


# 2. test_notificar_usuario_chama_email_e_sms
def test_notificar_usuario_chama_email_e_sms(mocker):
    # Criamos os mocks para "espionar" se as funções externas são chamadas
    mock_email = mocker.patch("notificacoes.servico.enviar_email", return_value=True)
    mock_sms = mocker.patch("notificacoes.sms.enviar_codigo_verificacao", return_value=True)
    
    gerenciador = GerenciadorDeNotificacoes()
    gerenciador.notificar_usuario(
        nome="Maria", 
        email="maria@exemplo.com", 
        telefone="+987654321"
    )
    
    # Verifica que ambas as funções de envio foram de fato invocadas
    mock_email.assert_called_once()
    mock_sms.assert_called_once()


# 3. test_historico_e_atualizado_apos_notificacao
def test_historico_e_atualizado_apos_notificacao(mocker):
    mocker.patch("notificacoes.servico.enviar_email", return_value=True)
    mocker.patch("notificacoes.sms.enviar_codigo_verificacao", return_value=True)
    
    gerenciador = GerenciadorDeNotificacoes()
    
    # Garante que o histórico começa vazio
    assert len(gerenciador.historico) == 0
    
    gerenciador.notificar_usuario(
        nome="Gustavo", 
        email="gustavo@exemplo.com", 
        telefone="+111222333"
    )
    
    # Verifica que após a notificação, o histórico passou a ter exatamente 1 entrada
    assert len(gerenciador.historico) == 1


# 4. test_resumo_conta_envios_corretamente
def test_resumo_conta_envios_corretamente(mocker):
    mocker.patch("notificacoes.servico.enviar_email", return_value=True)
    mocker.patch("notificacoes.sms.enviar_codigo_verificacao", return_value=True)
    
    gerenciador = GerenciadorDeNotificacoes()
    
    # Chama o método notificar_usuario 3 vezes seguidas
    gerenciador.notificar_usuario("User1", "user1@teste.com", "+111")
    gerenciador.notificar_usuario("User2", "user2@teste.com", "+222")
    gerenciador.notificar_usuario("User3", "user3@teste.com", "+333")
    
    dados_resumo = gerenciador.resumo()
    
    # Verifica que o campo ["total"] no retorno do resumo reflete os 3 envios
    assert dados_resumo["total"] == 3
