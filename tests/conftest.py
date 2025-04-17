# Em resumo, este código configura um ambiente de teste completo para uma aplicação web assíncrona (dio_blog):
#
# Define um banco de dados SQLite em memória para os testes.
# Cria e destrói as tabelas do banco de dados antes e depois de cada conjunto de testes.
# Cria um cliente HTTP assíncrono que se comunica diretamente com a aplicação ASGI.
# Fornece um token de acesso simulado para testes que exigem autenticação.
# Ao usar essas fixtures em suas funções de teste (funções definidas com async def e que recebem essas fixtures como argumentos), você pode interagir com sua aplicação em um ambiente isolado e controlado. Por exemplo, um teste poderia receber o client para fazer requisições a diferentes rotas da aplicação e o db para verificar o estado do banco de dados. O access_token seria usado para fazer requisições autenticadas.

# ==========================================================================
# Em resumo, o arquivo conftest.py é o local ideal para colocar qualquer código de suporte aos seus testes que
# você deseja compartilhar entre vários arquivos de teste dentro de um diretório.
# Ele simplifica a configuração e promove a escrita de testes mais limpos e reutilizáveis.
#
# No seu exemplo, o conftest.py contém as fixtures db, client e access_token,
# que são recursos essenciais para testar a aplicação dio_blog.
# Ao colocá-las em conftest.py, qualquer arquivo de teste dentro do mesmo diretório (ou subdiretórios)
# pode simplesmente declarar essas fixtures como argumentos em suas funções de teste para utilizá-las.
# ==========================================================================

try:
    import os

    os.environ.setdefault("DATABASE_URL", "sqlite:///tests.db")
except ImportError:
    raise ImportError("Erro ao importar e setar a variavel de ambiente!")


import asyncio  # Biblioteca padrão do Python para programação assíncrona.

import pytest_asyncio  # Um plugin do pytest que suporta a execução de testes assíncronos (funções definidas com async def).
from httpx import (  # httpx: Uma biblioteca HTTP assíncrona que será usada para fazer requisições HTTP para a aplicação de teste. ASGITransport é usado para interagir diretamente com aplicações ASGI (Asynchronous Server Gateway Interface), como aquelas construídas com frameworks como FastAPI (que provavelmente é o caso de dio_blog). AsyncClient é um cliente HTTP assíncrono fornecido por httpx.
    ASGITransport,
    AsyncClient,
)

try:
    from dio_blog.config import settings

    settings.DATABASE_URL = "sqlite:///tests.db"
except ImportError:
    raise ImportError("Erro ao importar e setar a configurações!")


# @pytest_asyncio.fixtur Um decorador que marca a função db como uma fixture assíncrona do pytest-asyncio. Fixtures são funções que fornecem recursos para os testes.


@pytest_asyncio.fixture
async def db(
    request,
):  # Define uma função assíncrona chamada db que recebe o objeto request do pytest.
    from dio_blog.database import (
        database,  # noqa # pylint: disable=C0415
        engine,
        metadata,
    )
    from dio_blog.models.post import posts  # noqa  # pylint: disable=C0415

    await database.connect()  # Estabelece uma conexão assíncrona com o banco de dados.
    metadata.create_all(engine)  # Cria todas as tabelas definidas nos modelos do SQLAlchemy (provavelmente onde posts está definido) no banco de dados.

    #  A função interna teardown() é definida para ser executada após todos os testes que utilizam esta fixture serem concluídos.
    def teardown():
        async def _teardown():  # Define uma função assíncrona interna para desconectar e remover as tabelas.
            await database.disconnect()  # Desconecta do banco de dados.
            metadata.drop_all(engine)  # Remove todas as tabelas do banco de dados.

        asyncio.run(_teardown())  # Executa a função assíncrona _teardown() de forma síncrona

    request.addfinalizer(teardown)  # Registra a função teardown para ser chamada após a execução dos testes que dependem desta fixture. Isso garante que o banco de dados seja limpo após cada conjunto de testes.


@pytest_asyncio.fixture
async def client(db):
    from dio_blog.main import app

    transport = ASGITransport(app=app)  # transport = ASGITransport(app=app): Cria um transporte ASGITransport do httpx, que permite fazer requisições diretamente para a aplicação ASGI sem precisar de um servidor HTTP real rodando.
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }  # Define um dicionário com cabeçalhos HTTP padrão que serão usados nas requisições (indicando que esperamos e enviaremos dados em formato JSON).
    # Cria um cliente HTTP assíncrono (AsyncClient) do httpx. O async with garante que o cliente seja fechado corretamente após o uso.
    # base_url="http://test": Define uma URL base para as requisições (o host "test" é comum em testes).
    # transport=transport: Usa o transporte ASGI criado para interagir com a aplicação.
    # headers=headers: Define os cabeçalhos padrão.
    # yield client: Em vez de retornar diretamente, yield transforma a fixture em um gerador. O valor após o yield (neste caso, o client) é fornecido aos testes que dependem desta fixture. O código após o yield seria executado após todos os testes que usam este cliente serem finalizados (embora aqui não haja código após o yield).
    async with AsyncClient(base_url="http://test", transport=transport, headers=headers) as client:
        yield client


@pytest_asyncio.fixture
async def access_token(client: AsyncClient):
    response = await client.post("/auth/login", json={"user_id": 1})
    return response.json()["access_token"]  # Assume que a resposta da requisição de login é um JSON contendo um campo chamado access_token, que é retornado pela fixture. Essa fixture provavelmente é usada em outros testes que precisam de um token de acesso autenticado.
