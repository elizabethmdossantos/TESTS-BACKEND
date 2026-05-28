import logging
import os

logger = logging.getLogger(__name__) # configurar o logger para o módulo de notificações

def enviar_sms(destinatario: str, mensagem: str) -> bool: # função para enviar sms, recebe destinatário e mensagem como parâmetros

    remetente = os.getenv('SMS_REMETENTE') # obter o remetente do SMS a partir de uma variável de ambiente

    if not remetente: # verificar se o remetente foi configurado
        raise EnvironmentError("A variável de ambiente 'SMS_REMETENTE' é obrigatória.") # lançar um erro se o remetente não estiver configurado
    
    print(f"[SMS] De: {remetente} | Para: {destinatario} | Mensagem: {mensagem}")

    logger.info(f"SMS enviado para {destinatario}")

    return True

def enviar_codigo_verificacao(telefone: str, codigo: str) -> bool: # função para enviar código de verificação por SMS, recebe telefone e código como parâmetros

    mensagem = f"Seu código de verificação é: {codigo}" # criar a mensagem de SMS com o código de verificação

    return enviar_sms(destinatario=telefone, mensagem=mensagem) # chamar a função enviar_sms para enviar a mensagem de SMS para o destinatário