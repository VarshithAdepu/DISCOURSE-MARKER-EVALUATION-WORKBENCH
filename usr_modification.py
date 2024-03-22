import re
from wxconv import WXC
relations=['समुच्चय', 'अन्यत्र', 'समानकाल', 'विरोधि', 'व्याभिचार', 'कार्य-कारण', 
        'वाक्य-कर्म', 'आवश्यकता-परिणाम', 'विरोधी.विपरीत', 'विरोधी_द्योतक',
        'समुच्चय.समावेशी', 'समुच्चय.Inclusive', 'वाक्य-कर्म', 'विरोधि.viparIwa', 
        'परिणाम', 'विरोधि_द्योतक', 'समुच्चय.BI_1', 'समुच्चय.x', 'समुच्चय दोतक', 
        'इसके परिणाम स्वरुप']

    
def convert_to_usr2(file_path):
    """
    Opens the file content (USR) & converts it
    from a single string to a list of rows
    
    Args:
        file_path: Path to input USR file
        output_path: Path to output file
    """
    with open(file_path, 'r') as file:
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
        # print("aa",result)
        return f3(result)
    
def find_words_in_list(given_list):
    found_words = []
    found_words = [word for word in given_list if word in relations]
    return given_list[0],found_words

def extract_digit(input_string):
    match = re.search(r'\.(\d+):', input_string)
    if match:
        return match.group(1)
    return None


def f3(result):
    # print(result)
    with open('annotated_text1.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        for i in range(len(lines)):
            id1=lines[i].split(' ')
            id2,id_word=find_words_in_list(id1)
            # print(id_word)
            
            # if len(id_word)!=0:
            #     id_word = [item for sublist in id_word for item in sublist]
                # print(f'{get_id1(id_word[0])}:{id_word[1]} ')

            for j in range(len(result)):
                l = result[j][7]
                n = get_id1(l)  # example 1a ,1b
                l = l.split(',')
                # print(l[-1],n,extract_digit(l[-1]))
                if len(id_word)!=0 and n==get_id1(id2):
                    new_res=''
                   
                    l=''.join(l)
                
                    new_res+= get_id1(id2) + '.' + extract_digit(l)+':'+ convert_to_eng(id_word[0]) +' '
                    
                    if get_relation(l)!=convert_to_eng(id_word[0]):
                        # print(get_relation(l),l)
                        # print(convert_to_eng(id_word[1]))
                
                        result[j][7]=result[j][7].replace(l,new_res)
                        print(('').join(result[j][7]))

        with open('duplicate_uploaded_file', 'w') as file:
            for i in range(len(result)):
                for row_number in range(len(result[i])):
                    output_string = ""
                    if(row_number == 0):
                        output_string = result[i][row_number]
                    else:
                        for element in result[i][row_number]:
                            if element == None:
                                element = ""
                            output_string += element
                        # output_string = output_string[:-1]
                    file.write(output_string + '\n')
            file.close()

    
    
def convert_to_eng(input_text):
    if not isinstance(input_text, str):
        input_text = str(input_text)
    wx = WXC(order='utf2wx', lang='hin')
    hindi_text = wx.convert(input_text)
    return hindi_text


# def save_usr_to_txt(result):
#        """
#            it converts the updated USR from list to string
#            and writes it in a .txt file
          
#            - usr : previous USR (list) object \n
#            - filename : name of the file \n
#            - sub\\_folder\\_path : path where the file was stored in root structure \n
#        """
#        with open('duplicate_discourse_evaluation_usr_file', 'w') as file:
#         for i in range(len(result)):
#             for row_number in range(len(result[i])):
#                 output_string = ""
#                 if(row_number == 0):
#                     output_string = result[i][row_number]
#                 else:
#                     for element in result[i][row_number]:
#                         if element == None:
#                             element = ""
#                         output_string += element
#                     # output_string = output_string[:-1]
#                 file.write(output_string + '\n')
#         file.close()
        
                        
def get_id1(sent):
    match1 = re.findall(r'(\w+_\w+_\w+_\w+-\w+_\d+[a-zA-Z]?)', sent)
    if match1:
        return match1[0]
    else:
        return None

             
def get_relation(sent):
    if sent:
        pattern = re.compile(r':(\w+-?\w+)', re.IGNORECASE)
        match = re.search(pattern, sent)

        if match:
            return match.group(1)
        else:
            return None
    else:
        return None


if __name__ == "__main__":
    
    file_path = 'uploaded_file'
    convert_to_usr2(file_path)
    

