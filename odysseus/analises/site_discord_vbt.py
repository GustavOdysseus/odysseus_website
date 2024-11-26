import os
import vectorbtpro as vbt
#from vectorbtpro import *
#from vectorbtpro.utils.knowledge.custom_assets import PagesAsset, MessagesAsset


# Configurar o token
token = "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"

# Configurar o token de duas maneiras possíveis:
# 1. Via variável de ambiente
os.environ["GITHUB_TOKEN"] = token

# 2. Via configurações do VBT (se a primeira não funcionar)
try:
    from vectorbtpro._settings import settings
    settings.knowledge.assets.vbt.token = token
except:
    pass

# Tentar carregar os assets com diferentes opções
try:
    # Opção 1: Carregar diretamente do GitHub
    pages_asset = vbt.PagesAsset.pull()
    messages_asset = vbt.MessagesAsset.pull()
except Exception as e:
    print(f"Erro ao carregar do GitHub: {e}")
    try:
        # Opção 2: Carregar de arquivos locais
        pages_asset = vbt.PagesAsset.from_json_file("pages.json.zip")
        messages_asset = vbt.MessagesAsset.from_json_file("messages.json.zip")
    except Exception as e:
        print(f"Erro ao carregar dos arquivos locais: {e}")
        raise

# Verificar se carregou corretamente
print("\nPáginas carregadas:", len(pages_asset) if 'pages_asset' in locals() else "Não carregado")
print("Mensagens carregadas:", len(messages_asset) if 'messages_asset' in locals() else "Não carregado")