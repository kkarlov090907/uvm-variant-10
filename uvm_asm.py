import argparse
import pprint
def asm_load_const(const: int):
    """Загрузка константы - код 50"""
    output = 0
    output |= 50  # Код операции в битах 0-5
    output |= (const << 6)  # Константа в битах 6-26
    return output.to_bytes(4, 'little')
def asm_read_value():
    """Чтение из памяти - код 33"""
    output = 0
    output |= 33  # Код операции в битах 0-5
    return output.to_bytes(4, 'little')
def asm_write_value(offset: int):
    """Запись в память - код 16"""
    output = 0
    output |= 16  # Код операции в битах 0-5
    output |= (offset << 6)  # Смещение в битах 6-17
    return output.to_bytes(4, 'little')
def asm_shift_right(offset: int):
    """Сдвиг вправо - код 10"""
    output = 0
    output |= 10  # Код операции в битах 0-5
    output |= (offset << 6)  # Смещение в битах 6-17
    return output.to_bytes(4, 'little')
def test_commands():
    """Тестируем команды согласно спецификации"""
    print("Тестируем команды...")

    # Тест 1: load_const
    result = list(asm_load_const(383))
    expected = [0xF2, 0x5F, 0x00, 0x00]
    print(f"load_const(383): {result} == {expected} -> {result == expected}")

    # Тест 2: read_value
    result = list(asm_read_value())
    expected = [0x21, 0x00, 0x00, 0x00]
    print(f"read_value(): {result} == {expected} -> {result == expected}")

    # Тест 3: write_value
    result = list(asm_write_value(13))
    expected = [0x50, 0x03, 0x00, 0x00]
    print(f"write_value(13): {result} == {expected} -> {result == expected}")

    # Тест 4: shift_right
    result = list(asm_shift_right(962))
    expected = [0x8A, 0xF0, 0x00, 0x00]
    print(f"shift_right(962): {result} == {expected} -> {result == expected}")
def asm(intermediate_representation):
    """Преобразуем промежуточное представление в байткод"""
    bytecode = bytes()
    for op, *args in intermediate_representation:
        if op == 'load_const':
            bytecode += asm_load_const(args[0])
        elif op == 'read_value':
            bytecode += asm_read_value()
        elif op == 'write_value':
            bytecode += asm_write_value(args[0])
        elif op == 'shift_right':
            bytecode += asm_shift_right(args[0])
        else:
            print(f"Ошибка: неизвестная команда {op}")
    return bytecode
def full_asm(text):
    """Полный ассемблер: текст -> промежуточное представление -> байткод"""
    text = text.strip()
    intermediate_representation = []

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):  # Пропускаем пустые строки и комментарии
            continue

        if ';' in line:
            cmd, arg = line.split(';')
            intermediate_representation.append((cmd, int(arg)))
        else:
            intermediate_representation.append((line,))

    bytecode = asm(intermediate_representation)
    return bytecode, intermediate_representation
def main():
    test_commands()
    print("\n" + "=" * 50)

    parser = argparse.ArgumentParser(description='Ассемблер УВМ вариант 10')
    parser.add_argument('-i', '--input', required=True, help='Входной файл с программой')
    parser.add_argument('-o', '--output', required=True, help='Выходной бинарный файл')
    parser.add_argument('-t', '--test', choices=['0', '1'], default='0', help='Режим тестирования')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as file:
        text = file.read()

    bytecode, ir = full_asm(text)

    with open(args.output, 'wb') as output_file:
        output_file.write(bytecode)

    print(f"Ассемблировано команд: {len(ir)}")
    print(f"Байткод записан в: {args.output}")

    if args.test == '1':
        print("\nПромежуточное представление:")
        pprint.pprint(ir)
        print("\nБайткод (hex):")
        print(' '.join([hex(i) for i in bytecode]))


if __name__ == "__main__":
    main()