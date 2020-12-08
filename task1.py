import os
from datetime import date, timedelta
from random import randint, choice, triangular
import regex as re
from mysqlConnector import insert_request_in_database

path_to_dir = 'files/'

'''generating a random date for the last 5 years'''


def generate_random_date():
    today_date = date.today()
    years, month, day = str(today_date).split('-')
    years_5_ago = date(int(years) - 5, int(month), int(day))
    number_days = (today_date - years_5_ago).days
    day_random = randint(0, number_days)
    date_random = today_date - timedelta(days=day_random)
    return str(date_random)


def generate_random_sequence_letters(all_letters):
    letters = ''
    for i in range(10):
        letters += choice(all_letters)
    return letters


'''generating 100 files with random data,english and russian letters,decimal and integer digits'''


def generate_100_files(path_to_dir):
    separator = '||'
    english_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    russian_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    if not os.path.exists('files'):
        os.mkdir('files')
    for i in range(1, 101):
        path_file = path_to_dir + str(i) + '.txt'
        with open(path_file, 'a', encoding='utf-8') as file:
            for i in range(100000):
                date_random = generate_random_date()
                english_sequence = generate_random_sequence_letters(english_letters)
                russian_sequence = generate_random_sequence_letters(russian_letters)
                digit_sequence = str(randint(1, 100000001))
                decimal_sequence = str(format(triangular(1, 20), '.6f'))
                row = date_random + separator + english_sequence + separator + russian_sequence + separator + digit_sequence + separator + decimal_sequence + separator + '\n'
                file.write(row)


'''delete from 100 files all rows which contain the data that was entered'''


def delete_rows_with_specified_string(list_files):
    specified_string = input('Enter symbols:')
    numbers_rows_to_delete = 0
    for name in list_files:
        with open(path_to_dir + name, 'r+', encoding='utf-8') as file:
            data = file.readlines()
            for row in data:
                if re.search(specified_string, row):
                    numbers_rows_to_delete += 1
                    del data[data.index(row)]
        with open(path_to_dir + name, 'w+', encoding='utf-8') as file:
            file.writelines(data)
    return numbers_rows_to_delete


'''combine 100 files in 1 file,execution time about 4 minutes'''


def combine_files_in_file(list_files):
    for name in list_files:
        with open(path_to_dir + name, 'r+', encoding='utf-8') as file:
            data = file.readlines()
            with open('all_files.txt', 'a+', encoding='utf-8') as all_files:
                all_files.writelines(data)


''' Enter 100 files in database mysql'''


def enter_data_in_mysql_from_files(path_to_dir):
    list_files = os.listdir(path_to_dir)
    numbers_files = len(list_files)
    processed_files = 0
    for name in list_files:
        request = "LOAD DATA local INFILE '{0}' INTO TABLE random_data FIELDS TERMINATED BY '||';".format(
            path_to_dir + name)
        insert_request_in_database(request)
        processed_files += 1
        numbers_files -= 1
        print('Files processed:', processed_files, '\n'
              + 'Files left:', numbers_files)

def request_sum_int_and_average_median():
    request_sum_digit_sequence = '(select sum(digit_sequence) from random_data);'
    request_median_decimal_sequence = '(select decimal_sequence from(select  row_number() over(order by decimal_sequence ) as number_row,decimal_sequence from random_data   ) as row_table where (select floor(count(*)/2) from random_data) = number_row);'
    sum_digit_sequence = insert_request_in_database(request_sum_digit_sequence)
    median_decimal_sequence = insert_request_in_database(request_median_decimal_sequence)
    print('Result: sum_digit_sequence = ', sum_digit_sequence[0][0], '\n',
          'Result: median_decimal_sequence = ', median_decimal_sequence[0][0])


def main():
    # generate_100_files(path_to_dir)
    while True:
        print(
            '1-delete rows like enter data\n'
            '2-combine files in file(execution time about 4 minutes)\n'
            '3-enter data in mysql from files\n'
            '4-sum all int and average median\n'
            '0-Exit')
        cmd = input("Enter command: ")
        if cmd == "1":
            list_files = os.listdir(path_to_dir)
            numbers_rows_to_delete = delete_rows_with_specified_string(list_files)
            print('Row delete:',numbers_rows_to_delete)
        elif cmd == "2":
            list_files = os.listdir(path_to_dir)
            combine_files_in_file(list_files)
        elif cmd == "3":
            enter_data_in_mysql_from_files(path_to_dir)
        elif cmd == "4":
            request_sum_int_and_average_median()
        elif cmd == "0" or cmd.lower() == "exit":
            break
        else:
            print("Command doesn't exist")
    return


main()
