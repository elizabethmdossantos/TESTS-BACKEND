import random
from notificacoes import templates
from notificacoes import servico
from notificacoes import sms


class GerenciadorDeNotificacoes:

    def __init__(self):
        self.historico: list[dict] = [] # inicializar o histórico de notificações como uma lista vazia

    def notificar_usuario(self, nome: str, email: str, telefone: str) -> dict:
        templates.boas_vindas = templates.boas_vindas(nome)

        email_sucesso = servico.enviar_email(
            destinatario=email,
            assunto=templates.boas_vindas['assunto'],
            corpo=templates.boas_vindas['corpo'])
        
        codigo_sms = random.randint(100000, 999999)
        sms_sucesso = sms.enviar_codigo_verificacao(telefone=telefone, codigo=str(codigo_sms))

        registro = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "email_enviado": email_sucesso,
            "sms_enviado": sms_sucesso
        }

        self.historico.append(registro)
        return registro

    def reenviar_falhas(self) -> int:
        reenvios_realizados = 0
        for notificacao in self.historico:
            houve_falha = False

            if not notificacao["email_enviado"]:
                templates.boas_vindas = templates.boas_vindas(notificacao["nome"])

                notificacao["email_enviado"] = servico.enviar_email(
                    destinatario=notificacao["email"],
                    assunto=templates.boas_vindas['assunto'],
                    corpo=templates.boas_vindas['corpo']
                )
                houve_falha = True

            if not notificacao["sms_enviado"]:
                codigo_sms = random.randint(100000, 999999)
                notificacao["sms_enviado"] = sms.enviar_codigo_verificacao(
                    telefone=notificacao["telefone"], 
                    codigo=str(codigo_sms)
                )
                houve_falha = True

            if houve_falha:
                reenvios_realizados += 1

        return reenvios_realizados
    
    def resumo(self) -> dict:
        return {
            "total": len(self.historico),
            "emails_enviados": sum(1 for n in self.historico if n["email_enviado"]),
            "sms_enviados": sum(1 for n in self.historico if n["sms_enviado"]),
            "falhas_email": sum(1 for n in self.historico if not n["email_enviado"]),
            "falhas_sms": sum(1 for n in self.historico if not n["sms_enviado"])
        }
