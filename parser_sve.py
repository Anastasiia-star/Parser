import re

try:
    with open('test_schedule.inc',"r",encoding = 'utf-8') as file:
        test_file = file.read()
except FileNotFoundError:
    print('Файл не найден')
    
print(test_file)
print("=======================")

def clean_schedule(file):
    del_comment = list(map((lambda x: re.sub(r'--[\w\s,()]+','',x)),file.split('\n')))
    return '\n'.join(list(filter(lambda x: x, del_comment)))

wihout_comment = clean_schedule(test_file)

def parse_keyword_DATE_line(current_date_line):
    print(re.findall(r'\d\d\s[A-Z]{3}\s\d{4}',current_date_line))
    
parse_keyword_DATE_line(wihout_comment)