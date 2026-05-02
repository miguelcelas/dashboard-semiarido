import feedparser
import json
from datetime import datetime, timedelta

# Configuração de fontes (Fácil de adicionar novas)
FONTES = [
    {"nome": "Marco Zero", "url": "https://marcozero.org/feed/", "estado": "PE"},
    {"nome": "Agência Eco Nordeste", "url": "https://agenciaeconordeste.com.br/feed/", "estado": "CE"},
    {"nome": "Agência Saiba Mais", "url": "https://saibamais.jor.br/feed/", "estado": "RN"},
    {"nome": "Diário do Sertão", "url": "https://www.diariodosertao.com.br/feed/", "estado": "PB"},
    # Para sites sem RSS, o ideal é usar BeautifulSoup futuramente
]

def buscar_noticias():
    data_limite = datetime(2026, 1, 1)
    noticias_filtradas = []

    for fonte in FONTES:
        try:
            feed = feedparser.parse(fonte['url'])
            for entrada in feed.entries:
                # Converte a data da notícia
                data_pub = datetime(*entrada.published_parsed[:6])
                
                if data_pub >= data_limite:
                    # Limpa o resumo para 180 caracteres
                    resumo_limpo = entrada.summary[:178] + ".." if len(entrada.summary) > 180 else entrada.summary
                    
                    noticias_filtradas.append({
                        "manchete": entrada.title,
                        "resumo": resumo_limpo,
                        "veiculo": fonte['nome'],
                        "link": entrada.link,
                        "estado": fonte['estado'],
                        "data": data_pub.strftime("%d/%m/%Y"),
                        "paywall": False # Pode ser ajustado conforme a fonte
                    })
        except Exception as e:
            print(f"Erro ao ler {fonte['nome']}: {e}")

    # Salva o resultado em um JSON que o Dashboard vai ler
    with open('noticias.json', 'w', encoding='utf-8') as f:
        json.dump(noticias_filtradas, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    buscar_noticias()
