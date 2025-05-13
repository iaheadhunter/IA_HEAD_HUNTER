from app.services.supabase_client import supabase

def process(user, mensagem):
    supabase.table("interacoes").insert({
        "user_id": user["id"],
        "mensagem": mensagem,
        "tipo": "mensagem_recebida"
    }).execute()

    return {
        'statusCode': 200,
        'body': '{"status": "ok"}'
    }
