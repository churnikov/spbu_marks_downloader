# Marks downloader from my.spbu.ru

У этого сайта нет api, в него фиг попадешь через POST.

Потому нам на помощь приходит [selenium](http://selenium-python.readthedocs.io/). Библиотека для тестировщиков. Её преймущество, в данной ситуации, в том, что она моделирует поведение пользователя в браузере (буквально).

Тулза пока в Über сыром состоянии, так что есть желание немного допилить её, то милости просим с:

# Иструкции:
1. Необходимо поставить [Chrome](https://www.google.ru/chrome/browser/desktop/index.html)
2. `$ git clone https://github.com/kuparez/spbu_marks_downloader.git`
3. `$ pip3 install -r requirements.txt`
3. Создайте копию config_example.json с именем config.json или любым другим (тогда надо явно указать будет при запуске `python3 main.py --config config_name.json`)
4. Заполните свои `login` и `password` в `config.json`
6. `python3 main.py`

Теперь можно в два нажатия проверять, поставил тебе препод оценку или нет 👯‍♂️
