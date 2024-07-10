from flask import Flask, render_template, request, redirect, url_for, jsonify
import subprocess
import re
from wxconv import WXC
import os
app = Flask(__name__, template_folder='templates', static_url_path='/static')


discourse_relation = {
                   "Ora" : "samuccaya",
                #    "ki" : "pariNAma",
                   "evaM" : "samuccaya",
                   "waWA" : "samuccaya",
                #    "agara" : "AvaSyakawA-pariNAma",
                #    "yaxi" : "AvaSyakawA-pariNAma",
                   "wo" : "AvaSyakawA-pariNAma",
                   "nahIM wo": "AvaSyakawA-pariNAma",
                   "kyoMki" : "kArya-kAraNa",
                   'cUzki'  :"kArya-kAraNa",
                   'cUMki'  :"kArya-kAraNa",
                   "isIlie" : "pariNAma",
                   "isalie" : "pariNAma",
                   "jabaki" : "viroXI_xyowaka",
                   "yaxyapi" : "vyABicAra",
                   "waWApi" : "vyABicAra",
                   "hAlAzki" : "vyABicAra",
                   "Pira BI" : "vyABicAra",
                   "lekina" : "viroXI",
                   "kiMwu" : "viroXI",
                   "paraMwu" : "viroXI",
                   "jaba" : "samAnakAla",
                   "waba": "samAnakAla",
                   "yA": "anyawra",
                   "aWavA": "anyawra",
                   'isake pariNAmasvarUpa' : "pariNAma",
                   'isI kAraNa': 'pariNAma',
                   'isake viparIwa' : "viroXI",
                   "viparIwa" : 'viroXI',
                   "isake alAvA" : 'samuccaya x' ,
                   'isake awirikwa' : 'samuccaya x',
                   'isake sAWa-sAWa' : 'samuccaya x',
                   'isake sAWa sAWa' : 'samuccaya x',
                   'isa kAraNa' : 'pariNAma',
                   'isake kAraNa':'kArya-kAraNa',
                   'isake bAvajZUxa' : 'vavicAra',
                   'nA kevala': 'samuccaya'
                   
           }

markers = {'और', 'एवं', 'तथा', 'अगर','चूँकि' , 'चूंकि', 'तो', 'क्योंकि', 'इसीलिए','इसलिए', 'जबकि', 'यद्यपि', 'तथापि', 
           'फिर भी', 'लेकिन', 'किंतु', 'परंतु', 'जब', 'तब', 'या', 'अथवा', 'विपरीत'}

multi_word_markers = {'नहीं तो', 'इसके परिणामस्वरूप', 'इसके विपरीत', 'इसके अलावा', 'इसके अतिरिक्त', 'इसके साथ-साथ', 
                      'इसके साथ साथ', 'इस कारण', 'इसके बावज़ूद'}

@app.route('/save_duplicate_file', methods=['POST'])
def save_duplicate_file():
    file = request.files['fileInput']
    filename = 'upload_file'
    file.save(os.path.join(app.root_path, filename))
    return "Duplicate file saved successfully"

def convert_to_eng(input_text):
    if not isinstance(input_text, str):
        input_text = str(input_text)
    wx = WXC(order='utf2wx', lang='hin')
    hindi_text = wx.convert(input_text)
    return hindi_text
def remove_word(sentence):
    """
    Get discourse relation from the first word
    - sentence : list of first 5 words in the wx converted sentence
    """
    sentence = sentence.split()
    sent = sentence[0]
    if sent in markers or sent in multi_word_markers:
        sentence = ' '.join(sentence[1:])
        if 'अगर' in sentence or 'यदि' in sentence:
            sentence = sentence.replace('अगर', '').replace('यदि', '')
            return sentence
        return sentence
    
    sentence = ' '.join(sentence)
    return sentence

def convert_to_usr1(file_contents):
    lines = file_contents.split("\n")
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
    
    return f2(result)

def convert_to_hindi1(input_text):
    if not isinstance(input_text, str):
        input_text = str(input_text)
    wx = WXC(order='wx2utf', lang='hin')
    hindi_text = wx.convert(input_text)
    return hindi_text

def f2(result):
    output_lines = []
    for i in range(len(result)-1):
        
        id_1 = result[i][0]
        id_2=result[i+1][0]
        k1=get_id2(id_1)
        k2=get_id2(id_2)
        sentence_without_hash = result[i][1][1:]  # Hindi sentence without hash
        sentence_without_hash = remove_word(sentence_without_hash)
        sentence_without_hash1 = result[i+1][1][1:]  # Hindi sentence without hash
        sentence_without_hash1 = remove_word(sentence_without_hash1)
        # print(sentence_without_hash1[:2])
        s = []
        l = result[i][7]
        n = get_id1(l)  # example 1a ,1b
        l = l.split()
        # print(l)
        ki1=result[i][1][1:].split()

        if n and len(l) >= 2:
            
            rel1 = get_relation(l[0])
            n1 = get_id1(l[0])
            n2 = get_id1(l[1])
            rel2 = get_relation(l[1])
            rel1 = convert_to_hindi1(rel1)
            rel2 = convert_to_hindi1(rel2)
            for j in range(len(result)):
                id_2 = result[j][0]
                
                org_id2 = get_id1(id_2)
                if n1 and n1 == org_id2:
                    k2=get_id1(id_2)
                    sentence_without_hash1 = result[j][1][1:]
                    sentence_without_hash1 = remove_word(sentence_without_hash1)
                    s.append('<<'+'o'+'>sent_id='+k2+'>' + " " + sentence_without_hash1 + ' <<'+'o'+'>/sent_id> ' + rel1 + " ")
            if i==len(result)-2:
                k1=get_id1(id_1)
                sentence_without_hash1=result[i+1][1][1:]
                sentence_without_hash1=remove_word(sentence_without_hash1)
                s.append('<<'+'o'+'>sent_id='+k1+'>' + " " + sentence_without_hash + ' <<'+'o'+'>/sent_id> ')
                output_lines.extend(s)

            for j in range(len(result)):
                id_2 = result[j][0]
                
                org_id2 = get_id1(id_2)
                if n2 and n2 == org_id2:
                    k1=get_id1(id_1)
                    k2=get_id1(id_2)
                    sentence_without_hash1 = result[j][1][1:]
                    sentence_without_hash1 = remove_word(sentence_without_hash1)
                    s.append('<<'+'o'+'>sent_id='+k2+'>' + " " + sentence_without_hash1 + ' <<'+'o'+'>/sent_id> ' + rel2 + " " + '<<'+'o'+'>sent_id='+k1+'>' + " " + sentence_without_hash + ' <<'+'o'+'>/sent_id> ')
                    
                    output_lines.extend(s)

            
        elif n:
            rel = get_relation(l[0])
            rel = convert_to_hindi1(rel)
            for j in range(len(result)):
                id_2 = result[j][0]
                
                org_id2 = get_id1(id_2)
                if n and n == org_id2:
                    k1=get_id1(id_1)
                    k2=get_id1(id_2)
                    sentence_without_hash1 = result[j][1][1:]
                    sentence_without_hash1 = remove_word(sentence_without_hash1)
                
                    s.append('<<'+'o'+'>sent_id='+k2+'>' + " " + sentence_without_hash1 +  ' <<'+'o'+'>/sent_id> '  + rel + " " + '<<'+'o'+'>sent_id='+k1+'>' + " " + sentence_without_hash + ' <<'+'o'+'>/sent_id> ')
                    output_lines.extend(s)
                    if len(output_lines)>=2:
                        v1=output_lines[-1].split()
                        v2=output_lines[-2].split()
                        # print(v1[0],v2[0])
                        if v1[0]==v2[0]:
                            output_lines[-2] = output_lines[-2].strip() + " " + output_lines[-1].replace('<<'+'o'+'>sent_id='+k2+'>' + " " + sentence_without_hash1 + ' <<'+'o'+'>/sent_id> ','')
                            del output_lines[-1]

            if len(output_lines)>=2:
                v1=output_lines[-1].split()
                v2=output_lines[-2].split()
                # print(v1[0],v2[0])
                if v1[0]==v2[0]:
                    output_lines[-2] = output_lines[-2].strip() + " " + output_lines[-1].replace('<<'+'o'+'>sent_id='+k2+'>' + " " + sentence_without_hash1 + ' <<'+'o'+'>/sent_id> ','')
                    del output_lines[-1]
                elif v1[0] in v2:
                    output_lines[-2] = output_lines[-2].strip() + " " + output_lines[-1].replace('<<'+'o'+'>sent_id='+k2+'>' + " " + sentence_without_hash1 + ' <<'+'o'+'>/sent_id> ','')
                    del output_lines[-1]
                    # print(output_lines[-1])
                elif v2[0] in v1:
                    output_lines[-2] = output_lines[-2].strip() + " " + output_lines[-1].replace('<<'+'o'+'>sent_id='+k2+'>' + " " + sentence_without_hash1 + ' <<'+'o'+'>/sent_id> ','')
                    del output_lines[-1]
            del_duplic(output_lines)
                

            if i==len(result)-2:
                k1=get_id1(id_2)
                sentence_without_hash1=result[i+1][1][1:]
                print(sentence_without_hash1)
                sentence_without_hash1=remove_word(sentence_without_hash1)
                s.append('<<'+'o'+'>sent_id='+k1+'>' + " " + sentence_without_hash + ' <<'+'o'+'>/sent_id> ')
                output_lines.extend(s)
                
            

        elif i==0 and k1!=k2:
            k1=get_id1(id_1)
            sentence_without_hash1=result[i][1][1:]
            sentence_without_hash1=remove_word(sentence_without_hash1)
            s.append('<<'+'o'+'>sent_id='+k1+'>' + " " + sentence_without_hash + ' <<'+'o'+'>/sent_id> ')
            output_lines.extend(s)
            
            
        else:
            
            if i==len(result)-2:
                id_1 = result[i][0]
                print(id_1)
                id_2=result[i+1][0]
                k1=get_id2(id_1)
                k2=get_id2(id_2)
                sentence_without_hash = result[i][1][1:]  # Hindi sentence without hash
                sentence_without_hash = remove_word(sentence_without_hash)
                sentence_without_hash1 = result[i+1][1][1:]  # Hindi sentence without hash
                sentence_without_hash1 = remove_word(sentence_without_hash1)
                # print(sentence_without_hash1,'aaaa')
                s = []
                l = result[i+1][7]
                n = get_id1(l)  # example 1a ,1b
                l = l.split()
                # print(l)
                rel = get_relation(l[0])
                rel = convert_to_hindi1(rel)
                for j in range(len(result)):
                    id_2 = result[j][0]
                    org_id2 = get_id1(id_2)
                    if n and n == org_id2:
                        # print(id_2)
                        k1=get_id1(id_1)
                        k2=get_id1(id_2)
                        # sentence_without_hash1 = result[j][1][1:]
                        # sentence_without_hash1 = remove_word(sentence_without_hash1)
                    
                        s.append('<<'+'o'+'>sent_id='+k1+'>' + " " + sentence_without_hash + ' <<'+'o'+'>/sent_id> ' + rel + " " + '<<'+'o'+'>sent_id='+k2+'>' + " " + sentence_without_hash1 + ' <<'+'o'+'>/sent_id> ')
                        output_lines.extend(s)
            
            elif i!=0:
                id_0=result[i-1][0]
                # id_2=result[i+1][0]
                k0=get_id2(id_0)
                if k1!=k2 and k0!=k1:
                    k1=get_id1(id_1)
                    sentence_without_hash1=result[i][1][1:]
                    sentence_without_hash1=remove_word(sentence_without_hash1)
                    s.append('<<'+'o'+'>sent_id='+k1+'>' + " " + sentence_without_hash + ' <<'+'o'+'>/sent_id> ')
                    output_lines.extend(s)
                    
                elif k0==k1 or k1==k2:
                    k1=get_id1(id_1)
                    # print(k1)
                    k2=get_id1(id_2)
                    sentence_without_hash1 = result[i][1][1:]
                    sentence_without_hash1 = remove_word(sentence_without_hash1)
                    s.append('<<'+'o'+'>sent_id='+k1+'>' + " " + sentence_without_hash1 + ' <<'+'o'+'>/sent_id> ')
                    output_lines.extend(s)
                    del_duplic(output_lines)
                    

            else:
                k1=get_id1(id_1)
                sentence_without_hash1=result[i][1][1:]
                print(sentence_without_hash1)
                sentence_without_hash1=remove_word(sentence_without_hash1)
                s.append('<<'+'o'+'>sent_id='+k1+'>' + " " + sentence_without_hash1 + ' <<'+'o'+'>/sent_id> ')
                output_lines.extend(s)
                k2=get_id1(id_2)
                sentence_without_hash1=result[i+1][1][1:]
                print(sentence_without_hash1)
                sentence_without_hash1=remove_word(sentence_without_hash1)
                s.append('<<'+'o'+'>sent_id='+k2+'>' + " " + sentence_without_hash1 + ' <<'+'o'+'>/sent_id> ')
                output_lines.extend(s)
    
    return '\n'.join(output_lines)

def del_duplic(output_lines):
    if len(output_lines)>=2:
        v1=output_lines[-1].split()
        v2=output_lines[-2].split()
        # print(v1[0],v2[0])
        if v1[0]==v2[0]:
            # output_lines[-2] = output_lines[-2].strip() + " " + output_lines[-1].replace('<sent_id='+k2+'>' + " " + sentence_without_hash1 + ' </sent_id> ','')
            del output_lines[-1]
        elif v1[0] in v2:
            # output_lines[-2] = output_lines[-2].strip() + " " + output_lines[-1].replace('<sent_id='+k2+'>' + " " + sentence_without_hash1 + ' </sent_id> ','')
            del output_lines[-1]
            # print(output_lines[-1])
        elif v2[0] in v1:
            # output_lines[-2] = output_lines[-2].strip() + " " + output_lines[-1].replace('<sent_id='+k2+'>' + " " + sentence_without_hash1 + ' </sent_id> ','')
            del output_lines[-1]
    return output_lines 

def get_id2(sent):
    match1 = re.findall(r'(\w+_\w+_\w+_\w+-\w+_\d+)', sent)
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

# Hardcoded valid usernames and passwords (for demonstration purposes only)
valid_users = {
    "1": "1",
    "user2": "password2"
}
def convert_to_usr(contents):
    # print("Entred usr function with content : ", contents)
    lines = contents.split("\n")
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
    
    return f1(result)

def f1(result):

    # print("Inside the f1 function")
    s = []
    for i in range(len(result)):
        org_id1 = get_id(result[i][0])
        sentence_without_hash = result[i][1][1:]  # Hindi sentence without hash
        s.append(org_id1 + " " + sentence_without_hash)

    # Join the formatted sentences
    return '\n'.join(s)

# def extract_id(text):
#     match = re.search(r'(?<=<sent_id=)(.*?)(?=>)', text)
#     return match.group(0) if match else "ID not found."

def get_id(sent):
    match1 = re.search(r'(\w+_\w+_\w+_\w+-\w+_\d+[a-zA-Z]?)', sent)
    if match1:
        return match1.group() 
    else:
        return None
    
def get_id1(sent):
    match1 = re.search(r'(\w+_\w+_\w+_\w+-\w+_\d+[a-zA-Z]?)', sent)
    if match1:
        return match1.group() 
    else:
        return None
# Function to check if a user is valid
def is_valid_user(username):
    return username in valid_users

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    if username in valid_users and valid_users[username] == password:
        # Authentication successful
        return 'authenticated'
    else:
        # Authentication failed
        return 'unauthenticated'


@app.route('/')
def index():
    username = request.args.get('username')
    return render_template('index.html', username=username)

@app.route('/process_input_1', methods=['POST'])
def process_input_1():
    uploaded_file = request.files['fileInput']
    
    # Check if a file was uploaded
    if uploaded_file.filename != '':
        try:
            # Read the contents of the uploaded file
            file_contents = uploaded_file.read().decode('utf-8')
            
            # Transform the file contents using the provided code
            transformed_contents = convert_to_usr(file_contents)
            return transformed_contents
        except Exception as e:
            return str(e), 500
    else:
        return 'No file uploaded', 400

@app.route('/process_input_2', methods=['POST'])
def process_input_2():
    uploaded_file = request.files['fileInput']
    
    # Check if a file was uploaded
    if uploaded_file.filename != '':
        try:
            # Read the contents of the uploaded file
            file_contents = uploaded_file.read().decode('utf-8')
            
            # Transform the file contents using the provided code
            transformed_contents = convert_to_usr1(file_contents)
            with open('annotated_text.txt', 'w') as f:
                f.write(transformed_contents.replace('<o>',''))
            return transformed_contents
        except Exception as e:
            return str(e), 500
    else:
        return 'No file uploaded', 400
    
@app.route('/save_to_file', methods=['POST'])
def save_to_file():
    data = request.json
    modified_text = data.get('text', '')

    with open('annotated_text_after_modification.txt', 'w') as file:
        file.write(modified_text)

    subprocess.run(['python3', 'usr_modification.py'])

    return jsonify({'message': 'Text saved successfully'})

if __name__ == '__main__':
    app.run(debug=True)
