import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart # criar mensagens de email com múltiplas partes
from email.mime.text import MIMEText # criar o corpo do email em formato de texto
import templates

logger = logging.getLogger(__name__) # configurar o logger para o módulo de notificações

def enviar_email(destinatario: str, assunto: str, corpo: str) -> bool: # função para enviar email, recebe destinatário, assunto e mensagem como parâmetros

    host = os.getenv("SMTP_HOST", "smtp.gmail.com") # "os" é um módulo que permite acessar variáveis de ambiente
    port = int(os.getenv("SMTP_PORT", "587")) # "SMTP_PORT" é o nome da variável de ambiente que contém a porta do servidor SMTP, e "587" é o valor padrão caso a variável não esteja definida

    usuario = os.getenv("SMTP_USER") # "SMTP_USER" é o nome da variável de ambiente que contém o nome de usuário para autenticação no servidor SMTP
    senha = os.getenv("SMTP_PASS") # "SMTP_PASS" é o nome da variável de ambiente que contém a senha para autenticação no servidor SMTP

    if not usuario or not senha: 
        raise EnvironmentError("SMTP_USER e SMTP_PASS são obrigatórios")
    
    msg = MIMEMultipart() # criar um objeto de mensagem multipart
    msg['subject'] = assunto # definir o assunto do email
    msg['From'] = usuario # definir o remetente do email
    msg['To'] = destinatario # definir o destinatário do email

    msg.attach(MIMEText(corpo, "plain")) # anexar o corpo do email como texto simples

    with smtplib.SMTP(host, port) as server: # criar uma conexão com o servidor SMTP usando o host e a porta definidos
        server.starttls() # iniciar a conexão TLS para segurança
        server.login(usuario, senha) # autenticar no servidor SMTP usando o nome de usuário e senha
        server.send_message(msg) # enviar a mensagem de email

    logger.info(f"Email enviado para {destinatario}")
    return True

def enviar_boas_vindas(email: str, nome: str) -> bool:
    dados_email = templates.boas_vindas(nome) # chamar a função de template para obter o assunto e corpo do email de boas-vindas
    return enviar_email(
        destinatario=email, 
        assunto=dados_email['assunto'], 
        corpo=dados_email['corpo']
        ) # chamar a função enviar_email para enviar o email de boas-vindas para o destinatário com o assunto e corpo obtidos do template
