import random
from notificacoes import templates
from notificacoes import servico
from notificacoes import sms

class GerenciadorDeNotificacoes:

    def __init__(self):
        self.historico: list[dict] = [] # inicializar o histórico de notificações como uma lista vazia

    def notificar_usuario(self, nome: str, email: str, telefone: str) -> dict:
        # Gerar o conteúdo do email usando o template de boas-vindas
        dados_boas_vindas = templates.boas_vindas(nome)
        # Enviar o email e o SMS, armazenando os resultados
        # O resultado do envio de email e SMS é armazenado em variáveis para serem usadas posteriormente
        email_sucesso = servico.enviar_email(
            destinatario=email,
            assunto=dados_boas_vindas['assunto'],
            corpo=dados_boas_vindas['corpo'])
        # Gerar um código de verificação aleatório para o SMS
        codigo_sms = random.randint(100000, 999999)
        # Enviar o SMS usando o serviço de SMS e armazenar o resultado
        sms_sucesso = sms.enviar_codigo_verificacao(telefone=telefone, codigo=str(codigo_sms))
        # Criar um registro da notificação com os detalhes e os resultados dos envios
        registro = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "email_enviado": email_sucesso,
            "sms_enviado": sms_sucesso
        }
        # Adicionar o registro ao histórico de notificações
        self.historico.append(registro)
        # Retornar o registro da notificação para que possa ser verificado nos testes
        return registro

    def reenviar_falhas(self) -> int:
        # Iterar sobre o histórico de notificações e tentar reenviar as notificações que falharam
        reenvios_realizados = 0 
        # A variável reenvios_realizados é usada para contar quantas notificações foram reenviadas com sucesso
        for notificacao in self.historico:
            houve_falha = False

            if not notificacao["email_enviado"]:
                # Gerar o conteúdo do email usando o template de boas-vindas novamente, caso o envio anterior tenha falhado
                dados_boas_vindas = templates.boas_vindas(notificacao["nome"])
                # Tentar reenviar o email e atualizar o status de envio no registro da notificação
                notificacao["email_enviado"] = servico.enviar_email(
                    destinatario=notificacao["email"],
                    assunto=dados_boas_vindas['assunto'],
                    corpo=dados_boas_vindas['corpo']
                )
                houve_falha = True

            if not notificacao["sms_enviado"]:
                # Gerar um código de verificação aleatório para o SMS
                codigo_sms = random.randint(100000, 999999)
                # Tentar reenviar o SMS e atualizar o status de envio no registro da notificação
                notificacao["sms_enviado"] = sms.enviar_codigo_verificacao(
                    telefone=notificacao["telefone"], 
                    codigo=str(codigo_sms)
                )
                houve_falha = True

            if houve_falha:
                reenvios_realizados += 1

        return reenvios_realizados
    
    def resumo(self) -> dict:
        # Gerar um resumo das notificações enviadas, contando o total de notificações, quantas foram enviadas com sucesso e quantas falharam
        return {
            "total": len(self.historico),
            "emails_enviados": sum(1 for n in self.historico if n["email_enviado"]),
            "sms_enviados": sum(1 for n in self.historico if n["sms_enviado"]),
            "falhas_email": sum(1 for n in self.historico if not n["email_enviado"]),
            "falhas_sms": sum(1 for n in self.historico if not n["sms_enviado"])
        }
