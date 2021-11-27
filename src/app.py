from sanic import Sanic
from src.database.database import connection
from src.models import tables
from src.routes import routes
from src.models.vpn_user import UserVPN

app = Sanic(__name__)
app.blueprint(routes)


@app.listener('before_server_start')
async def create_tables(server: Sanic, _):
    try:
        connection.create_tables(
            tables
        )
    except Exception as e:
        print("Error ao setar o db: ", str(e))
        pass


@app.listener('before_server_start')
async def creat_user_admin(server: Sanic, _):
    with connection.atomic() as trasaction:
        try:
            UserVPN.create(
                name="admin",
                username="admin",
                password="123456",
                admin="1"
            )
        except Exception as e:
            print("Error ao criar admin o db: ", str(e))
            pass


@app.listener('after_server_start')
async def depois(server: Sanic, _):
    print('depois do server iniciar')
