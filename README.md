# Face-Recognition

## Небольшая система для классификации изображений  

### Development  

Для разработки необходим Python 3.9  
В корневой папке создайте виртуальное окружение с помощью следующей команды:
~~~console
python -m venv venv
~~~
Запустите виртуальное окружение и установите зависимости с помощью команды:  
~~~console
pip install -r requirements.txt
~~~
Создайте папки с названием "ORL" и "results" по пути "./data/" и запустите метод upload() по пути "./src/core/utils/load_data.py"  
Запустить можно простым созданием файла с вызовом метода.  
Данный метод загрузит все изображения из базы ORL.  

Для запуска системы выполните слудющую команду:
~~~console
python src/main.py
~~~
