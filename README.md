# create-google-calendar-events-from-google-spreadsheets

```
python.exe -m pip install --upgrade pip
python -m venv venv
. venv/Scripts/activate
pip install -r requirements.txt
```
https://console.cloud.google.com/projectselector2/home/dashboard

Создаём проект
Подключаем API:
Создаём сервисный аккаунт(адрес вашего личного аккаунта в поле Service account admins role)
Получаем JSON-файл с ключом доступа к сервисному аккаунту

в таблице
файл
 > Поделиться
  > Jткрыть доступ
   > Указать client_email из JSON

в календаре
три точки
 > Настройки и общий доступ
  > Разрешения на доступ к мероприятиям client_email из JSON
  > Интеграция календаря
   > Идентификатор календаря скопировать