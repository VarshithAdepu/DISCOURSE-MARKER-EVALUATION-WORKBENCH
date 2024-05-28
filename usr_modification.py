import re
from wxconv import WXC

relations = [
    'समुच्चय', 'अन्यत्र', 'समानकाल', 'विरोधि', 'व्याभिचार', 'कार्य-कारण',
    'वाक्य-कर्म', 'आवश्यकता-परिणाम', 'विरोधी.विपरीत', 'विरोधी_द्योतक',
    'समुच्चय.समावेशी', 'समुच्चय.Inclusive', 'वाक्य-कर्म', 'विरोधि.viparIwa',
    'परिणाम', 'विरोधि_द्योतक', 'समुच्चय.BI_1', 'समुच्चय.x', 'समुच्चय दोतक',
    'इसके परिणाम स्वरुप'
]

def convert_to_usr2(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        lines = content.split("\n")
        result = []
        temp = []
        for line in lines:
            if line.startswith('<sent_id='):
                if temp:
                    result.append(temp)
                temp = [line]
            else:
                temp.append(line)
        if temp:
            result.append(temp)
        return process_result(result)

def process_result(result):
    with open('annotated_text_after_modification.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            id1 = lines[i].split(' ')
            id2, id_word = find_words_in_list(id1)
            # s1=lines[i].replace('>',' ').replace('<',' ')
            # s1=s1.split('  ')
            
            # l1=get_id_from_annotated(lines[i].split())

            for j in range(len(result)):
                l = result[j][7]
                id0=get_id1(result[j][0])
                n = get_id1(l)  
                l = l.split(',')
                if len(id_word) != 0 and n == get_id1(id2):
                    new_res = ''
                    l = ''.join(l)
                    new_res += get_id1(id2) + '.' + extract_digit(l) + ':' + convert_to_eng(id_word[0]) + ' '
                    if get_relation(l) != convert_to_eng(id_word[0]):
                        result[j][7] = result[j][7].replace(l, new_res)
                        # print(('').join(result[j][7]))
                # print(get_id1(result[j][0]),get_id1(result[j+1][0]))
                # if len(l1)>=2 and (l1[1]==get_id1(result[j][0])):
                    # print(lines[i].split('> '))
                    # print(s1[1])
                    # print('sss',l1[1])
                    # print(get_id1(result[j][0]),get_id1(result[j+1][0]))

                # elif len(l1)==1 and (l1[0]==get_id1(result[j][0])):
                #     print(s1[1])

            

        with open('usr_after_modification', 'w', encoding='utf-8') as file:
            for i in range(len(result)):
                for row_number in range(len(result[i])):
                    output_string = ""
                    if row_number == 0:
                        output_string = result[i][row_number]
                    else:
                        for element in result[i][row_number]:
                            if element == None:
                                element = ""
                            output_string += element
                    file.write(output_string + '\n')


def find_words_in_list(given_list):
    found_words = [word for word in given_list if word in relations]
    return given_list[0], found_words

def extract_digit(input_string):
    match = re.search(r'\.(\d+):', input_string)
    if match:
        return match.group(1)
    return None

def get_id1(sent):
    match1 = re.findall(r'(\w+_\w+_\w+_\w+-\w+_\d+[a-zA-Z]?)', sent)
    if match1:
        return match1[0]
    return None

def get_relation(sent):
    pattern = re.compile(r':(\w+-?\w+)', re.IGNORECASE)
    match = re.search(pattern, sent)
    if match:
        return match.group(1)
    return None

def convert_to_eng(input_text):
    wx = WXC(order='utf2wx', lang='hin')
    hindi_text = wx.convert(input_text)
    return hindi_text

if __name__ == "__main__":
    file_path = 'upload_file'
    convert_to_usr2(file_path)
