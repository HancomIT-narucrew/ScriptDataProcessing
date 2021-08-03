import re

def modifyScripts(file_name):

    r = open('crawling.txt', 'r+', encoding='UTF-8')    # 원본 파일 읽어오기
    w = open('./raw_file/'+ file_name+'_raw.txt', 'a+', encoding='UTF-8')    # 전처리 된 raw 파일 생성

    rm_pattern = [
        '\([A-Z].*\)',  # [문장] 제거
        '\[[A-Z].*\]',  # (문장) 제거
        '.*\♪.*',  # '♪' 문장 제거
        '.*\#.*',  # '#' 제거
        '"',  # " 제거
        "^(')",  # '문장' '의 제거
        "\s(')$",
        '[A-Z].*\:\s',  # '이름:' 제거
        'OpenSubtitles recommends using Nord VPN',
        'from 3.49 USD/month ----> osdb.link/vpn',
        '.*\-.*',   # '-' 문장 제거
        '.*\w+\.\w+\.+.*',   # 문자.문자.로 된 문장 제거 ex)L.A.
        '\s$',   #뒤에 공백이 있을 때
        '.*\:.*',    # ':'문장제거
        '.*\;.*',    # ';'문장제거
        '.*\=.*',    # '=' 문장제거
        
        '^\s'  # 공백제거 (제일 나중에 해야함)
    ]

    change_pattern=[ # -삭제
        'e-mail',
        'T-shirt',
        'ex-',  # ex-girlfriend, ex-boyfriend
        'co-',
        '-er',
        'non-',
        're-'
    ]

    dot_pattern=[   #...을 .으로 바꾸는 패턴
        'um...', 'Um...',
        'so...', 'So...',
        'uh...', 'Uh...',
        'oh...', 'Oh...'
    ]

    lines = r.readlines()  # 전체 스크립트
    lines = list(map(lambda s: s.strip(), lines))  # 전체 스크립트에서 개행문자 삭제
    count = 0  # index, 라인 수
    file_list = list()  # 한 줄씩 입력하기 위해 생성한 빈 리스트

    for line in lines:

        for j in change_pattern:
            line = re.sub(pattern=j, repl=re.sub(pattern='-', repl='', string=j), string=line)

        for i in rm_pattern:
            line = re.sub(pattern=i, repl='', string=line)

        for k in dot_pattern:
            line = re.sub(pattern=k, repl=re.sub(pattern='...', repl='.', string=k), string=line)

        if line.isupper() == True:  # 문장 전체 대문자 제거
            line = line.replace(line, '')

        if '!' in line:  # '!' -> '.'
            line = line.replace('!', '.')

        if ';' in line:  # ';' -> '.'
            line = line.replace(';', '.')

        if '&' in line:  # '&' -> 'and'
            line = line.replace('&', 'and')

        if '/' in line:  # '/' -> ' and '
            line = line.replace('/', ' and ')

        if '&' in line:  # '&' -> ' and '
            line = line.replace('&', ' and ')

        if '%' in line:  # '%' -> ' percents'
            line = line.replace('%', ' percents')

        if 'Mrs.' in line:  # 'Mrs.' -> 'Mrs'
            line = line.replace('Mrs.', 'Mrs')

        if 'Mr.' in line:  # 'Mr.' -> 'Mr'
            line = line.replace('Mr.', 'Mr')

        if "ma'am" in line:  # 'ma'am' -> 'maam'
            line = line.replace("ma'am", "maam")

        if '  ' in line:  # '  ' -> ' ' # 공백이 두번인 것 제거
            line = line.replace('  ', ' ')


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

    for i in file_list:  # '...','..' 문장 삭제
        if re.search('.*\.\..*',i) == None:
            w.write(i + '\n')

    print(count)
    r.truncate(0)

    r.close()
    w.close()

def attachTag(file_name) :
    r = open('./raw_file/'+ file_name+'_raw.txt', 'r+', encoding='UTF-8')  # raw 파일 읽어오기
    w = open('./tag_file/'+ +'_tag.txt', 'a+', encoding='UTF-8')  # tag가 부착된 tag 파일 생성

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