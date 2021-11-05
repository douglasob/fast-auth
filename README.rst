Simple Auth FastAPI
===================


Facilita implementação de um sistema de autenticação básico e uso de uma
sessão de banco de dados em projetos com FastAPi.


Instalação e configuração
=========================

Instale usando pip ou seu o gerenciador de ambiente da sua preferencia:

    pip install simple-auth-fastapi

As configurações desta lib são feitas a partir de variáveis de ambiente.
Para facilitar a leitura dessas informações o simple-auth-fastapi
procura no diretório inicial(pasta onde o uvicorn ou gunicorn é chamado
iniciando o serviço web) o arquivo .env e faz a leitura dele.

Abaixo temos todas as variáveis de ambiente necessárias e em seguida a explição de cada uma:

    CONNECTION_STRING=postgresql+asyncpg://postgres:12345678@localhost:5432/fastapi 

    SECRET_KEY=1155072ced40aeb1865533335aaec0d88bbc47a996cafb8014336bdd2e719376
    
    TTL_JWT=60

- CONNECTION_STRING: Necessário para a conexão com o banco de dados. Gerealmente seguem o formato
  dialect+driver://username:password@host:port/database. O driver deve ser um que suporte execuções
  assíncronas como asyncpg para PostgreSQL, asyncmy para MySQL, para o SQLite o simple-auth-fastapi
  já trás o aiosqlite.

- SECRET_KEY: Para gerar e decodificar o token JWT é preciso ter uma chave secreta, que como o nome
  diz não deve ser pública. Para gerar essa chave pode ser utilizado o seguinte comando:

    openssl rand -hex 32

- TTL_JWT: O token JWT deve ter um tempo de vida o qual é especificado por essa variável. Este deve 
  ser um valor inteiro que ira representar o tempo de vida dos token em minutos. Caso não seja
  definido será utilizado o valor 1440 o equivalente a 24 horas.


Primeiros passos
================

Após a instalação e especificação da CONNECTION_STRING as tabelas podem ser criada no banco de dados
utilizando o seguinte comando no terminal:

    migrate

Este comando irá criar 3 tabelas, auth_users, auth_groups e auth_users_groups.
Tendo criado as tabelas, já será possível criar usuários pela linha de comando:

    create_user

Ao executar o comando será solicitado o username e password.

Como utilizar
=============

Toda a forma de uso foi construida seguindo o que consta na documentação do FastAPI

Conexao com banco de dados
--------------------------

Tendo a CONNECTION_STRING devidamente especificada, para ter acesso a uma sessão do banco de dados
a partir de uma path operation basta seguir o exemplo abaixo::

    from fastapi import FastAPI, Depends
    from sqlalchemy.ext.asyncio import AsyncSession
    from simple_auth_fastapi import connection_database, get_db

    connection_database()

    app = FastAPI()


    @app.get('/get_users')
    async def get_users(db: AsyncSession = Depends(get_db)):
        result = await db.execute('select * from auth_users')
        return [dict(user) for user in result]

Explicando o que foi feito acima, a função connection_database estabelece conexão com o banco de dados
passando a CONNECTION_STRING para o SQLAlchemy, mais especificamente para a função
create_async_engine.
No path operation passamos a função get_db como dependencia, sendo ele um generator que retorna
uma sessão assincrona já instanciada, basta utilizar conforme necessário e o simple_auth_fastapi mais o
prório fastapi ficam responsáveis por encerrar a sessão depois que a requisição é retornada.


Autenticação - Efetuando login
------------------------------

Abaixo um exemplo de rota para authenticação::

    from fastapi import FastAPI, Depends
    from pydantic import BaseModel
    from sqlalchemy.ext.asyncio import AsyncSession
    from simple_auth_fastapi import connection_database, authenticate, create_token_jwt

    connection_database()

    app = FastAPI()


    class SchemaLogin(BaseModel):
        username: str
        password: str


    @app.post('/login'):
    async def login(credentials: SchemaLogin):
        user = await authenticate(credentials.username, credentials.password)
        if user:
            token = create_token_jwt(user)
            return {'access': token}

A função authenticate é responsável por buscar no banco de dados o usuário informado
e checar se a senha confere, se estiver correto o usuário(objeto do tipo User que está
em simple_auth_fastapi.models) é retornado o qual deve ser passado como parâmetro para a 
função create_token_jwt que gera e retorna o token. No token fica salvo por padrão o id 
e o username do usuário, caso necessário, pode ser passado um dict como parametro com
informações adicionais para serem empacotadas junto.


Autenticação - requisição autenticada
-------------------------------------

O exemplo a seguir demonstra uma rota que só pode ser acessada por um usuário autenticado::

    from fastapi import FastAPI, Depends
    from pydantic import BaseModel
    from sqlalchemy.ext.asyncio import AsyncSession
    from simple_auth_fastapi import connection_database, require_auth

    connection_database()

    app = FastAPI()


    @app.get('/authenticated')
    def authenticated(payload: dict = Depends(require_auth)):
        #faz alguma coisa
        return {}


Para garantir que uma path operation seja executada apenas por usuários autenticados basta 
importar e passar ccomo dependência a função require_auth. Ela irá retornar os dados
que foram empacotados no token JWT.
