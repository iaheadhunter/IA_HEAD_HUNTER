from lambda_function import lambda_handler
import json

def simular_evento(wa_id, mensagem):
    return {
        "body": json.dumps({
            "contacts": [{
                "wa_id": wa_id,
                "profile": {"name": "Ignorado"}
            }],
            "messages": [{
                "text": {"body": mensagem}
            }]
        })
    }

# Número fixo para o teste
numero_teste = "5511999999999"

# Loop interativo
print("💬 Simulador de mensagens do WhatsApp (digite 'sair' para encerrar)")
while True:
    entrada = input("> Você: ").strip()
    if entrada.lower() in ["sair", "exit", "quit"]:
        break

    evento = simular_evento(numero_teste, entrada)
    resposta = lambda_handler(evento, None)
    corpo = json.loads(resposta["body"])
    print(f"🤖 IA Head Hunter: {corpo.get('resposta', corpo.get('status', corpo.get('erro', 'Erro desconhecido')))}")
