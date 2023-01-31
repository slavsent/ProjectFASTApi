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
python main.py or run main.py в IDE
# work docker
сборка команда
docker-compose up -d --build
запуск
docker-compos up -d
#pytest
для запуска тестов в IDE: run ./test/testing.py
для запуска тестов в docker-compose используется тестовая база restoran_pytest
имя базы настраивается в .env
если база не существует она создается
сборка команда
docker-compose -f docker-compose.tests.yml up -d --build
запуск
docker-compos -f docker-compose.tests.yml up -d
#файл .env
пример файла: example.env


