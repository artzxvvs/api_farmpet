import traceback

try:
    from main import app
    print('Importou main.app com sucesso. Gerando OpenAPI...')
    schema = app.openapi()
    print('OpenAPI gerado com sucesso. Tamanho:', len(str(schema)))
except Exception as e:
    print('Erro ao gerar OpenAPI:')
    traceback.print_exc()
    raise
