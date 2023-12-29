# BeHome
Лучший хаб для умного дома

![Static Badge](https://img.shields.io/badge/Peshk0v-BeHome-BeHome)
![GitHub top language](https://img.shields.io/github/languages/top/peshk0v/BeHome)
![GitHub Repo stars](https://img.shields.io/github/stars/peshk0v/BeHome)
![GitHub issues](https://img.shields.io/github/issues/peshk0v/BeHome)

## Установа (LINUX, RASSBERRY/ORANGE PI)
Вы можете скачать exe файл из [РЕЛИЗОВ](https://github.com/peshk0v/BeHome/releases), или установить python версию:

1. Клонирование репозитория:
```git clone https://github.com/peshk0v/BeHome.git```
2. Переход в директорию:
```cd BeHome```
3. Установка зависимостей:
```pip install -r requirements.txt```
4. Поменяйте значения в файле `config.toml`:
<br> 1. В элементе `guard` вставьте свою учётную запись (Имя пользователя и Пароль)
<br> 2. В элементе `device` вставьте порт в который подключена Arduino
<br> 3. В элементе `output` вставьте названия устроиств и их пины, чтобы совпадало
5. Запустить программу:
```python main.py```

## Документация
Пользовательскую документацию можно получить по [этой ссылке](https://telegra.ph/LiveHome-12-27).

## Поддержка
Если у вас возникли сложности или вопросы по использованию, создайте [ОБСУЖДЕНИЕ](https://github.com/peshk0v/BeHome/issues/new/choose)
