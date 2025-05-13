from app.services.supabase_client import supabase
from app.services.utils import extrair_nome

def iniciar(wa_id, link):
    nome = extrair_nome(link)

    supabase.table("cadastros_pendentes").insert({
        "whatsapp": wa_id,
        "link": link,
        "nome": nome
    }).execute()

    return {
        'statusCode': 200,
        'body': f'{{"resposta": "{nome}, quer seguir com o uso do IA Head Hunter e aceitar os termos? (responda com \\"sim\\" ou \\"não\\")"}}'
    }
