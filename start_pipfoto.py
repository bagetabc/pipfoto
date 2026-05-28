import sys
import struct
import os
from PIL import Image

def encode(input_img, output_name):
    print(f"Кодирование: {input_img} -> {output_name}")
    try:
        img = Image.open(input_img).convert('RGB').resize((80, 40))
        w, h = img.size
        with open(output_name, 'wb') as f:
            f.write(b'PIP_FOTO')
            f.write(struct.pack('II', w, h))
            for y in range(h):
                for x in range(w):
                    f.write(bytes(img.getpixel((x, y))))
        print("Файл успешно создан!")
    except Exception as e:
        print(f"ОШИБКА КОДИРОВАНИЯ: {e}")

def decode(file_path):
    print(f"Попытка чтения файла: {file_path}")
    if not os.path.exists(file_path):
        print(f"КРИТИЧЕСКАЯ ОШИБКА: Файл не найден по пути: {file_path}")
        return
    
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
            if header != b'PIP_FOTO':
                print("Ошибка: файл не имеет формата .pipfoto")
                return
            
            w, h = struct.unpack('II', f.read(8))
            
            for y in range(h):
                line = ""
                for x in range(w):
                    r, g, b = struct.unpack('BBB', f.read(3))
                    # ANSI escape sequence для вывода цвета
                    line += f"\033[48;2;{r};{g};{b}m  "
                print(line + "\033[0m")
    except Exception as e:
        print(f"ОШИБКА ЧТЕНИЯ: {e}")

if __name__ == "__main__":
    # Если аргументов 2 (скрипт + путь к файлу), считаем, что это декодирование
    if len(sys.argv) == 2:
        decode(sys.argv[1])
    # Если аргументов 4 (скрипт + encode + вход + выход), кодируем
    elif len(sys.argv) == 4 and sys.argv[1] == "encode":
        encode(sys.argv[2], sys.argv[3])
    # Если аргументов 3 (скрипт + decode + путь), декодируем
    elif len(sys.argv) == 3 and sys.argv[1] == "decode":
        decode(sys.argv[2])
    else:
        print("Использование:")
        print("  Кодировать: python pipfoto_tool.py encode <вход.jpg> <выход.pipfoto>")
        print("  Декодировать: python pipfoto_tool.py decode <файл.pipfoto>")