from odmantic import AIOEngine

from main import app

market_screener_engine = AIOEngine(motor_client=app.state.mongoClient, database="market_screener")
