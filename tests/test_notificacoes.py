import pytest
from src.notificacoes.servico import enviar_boas_vindas, enviar_email

# Transformamos em fixture para garantir o ciclo de vida e isolamento correto do pytest
@pytest.fixture
def setup_env(monkeypatch):
    monkeypatch.setenv("SMTP_HOST", "smtp.test.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USER", "remetente@test.com")
    monkeypatch.setenv("SMTP_PASS", "senha_segura")


def test_enviar_email_sucesso(mocker, setup_env):  # Passamos a fixture como argumento
    # Criar um mock para a classe SMTP do módulo smtplib
    mock_smtp = mocker.patch("src.notificacoes.servico.smtplib.SMTP") 

    # Obter a instância do mock (context manager)
    mock_inst = mock_smtp.return_value.__enter__.return_value 

    resultado = enviar_email("dest@test.com", "assunto", "corpo")   

    assert resultado is True

    # ATENÇÃO: Se sua função interna não converter para int, mude 587 para "587"
    mock_smtp.assert_called_once_with("smtp.test.com", 587) 

    mock_inst.starttls.assert_called_once() 
    mock_inst.login.assert_called_once_with("remetente@test.com", "senha_segura") 
    mock_inst.send_message.assert_called_once() 


def test_sem_credenciais_levanta_erro(monkeypatch):
    # Garante que o ambiente estará limpo, independentemente da ordem dos testes
    monkeypatch.delenv("SMTP_USER", raising=False) 
    monkeypatch.delenv("SMTP_PASS", raising=False)

    with pytest.raises(EnvironmentError, match="obrigatórios"): 
        enviar_email("dest@test.com", "assunto", "corpo")


def test_enviar_boas_vindas(mocker, setup_env): # Passamos a fixture aqui também
    mock_enviar = mocker.patch(
        "src.notificacoes.servico.enviar_email",
        return_value=True,
    )

    resultado = enviar_boas_vindas("novo@test.com", "Elizabeth") 

    assert resultado is True

    mock_enviar.assert_called_once_with(
        destinatario="novo@test.com",
        assunto="Bem-vindo!",
        corpo="Olá Elizabeth, sua conta foi criada com sucesso!😃"
    )