# Личный финансовый кошелек

Простое консольное приложение для учета личных доходов и расходов.

### Функционал:

* Вывод текущего баланса, а также доходов и расходов.
* Добавление, обновление и удаление записей.
* Поиск записей по сумме, дате или их диапазонам.
* Поиск записей по категории, описанию или по шаблону описания.
* Валидация ввода данных.
* Тесты, охватывающие каждую из команд.
* Хранение данных в CSV.

### Зависимости:

* Сlick: CLI интерфейс, валидация введенных данных.
* Tabulate: форматирование вывода данных в виде таблицы.

### Установка и запуск:

**1. С помощью Poetry:**
```
> poetry install
> poetry run personal_wallet balance
```
**2. С помощью Docker:**

```
> docker build . -t personal-wallet
> docker run -v data:/data personal-wallet balance
```

### Команды:

### 1. Вывод баланса

**Команда:** `balance`

**Описание:** Показывает текущий баланс, а также отдельно доходы и расходы.

**Пример использования:**

```
> personal_wallet balance
Current balance: 4500
Income: 1750
Expenses: 3050
```

### 2. Добавление записи

**Команда:** `add`

**Описание:** Добавляет новую запись о доходе или расходе.

**Параметры:**

* `-d` или `--date`: Дата записи (формат YYYY-MM-DD). Необязательный параметр. По умолчанию используется текущая дата.
* `-a` или `--amount`: Сумма записи. Обязательный параметр.
* `-c` или `--category`: Категория записи (income/expenses). Обязательный параметр.
* `-s` или `--description`: Описание записи. Необязательный параметр.

**Пример использования:**

```
> personal_wallet add -c income -a 33000 -s "Wrote an article for the blog"
Added transaction successfully!
```

### 3. Поиск по записям

**Команда:** `find`

**Описание:** Поиск записей по индексу, дате, сумме или категории.

**Параметры:**

* `-i` или `--index`: Индекс записи или диапазон индексов от..до (т.е., '1' или '1..15'). Необязательный параметр.
* `-d` или `--date`: Дата записи (формат YYYY-MM-DD) или диапазон дат от..до (т.е., '2024-05-08' или '2024-05-01..2024-05-09'). Необязательный параметр.
* `-a` или `--amount`: Сумма записи или диапазон сумм от..до (т.е., '100' или '50..200'). Необязательный параметр.
* `-c` или `--category`: Категория записи (income/expenses). Необязательный параметр.
* `-s` или `--description`: Описание записи или шаблон с % в начале и/или конце строки (т.е., 'Salary' или 'Sa%'). % заменяет любую последовательность символов. Необязательный параметр.

**Пример использования:**

```
> personal_wallet find -c expenses -d 2024-05-01
    date          amount  category    description
--  ----------  --------  ----------  -------------
 0  2024-05-01       550  expenses    Bought coffee
 1  2024-05-01      1700  expenses    Ordered food delivery
```

### 4. Обновление записи

**Команда:** `update`

**Описание:** Изменяет существующую запись о доходе или расходе.

**Параметры:**

* `-i` или `--index`: Индекс обновляемой записи. Обязательный параметр.
* `-c` или `--category`: Новая категория записи (income/expenses). Необязательный параметр.
* `-d` или `--date`: Дата записи (формат YYYY-MM-DD). Одиночная дата или диапазон от..до. Необязательный параметр.
* `-a` или `--amount`: Сумма записи. Одиночная сумма или диапазон от..до. Необязательный параметр.
* `-s` или `--description`: Новое описание записи. Необязательный параметр.

**Пример использования:**

```
> personal_wallet update -i 1 -a 500 -c income -s "Sold a painting."
Updated transaction successfully!
```

### 5. Удаление записи

**Команда:** `delete`

**Описание:** Удаляет существующую запись.

**Параметры:**

* `-i` или `--index`: Индекс удаляемой записи. Обязательный параметр.

**Пример использования:**

```
> personal_wallet delete -i 1
Deleted transaction successfully!
```

### 5. Дополнительные команды:

* `--help`: Отображает список доступных команд и их описание.
* `--version`: Отображает версию приложения.
* `--data-path`: Задает путь к директории хранения записей. По умолчанию записи сохраняются в директорию data в корневой директории проекта.
* `--config`: Задает путь к файлу конфигурации. По умолчанию - config.ini в корневой директории проекта.

### 6. Файл конфигурации:
Файл конфигурации в формате .ini может быть использован для установки значения по умолчанию для других параметров. Строки ключ=значение должны идти после секции `[options]`.

**Пример использования:**

```
[options]
data_path=D:\my_wallet_data
```
