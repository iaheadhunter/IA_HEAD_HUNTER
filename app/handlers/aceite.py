from datetime import datetime
from app.services.supabase_client import supabase, get_pending_user

def process(wa_id, mensagem):
    pendente = get_pending_user(wa_id)
    if not pendente:
        return {
            'statusCode': 200,
            'body': '{"resposta": "Não encontrei seu link. Por favor, envie novamente seu LinkedIn."}'
        }

    if mensagem in ["sim", "s"]:
        supabase.table("users").insert({
            "whatsapp": pendente["whatsapp"],
            "link": pendente["link"],
            "nome": pendente["nome"],
            "plano": "gratuito",
            "consentimento_termo": True,
            "versao_termo": "1.0",
            "data_consentimento": datetime.utcnow().isoformat()
        }).execute()

        supabase.table("cadastros_pendentes").delete().eq("whatsapp", wa_id).execute()

        return {
            'statusCode': 200,
            'body': f'{{"resposta": "Cadastro confirmado! Bem-vindo(a), {pendente["nome"]}."}}'
        }

    elif mensagem in ["não", "nao", "n"]:
        supabase.table("cadastros_pendentes").delete().eq("whatsapp", wa_id).execute()
        return {
            'statusCode': 200,
            'body': '{"resposta": "Tudo bem! Se quiser começar depois, é só me mandar seu LinkedIn."}'
        }

    return {
        'statusCode': 200,
        'body': '{"resposta": "Por favor, responda apenas com \\"sim\\" ou \\"não\\"."}'
    }
