#usr/bin/python
from time import time, strftime
import argparse
import itertools, string
import hashlib
import sys

info = """
--------------------------------------------------------------------------
|   ___  _   _    __  __ ____  ____   ____                _              |
|  / _ \| | | |  |  \/  |  _ \| ___| / ___|_ __ __ _  ___| | _____ _ __  | 
| | | | | | | |  | |\/| | | | |___ \| |   | '__/ _` |/ __| |/ / _ \ '__| |
| | |_| | |_| |  | |  | | |_| |___) | |___| | | (_| | (__|   <  __/ |    |  
|  \___/ \___/___|_|  |_|____/|____/ \____|_|  \__,_|\___|_|\_\___|_|    |  
|           |_____|                                                      |
|------------------------------------------                              |
| Название        : Python MD5 брутфорсер |                              |
| Автор           : Олег Уланов           |                              |
| Лицензия        : MIT License           |                              |
--------------------------------------------------------------------------
"""
# Брутфорс
def CrackHash(alphabet, hash):
    try:
        # Печать и инициализация времени начала брутфорса
        print("[+] Взлом начат: ", strftime('%H:%M:%S'))
        start_time = time()

        # Всего обработанно слов
        total = 0
        
        # Цикл по длине сообщения
        for n in range(1, 31+1):

            # Время начала перебора слов заданной длины
            length_time = time()
            print("[!] Предполагаемая длина строки:", n)

            # Генерация всевозможных заданной длины
            for xs in itertools.product(alphabet, repeat=n):
                
                # Формирование строки
                cleartext = ''.join(xs)

                # Создание хеша для данной строки
                m = hashlib.md5()
                m.update(bytes(cleartext, encoding='utf-8'))

                # Инкремент числа обработанных слов
                total += 1

                # Сравнение хешей
                if m.hexdigest() == hash:
                    print("[!] Обнаружено совпадение:\t", cleartext)
                    print("[-] Взлом закончен:\t\t", strftime('%H:%M:%S'))
                    print("[-] Всего слов исследовано:\t", total)
                    print("---MD5 взломан за %s секунд---" % (time() - start_time))
                    sys.exit()
            print("[!]",n,"- длина строки обработана за %s секунд" % (time() - length_time))
    except:
        sys.exit()

# Точка входа
if __name__ == "__main__":
    # Парсинг аргументов
    parser = argparse.ArgumentParser(description=info, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-hs', '--hash', required=True, type=str, help='Взламываемый хеш')
    parser.add_argument('-f', '--fast', default=False, type=bool, help='Быстрый режим при установке на True работает только с латиницей и цифрами')
    parser.add_argument('-c', '--cyrillic', default=False, type=bool,help='Доп. использование кириллицы при установке на True')
    parser.add_argument('-cu', '--custom', default=False, type=str,help='Использование кастомного списка символов')
    args = parser.parse_args()

    # Печать информации о ПО в кносоль
    print(info)

    # Печать данных о хеше 
    print("Исследуемый хеш: " + args.hash)

    # Формирование словаря для утилиты
    if ((args.custom!=False)):
        alphabet = args.custom
    else:
        if (args.fast!=False):
            alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' 
        else:
            alphabet = string.printable.replace(' \t\n\r\x0b\x0c', '')
        
        if (args.cyrillic!=False):
            alphabet=alphabet+'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    
    # Печать дополнительных данных об алфавите
    print("Алфавит:\t " + alphabet)
    print("Мощность:\t " + str(len(alphabet)) + "\n")

    # Переход к атаке грубой силы
    CrackHash(alphabet, args.hash)