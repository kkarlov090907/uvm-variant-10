# uvm-variant-10
Учебная виртуальная машина (вариант 10)
### Архитектура:
- 32-битная виртуальная машина
- Стековая архитектура
- Объединенная память команд и данных
- Размер команды: 4 байта

### Команды:

#### load_const (код 50)
Биты 0-5: 50 (0x32)
Биты 6-26: константа.
Загружает константу в стек

#### read_value (код 33)
Биты 0-5: 33 (0x21).
Читает значение из памяти по адресу из стека.

#### write_value (код 16)
Биты 0-5: 16 (0x10)
Биты 6-17: смещение.
Записывает значение в память по адресу (адрес + смещение).

#### shift_right (код 10)
Биты 0-5: 10 (0x0A)
Биты 6-17: смещение.
Выполняет побитовый арифметический сдвиг вправо.

### Тестовые примеры из спецификации:
- load_const: A=50, B=383 → 0xF2, 0x5F, 0x00, 0x00
- read_value: A=33 → 0x21, 0x00, 0x00, 0x00
- write_value: A=16, B=13 → 0x50, 0x03, 0x00, 0x00
- shift_right: A=10, B=962 → 0x8A, 0xF0, 0x00, 0x00

## Использование

### CLI ассемблер:
python uvm_asm.py -i program.asm -o program.bin -t 1
python uvm_interp.py -i program.bin -o dump.json -r 0-10
python uvm_gui.py

## Простая программа:
load_const;0
load_const;100
write_value;0

## Сдвиг векторов:
load_const;0
load_const;100
write_value;0
load_const;1
load_const;50
write_value;0
load_const;2
load_const;25
write_value;0
load_const;3
load_const;12
write_value;0
load_const;4
load_const;6
write_value;0
