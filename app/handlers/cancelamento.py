from app.services.supabase_client import supabase, get_user_by_whatsapp

def process(wa_id):
    user = get_user_by_whatsapp(wa_id)
    if user:
        supabase.table("users").delete().eq("id", user["id"]).execute()
        return {
            'statusCode': 200,
            'body': '{"resposta": "Seu cadastro foi cancelado e seus dados foram removidos com sucesso."}'
        }

    return {
        'statusCode': 200,
        'body': '{"resposta": "Você não está cadastrado ainda."}'
    }
