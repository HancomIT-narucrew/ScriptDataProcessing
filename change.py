import re

def modifyScripts():

    r = open('crawling.txt', 'r+', encoding='UTF-8')    # 원본 파일 읽어오기
    w = open(file_name+'_raw.txt', 'a+', encoding='UTF-8')    # 전처리 된 raw 파일 생성

    rm_pattern = [
        '\([A-Z].*\)\s',  # [문장] 제거
        '\[[A-Z].*\]\s',  # (문장) 제거
        '^♪\s[A-Z].*',  # '♪' 문장 제거
        '\-\s',  # '- ' 제거
        '\#',  # '#' 제거
        '"',  # " 제거
        "^(')",  # '문장' '의 제거
        "\s(')$",
        '[A-Z].*\:\s',  # '이름:' 제거
        'OpenSubtitles recommends using Nord VPN',
        'from 3.49 USD/month ----> osdb.link/vpn',
        '^\s'  # 공백제거 (제일 나중에 해야함)
    ]

    change_pattern=[ # -삭제
        'e-mail',
        'T-shirt',
        'ex-', # ex-girlfriend, ex-boyfriend
        'co-',
        '-er',
        'non-'
        're-'
    ]

    lines = r.readlines()  # 전체 스크립트
    lines = list(map(lambda s: s.strip(), lines))  # 전체 스크립트에서 개행문자 삭제
    count = 0  # index
    file_list = list()  # 한 줄씩 입력하기 위해 생성한 빈 리스트

    for line in lines:

        for i in rm_pattern:
            line = re.sub(pattern=i, repl='', string=line)

        for j in change_pattern:
            line = re.sub(pattern=j, repl=re.sub(pattern='-', repl='', string=j), string=line)

        if line.isupper() == True:  # 문장 전체 대문자 제거
            line = line.replace(line, '')

        if '!' in line:  # '!' -> '.'
            line = line.replace('!', '.')

        if '&' in line:  # '&' -> 'and'
            line = line.replace('&', 'and')

        if 'um...' in line:  # 'um...' -> 'um.'
            line = line.replace('um...', 'um.')

        if 'Um...' in line:  # 'Um...' -> 'Um.'
            line = line.replace('Um...', 'Um.')

        if 'so...' in line:  # 'so...' -> 'so.'
            line = line.replace('so...', 'so.')

        if 'uh...' in line:  # 'uh...' -> 'uh.'
            line = line.replace('uh...', 'uh.')

        if 'a.m.' in line:  # 'a.m.' -> 'am'
            line = line.replace('a.m.', 'am')

        if 'p.m.' in line:  # 'p.m.' -> 'pm'
            line = line.replace('p.m.', 'pm')

        if '-in-law' in line:  # '-in-law' -> ' in law'
            line = line.replace('-in-law', ' in law')

        # ...을 지우기 위해 문장정렬
        if line != "":
            if count == 0:
                file_list.insert(count, line)
                count += 1
            else:
                if line[0].isupper() == True:
                    file_list.insert(count, line)
                    count += 1
                else:
                    file_list[count - 1] = file_list[count - 1] + ' ' + line

    for i in file_list:  # ... 문장 삭제
        if re.search('.*\.\.\..*',i) == None:
            w.write(i + '\n')

    r.truncate(0)

    r.close()
    w.close()

def attachTag(file_name) :
    r = open(file_name+'_raw.txt', 'r+', encoding='UTF-8')  # raw 파일 읽어오기
    w = open(file_name+'_tag.txt', 'a+', encoding='UTF-8')  # tag가 부착된 tag 파일 생성

    while True:
        line = r.readline()
        if not line: break

        line = re.sub(pattern='\s', repl='\tO\n', string=line)
        line = re.sub(pattern='^	O', repl='', string=line)
        line = re.sub(pattern='\,\tO', repl='\tCOMMA', string=line)
        line = re.sub(pattern='\.\tO', repl='\tPERIOD', string=line)
        line = re.sub(pattern='\?\tO', repl="\tQUESTION", string=line)
        line = re.sub(pattern="'s\tO", repl="\tO\n's\tO", string=line)
        line = re.sub(pattern="'re\tO", repl="\tO\n're\tO", string=line)
        line = re.sub(pattern="'m\tO", repl="\tO\n'm\tO", string=line)
        line = re.sub(pattern="'m\tO", repl="\tO\n'm\tO", string=line)
        line = re.sub(pattern="'ll\tO", repl="\tO\n'll\tO", string=line)
        line = re.sub(pattern="n't\tO", repl="\tO\nn't\tO", string=line)

        w.write(line)


    r.close()
    w.close()