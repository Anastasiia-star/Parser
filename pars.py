import re
import numpy as np

try:
    with open('test_schedule.inc',"r",encoding = 'utf-8') as file:
        test_file = file.read()
except FileNotFoundError:
    print('Файл не найден')
    

def clean_schedule(file):
    del_comment = list(map((lambda x: re.sub(r'--[\w\s,()]+','',x)),file.split('\n')))
    return '\n'.join(list(filter(lambda x: x, del_comment)))

wihout_comment = clean_schedule(test_file)

def parse_schedule(text, keywords_tuple=("DATES", "COMPDAT", "COMPDATL")):
    out_list = []
    all_tags_continue = list(set(re.findall(r'\n/\n(\w+)',text))-set(keywords_tuple))
    text_list = text.split('\n')
    date = np.nan
    cur_str = ""
    cur_list = []
    
    for rec in text_list:
        if rec in all_tags_continue or rec.strip()=='/': cur_str = ""
        if cur_str == "DATES" and rec not in keywords_tuple:
            date = parse_keyword_DATE_line(rec)
            if len(cur_list)==1:
                cur_list.append(np.nan)
                out_list.append(cur_list)
                cur_list = []
            cur_list.append(date)
        if (cur_str == "COMPDAT" or cur_str == "COMPDATL") and rec not in keywords_tuple:
            if cur_list==[]: cur_list.append(date)
            unpack = default_params_unpacking_in_line(rec)
            if cur_str == "COMPDAT":
                cur_list = cur_list+parse_keyword_COMPDAT_line(unpack)
            else:
                cur_list = cur_list+parse_keyword_COMPDATL_line(unpack)
            out_list.append(cur_list)
            cur_list = []
            
        if rec=="END" and len(cur_list)==1:
            cur_list.append(np.nan)
            out_list.append(cur_list)
        if rec in keywords_tuple:
            cur_str = rec
    return print(out_list)


def parse_keyword_DATE_line(current_date_line):
    return re.findall(r'\d\d\s[A-Z]{3}\s\d{4}',current_date_line)[0]

def default_params_unpacking_in_line(current_date_line):
    pattern = re.compile(r'(\w+)\*')
    pattern_replace = re.findall(r'\w+\*',current_date_line)
    output_line = ['DEFAULT '*int(x) for x in pattern.findall(current_date_line)]
    output = [x.strip() for x in output_line]
    for num in range(len(output)):
        current_date_line = current_date_line.replace(pattern_replace[num],output[num])
    return current_date_line

def parse_keyword_COMPDAT_line(well_comp_line):
    well_comp_line=re.sub(r"'|(\s+/$)","",well_comp_line)
    well_comp_line=re.sub(r"\s*/\s*","",well_comp_line)
    well_comp_line=re.split(r"\s+",well_comp_line)
    well_comp_line.insert(1,np.nan)
    return well_comp_line

def parse_keyword_COMPDATL_line(well_comp_line):
    well_comp_line=re.sub(r"'|(\s+/$)","",well_comp_line)
    well_comp_line=re.sub(r"\s*/\s*","",well_comp_line)
    well_comp_line=re.split(r"\s+",well_comp_line)
    return well_comp_line

parse_schedule(wihout_comment)