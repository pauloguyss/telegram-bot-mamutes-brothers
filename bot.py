import os
import re
import random
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]

# URL pública do serviço (ex: https://seu-app.onrender.com).
# No Render, você pode usar a variável automática RENDER_EXTERNAL_URL.
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") or os.environ.get("RENDER_EXTERNAL_URL")

# Porta que o servidor vai escutar (Render define isso automaticamente em PORT)
PORT = int(os.environ.get("PORT", "8080"))

# Caminho secreto do webhook (usa o próprio token, mais difícil de adivinhar)
WEBHOOK_PATH = BOT_TOKEN

# --- Regra 1: variações de "daku" -> resposta fixa ---
# Cobre: daku, dacu, da cu, da ku (com ou sem espaço, k ou c)
PADRAO_DAKU = re.compile(r"\bda\s*[ck]u\b", re.IGNORECASE)
RESPOSTA_DAKU = "Esse aí é o @UrsoPimpao"

# --- Regra 2: menção a @Junho -> frase aleatória ---
VERBOS = [
    "dançando", "dormindo", "correndo", "aprontando", "sumido",
    "trabalhando", "viajando", "comendo", "bebendo", "cantando",
    "pescando", "surfando", "estudando", "sonhando", "perdido",
    "nadando", "pulando", "gritando", "chorando", "rindo",
    "brigando", "namorando", "flertando", "dirigindo", "pilotando",
    "escalando", "mergulhando", "acampando", "caçando", "colhendo",
    "plantando", "cozinhando", "assando", "fritando", "lavando",
    "varrendo", "arrumando", "consertando", "quebrando", "construindo",
    "demolindo", "pintando", "desenhando", "esculpindo", "fotografando",
    "filmando", "gravando", "editando", "programando", "hackeando",
    "jogando", "apostando", "negociando", "vendendo", "comprando",
    "roubando", "escondendo", "procurando", "achando", "perdendo",
    "ganhando", "comemorando", "festejando", "bebericando", "cochilando",
    "roncando", "acordando", "levantando", "caindo", "tropeçando",
    "voando", "flutuando", "mergulhado", "afundando", "boiando",
    "remando", "pedalando", "patinando", "esquiando", "surfando",
    "meditando", "orando", "rezando", "cantarolando", "assobiando",
    "discutindo", "debatendo", "palestrando", "ensinando", "aprendendo",
    "treinando", "malhando", "alongando", "descansando", "relaxando",
    "viajando", "passeando", "explorando", "investigando", "espionando",
    "negociando", "empreendendo", "planejando", "sonhando", "improvisando",
]

CIDADES = [
    "São Paulo - SP", "Rio de Janeiro - RJ", "Salvador - BA",
    "Manaus - AM", "Curitiba - PR", "Fortaleza - CE",
    "Belo Horizonte - MG", "Recife - PE", "Florianópolis - SC",
    "Belém - PA", "Cuiabá - MT", "Natal - RN", "Maceió - AL",
    "Goiânia - GO", "Vitória - ES", "Campo Grande - MS",
    "João Pessoa - PB", "Aracaju - SE", "Teresina - PI", "São Luís - MA",
    "Palmas - TO", "Macapá - AP", "Boa Vista - RR", "Rio Branco - AC",
    "Brasília - DF", "Porto Alegre - RS", "Campinas - SP", "Santos - SP",
    "Guarulhos - SP", "Osasco - SP", "Sorocaba - SP", "Ribeirão Preto - SP",
    "São José dos Campos - SP", "Niterói - RJ", "Duque de Caxias - RJ",
    "Nova Iguaçu - RJ", "Petrópolis - RJ", "Uberlândia - MG", "Contagem - MG",
    "Juiz de Fora - MG", "Betim - MG", "Londrina - PR", "Maringá - PR",
    "Ponta Grossa - PR", "Joinville - SC", "Blumenau - SC", "Chapecó - SC",
    "Caxias do Sul - RS", "Pelotas - RS", "Santa Maria - RS", "Gramado - RS",
    "Feira de Santana - BA", "Vitória da Conquista - BA", "Ilhéus - BA",
    "Porto Seguro - BA", "Caruaru - PE", "Olinda - PE", "Petrolina - PE",
    "Campina Grande - PB", "Mossoró - RN", "Imperatriz - MA",
    "Parnaíba - PI", "Marabá - PA", "Santarém - PA", "Altamira - PA",
    "Foz do Iguaçu - PR", "Balneário Camboriú - SC", "Itajaí - SC",
    "Uberaba - MG", "Montes Claros - MG", "Governador Valadares - MG",
    "Anápolis - GO", "Rio Verde - GO", "Águas Lindas - GO",
    "Dourados - MS", "Corumbá - MS", "Sinop - MT", "Rondonópolis - MT",
    "Barretos - SP", "Piracicaba - SP", "Bauru - SP", "Franca - SP",
    "Presidente Prudente - SP", "Jundiaí - SP", "Taubaté - SP",
    "Volta Redonda - RJ", "Campos dos Goytacazes - RJ", "Angra dos Reis - RJ",
    "Búzios - RJ", "Paraty - RJ", "Gramado do Sul - RS", "Bento Gonçalves - RS",
    "Novo Hamburgo - RS", "São Leopoldo - RS", "Bagé - RS",
    "Criciúma - SC", "Lages - SC", "Itabuna - BA", "Camaçari - BA",
    "Juazeiro do Norte - CE", "Sobral - CE", "Crato - CE",
    "Ji-Paraná - RO", "Vilhena - RO", "Cacoal - RO", "Ariquemes - RO",
    "Gaspar - SC", "Tubarão - SC", "Araraquara - SP", "Marília - SP",
]


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text or ""
    texto_lower = texto.lower()

    if PADRAO_DAKU.search(texto_lower):
        await update.message.reply_text(RESPOSTA_DAKU)
        return

    if "@junho" in texto_lower:
        verbo = random.choice(VERBOS)
        cidade = random.choice(CIDADES)
        await update.message.reply_text(f"O Juim está {verbo} lá em {cidade}")
        return


def main():
    if not WEBHOOK_URL:
        raise RuntimeError(
            "Defina a variável de ambiente WEBHOOK_URL (ex: https://seu-app.onrender.com)"
        )

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    full_webhook_url = f"{WEBHOOK_URL.rstrip('/')}/{WEBHOOK_PATH}"

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=WEBHOOK_PATH,
        webhook_url=full_webhook_url,
    )


if __name__ == "__main__":
    main()
