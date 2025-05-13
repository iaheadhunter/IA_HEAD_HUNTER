from app.services.supabase_client import supabase
from app.services.utils import is_linkedin_url

def primeiro_contato(wa_id, mensagem):
    # Checa se existe cadastro
    user = supabase.table("users").select("id").eq("whatsapp", wa_id).execute()
    if user.data:
        return None  # já é cadastrado, o handler principal decide

    # Verifica se já está em contato pendente
    pendente = supabase.table("cadastros_pendentes").select("*").eq("whatsapp", wa_id).execute()
    if not pendente.data:
        # Primeira mensagem de um novo número
        supabase.table("cadastros_pendentes").insert({
            "whatsapp": wa_id,
            "estado": "aguardando_confirmacao"
        }).execute()
        return {
            'statusCode': 200,
            'body': '{"resposta": "Você é novo, né? 😄 Já sabe como eu funciono? (responda com \\"sim\\" ou \\"não\\")"}'
        }

    estado = pendente.data[0].get("estado", "")

    if estado == "aguardando_confirmacao":
        if mensagem in ["sim", "s"]:
            supabase.table("cadastros_pendentes").update({
                "estado": "aguardando_aceite"
            }).eq("whatsapp", wa_id).execute()
            return {
                'statusCode': 200,
                'body': '{"resposta": "Legal! Aqui está o termo de uso: [link do termo]. Por favor, responda \\"aceito\\" para continuar."}'
            }

        elif mensagem in ["não", "n", "nao"]:
            return {
                'statusCode': 200,
                'body': '{"resposta": "Sem problema! Eu sou sua assistente que te ajuda a se candidatar automaticamente a vagas com base no seu LinkedIn. Posso continuar? (responda \\"sim\\" para aceitar o termo de uso)."}'
            }

    return None
