# ProjectFASTApi
# Name
Menu Restoran
# Discription
Проект по созданию разных меню, у меню может быть несколько подменю у разных меню не может быть двух одинаковых подменю
у подменю есть блюда у двух разных подменю не может быть двух разных блюд
в Меню ведется подсчет сколько разделов подменю и сколько блюд
в разделе Подменю ведется подсчет сколько в нем блюд
у каждого блюда есть дополнительное поле цена
при удаление блюда или подменю происходит пересчет количества блюд и подменю в разделах меню и подменю
#star project:
python main.py or run main.py or uvicorn app:app --reload --host 0.0.0.0 --port 8000
# work docker
Для запуска в файле db.py в каталоге core следует раскоментировать строчку:
#SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:space@restoran_db/restoran_m"
и закоментировать:
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:space@localhost/restoran_m"
для запуска в среде python сделать наоборот
сборка команда
docker-compose up -d --build
запуск
docker-compos up -d
#pytest
для запуска тестов используется тестовая база restoran_pytest
имя базы настраивается в ./core/db.py
если база не существует она создается

для тестов docker используется в настройках две сети по необходимости не нужное можно закоментировать
...
    networks:
      - test_network
      - another_network

networks:
  test_network:
      name: restoran_network
  another_network:
    name: another_network
