import argparse
import json


def mask(n):
    """Создает битовую маску из n битов"""
    return (1 << n) - 1


def execute(bytecode):
    """Выполняет байткод УВМ"""
    stack = []
    memory = [0] * 100  # Память данных

    i = 0
    while i < len(bytecode):
        # Читаем команду (4 байта)
        command_bytes = bytecode[i:i + 4]
        command_int = int.from_bytes(command_bytes, 'little')

        # Извлекаем код операции (биты 0-5)
        opcode = command_int & mask(6)

        print(f"Команда {i // 4}: opcode={opcode}, stack={stack}")

        if opcode == 50:  # load_const
            # Извлекаем константу (биты 6-26)
            constant = (command_int >> 6) & mask(21)
            stack.append(constant)
            print(f"  load_const {constant}")

        elif opcode == 33:  # read_value
            address = stack.pop()
            value = memory[address]
            stack.append(value)
            print(f"  read_value from [{address}] = {value}")

        elif opcode == 16:  # write_value - ИСПРАВЛЕНО!
            # Извлекаем смещение (биты 6-17)
            offset = (command_int >> 6) & mask(12)
            value = stack.pop()  # Сначала значение
            address = stack.pop()  # Потом адрес
            memory[address + offset] = value
            print(f"  write_value {value} to [{address} + {offset}]")

        elif opcode == 10:  # shift_right
            # Извлекаем смещение (биты 6-17)
            offset = (command_int >> 6) & mask(12)
            shift_amount = stack.pop()
            base_address = stack.pop()
            value_address = base_address + offset
            value = memory[value_address]
            result = value >> shift_amount  # Арифметический сдвиг вправо
            memory[base_address] = result
            print(f"  shift_right [{value_address}]={value} >> {shift_amount} = {result} to [{base_address}]")

        else:
            print(f"  Неизвестный opcode: {opcode}")
            break

        i += 4

    return stack, memory


def main():
    parser = argparse.ArgumentParser(description='Интерпретатор УВМ вариант 10')
    parser.add_argument('-i', '--input', required=True, help='Входной бинарный файл')
    parser.add_argument('-o', '--output', required=True, help='Выходной файл дампа памяти')
    parser.add_argument('-r', '--range', required=True, help='Диапазон адресов (например: 0-10)')
    args = parser.parse_args()

    # Читаем байткод
    with open(args.input, "rb") as file:
        bytecode = file.read()

    print(f"Загружено байт: {len(bytecode)}")

    # Выполняем программу
    stack, memory = execute(bytecode)

    # Сохраняем дамп памяти в JSON
    start, end = map(int, args.range.split('-'))
    memory_dump = {f"addr_{i}": memory[i] for i in range(start, end + 1)}

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(memory_dump, f, indent=2, ensure_ascii=False)

    print(f"\nРезультат выполнения:")
    print(f"Стек: {stack}")
    print(f"Память (первые 10 ячеек): {memory[:10]}")
    print(f"Дамп памяти сохранен в {args.output}")


if __name__ == "__main__":
    main()