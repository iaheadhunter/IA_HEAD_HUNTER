import json
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Função para extrair nome a partir do link
def extrair_nome(linkedin_url):
    return linkedin_url.rstrip('/').split("/")[-1].replace("-", " ").title()

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        wa_id = data["contacts"][0]["wa_id"]
        mensagem = data["messages"][0]["text"]["body"].strip().lower()

        # Verifica se o número já está cadastrado
        user = supabase.table("users").select("*").eq("whatsapp", wa_id).execute()

        if user.data:
            usuario = user.data[0]

            if mensagem == "cancelar":
                supabase.table("users").delete().eq("id", usuario["id"]).execute()
                return {
                    'statusCode': 200,
                    'body': json.dumps({'resposta': 'Seu cadastro foi cancelado e todos os dados foram removidos com sucesso.'})
                }

            # Registra interação
            supabase.table("interacoes").insert({
                "user_id": usuario["id"],
                "mensagem": mensagem,
                "tipo": "mensagem_recebida"
            }).execute()

            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'ok'})
            }

        # Verifica se existe cadastro pendente
        pendente = supabase.table("cadastros_pendentes").select("*").eq("whatsapp", wa_id).execute()
        if pendente.data:
            dados = pendente.data[0]

            # Se usuário responder "sim", criar cadastro definitivo
            if mensagem in ["sim", "s"]:
                supabase.table("users").insert({
                    "whatsapp": dados["whatsapp"],
                    "link": dados["link"],
                    "nome": dados["nome"],
                    "plano": "gratuito",
                    "consentimento_termo": True,
                    "versao_termo": "1.0",
                    "data_consentimento": datetime.utcnow().isoformat()
                }).execute()

                supabase.table("cadastros_pendentes").delete().eq("whatsapp", wa_id).execute()

                return {
                    'statusCode': 200,
                    'body': json.dumps({'resposta': f'Cadastro confirmado! Bem-vindo(a), {dados["nome"]}, ao IA Head Hunter!'})
                }

            # Se responder "não", não salva nada
            elif mensagem in ["não", "nao", "n"]:
                supabase.table("cadastros_pendentes").delete().eq("whatsapp", wa_id).execute()
                return {
                    'statusCode': 200,
                    'body': json.dumps({'resposta': 'Tudo bem! Seus dados não foram salvos. Se quiser começar depois, é só me enviar o LinkedIn novamente.'})
                }

        # Se a mensagem for um link do LinkedIn válido
        if mensagem.startswith("https://www.linkedin.com/in/"):
            nome = extrair_nome(mensagem)

            # Salva temporariamente
            supabase.table("cadastros_pendentes").insert({
                "whatsapp": wa_id,
                "link": mensagem,
                "nome": nome
            }).execute()

            return {
                'statusCode': 200,
                'body': json.dumps({'resposta': f'{nome}, quer seguir com o uso do IA Head Hunter e aceitar os termos? (responda com "sim" ou "não")'})
            }

        # Primeira mensagem genérica
        return {
            'statusCode': 200,
            'body': json.dumps({'resposta': 'Você é novo, né? 😄 Já sabe como eu funciono? Me envie o link do seu perfil do LinkedIn (começando com https://www.linkedin.com/in/).'})
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'erro': str(e)})
        }
