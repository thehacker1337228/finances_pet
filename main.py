import asyncio
from services.models import init_main
from app.routes import app




if __name__ == '__main__':
    asyncio.run(init_main())  # инитим создание таблиц (sqlalchemy)
    app.run(debug=True) # запускаем роуты (flask)
