# Marks downloader from my.spbu.ru

У этого сайта нет api, в него фиг попадешь через POST.

Потому нам на помощь приходит [selenium](http://selenium-python.readthedocs.io/). Библиотека для тестировщиков. Её преймущество, в данной ситуации, в том, что она моделирует поведение пользователя в браузере (буквально).

Тулза пока в Über сыром состоянии, так что есть желание немного допилить её, то милости просим с:

# Иструкции:
1. Необходимо поставить [Chrome](https://www.google.ru/chrome/browser/desktop/index.html)
2. `$ git clone https://github.com/kuparez/spbu_marks_downloader.git`
3. `$ pip3 install -r requirements.txt`
4. Заполните свои `LOGIN` и `PASSWORD` в `config.py`
5. В `main.py` надо поправить следующие поля:
  1. 42 строка: `driver = webdriver.Chrome('chromedriver')` - Скорее всего, надо указать абсолютный путь до файла
  2. 86 и 90 строки: `with open('path/to/downloads/Оценка.csv', 'r') as f:` - Надо указать полный путь, куда Chrome сохраняет у вас данные
6. `python3 main.py`

Теперь можно в два нажатия проверять, поставил тебе прпод оценку или нет 👯‍♂️
