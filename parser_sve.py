try:
    with open('test_schedule.inc',"r",encoding = 'utf-8') as file:
        test_file = file.read()
except FileNotFoundError:
    print('Файл не найден')
    
print(test_file)