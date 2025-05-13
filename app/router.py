from app.handlers import cadastro, aceite, interacao, cancelamento
from app.services.utils import is_linkedin_url
from app.services.supabase_client import get_user_by_whatsapp, get_pending_user

def handle(event):
    try:
        data = event["body"] if isinstance(event["body"], dict) else eval(event["body"])
        wa_id = data["contacts"][0]["wa_id"]
        mensagem = data["messages"][0]["text"]["body"].strip().lower()

        user = get_user_by_whatsapp(wa_id)

        if user:
            return interacao.process(user, mensagem)

        if mensagem == "cancelar":
            return cancelamento.process(wa_id)

        if is_linkedin_url(mensagem):
            return cadastro.iniciar(wa_id, mensagem)

        if mensagem in ["sim", "não", "nao", "n", "s"]:
            return aceite.process(wa_id, mensagem)

        return {"statusCode": 200, "body": '{"resposta":"Você é novo, né? 😄 Já sabe como eu funciono? Me envie seu LinkedIn!"}'}

    except Exception as e:
        return {"statusCode": 400, "body": f'{{"erro": "{str(e)}"}}'}
