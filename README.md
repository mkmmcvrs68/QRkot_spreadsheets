# Описание проекта
  Приложение QRKot
    Смысл приложения: Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
  
  
  UPDATE
    Добавлена возможность создать отчет по закрытым проектам
  
 
# Запуск проекта
  1) Клонировать репозиторий:
    ```
    git clone https://github.com/mkmmcvrs68/cat_charity_fund
    ```
  2) Cоздать виртуальное окружение:

    ```
    python3 -m venv venv
    или 
    python -m venv venv (Windows)
    ```
  3) Активировать виртуальное окружение:
    ```
    source venv/bin/activate
    или
    source venv/scripts/activate (Windows)
    ```

  4) Установить зависимости из файла requirements.txt:
    ```
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```
  5) Создать и заполнить файл .env по примеру из .env.example:
    ```
    touch .env
    ```
  6) Применение миграций:
    ```
    alembic upgrade head
    ```
  7) Запуск проекта:
    ```
    uvicorn app.main:app --reload
    ```

# Проект и документация
  Локальный доступ к API: http://127.0.0.1:8000
  Автоматически сгенерированная документация Swager: http://127.0.0.1:8000/docs
  

# Стек 
  * Python 3.9.10
  * FastAPI
  * SQLAlchemy
  * Uvicorn[standart]
  * Alembic
  * Pydantic
  Update
  * Google Drive API
  * Google Sheets API

# Автор
  [Козлов Максим](https://github.com/mkmmcvrs68)
  mkvrs68@gmail.com