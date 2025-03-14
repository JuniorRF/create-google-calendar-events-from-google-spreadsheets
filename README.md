# create-google-calendar-events-from-google-spreadsheets
### Программа собирает информацию из таблиц Google  
### \> создает меропритие в календаре Goоgle  
### \> вставляет ссылку на событие в календарь

Python 3.10.9
```
pip install -r requirements.txt
```
https://console.cloud.google.com/projectselector2/home/dashboard

1. Создаём проект
2. Подключаем API:
   - [Google Calendar API](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com)
   - [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com)
3. Создаём сервисный аккаунт(адрес вашего личного аккаунта в поле Service account admins role)
4. Получаем JSON-файл с ключом доступа к сервисному аккаунту
5. Переименовать файл в keys.json и положить в папку программы

в таблице
* файл
* \>Поделиться
* \>\>Открыть доступ
* \>\>\>Указать `client_email` из JSON
* \>\>\>\> Назначить редактором
* \>\>\>\>\> В `settings.py` указать `SPREED_SHEETS_ID` 
*  https://docs.google.com/spreadsheets/d/<`SPREED_SHEETS_ID`>/edit?gid=0#gid=0

в календаре
* три точки
* \> Настройки и общий доступ
* \>\> Разрешения на доступ к мероприятиям
* \>\>\> вставить `client_email` из JSON, права **Внесение изменений в мероприятия** или выше
* \>\> Интеграция календаря
* \>\>\> Идентификатор календаря указать в `settings.py` `CALENDAR_ID` 
* основной календарь собственная почта 
* иные 8b472d96c37bc493132f374d99@group.calendar.google.com  

### Запуск программы из cmd  
#### перейти в папку с программой 
#### `python main.py`