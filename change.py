import re
from os.path import getsize

def modifyScripts(file_name):
    file_path = './raw_file/'+ file_name+'_raw.txt'
    r = open('crawling.txt', 'r+', encoding='UTF-8')    # 원본 파일 읽어오기
    w = open(file_path, 'a+', encoding='UTF-8')    # 전처리 된 raw 파일 생성

    rm_pattern = [
        ##지우지 마세용
        # '\[[A-Z].*\]',  # [문장] 제거
        # '\[\s([A-Z].*)\s\]',    #[\s문장\s] 제거
        # '\([A-Z].*\)',  # (문장) 제거
        # '\(\s([A-Z].*)\s\)', # (\s문장\s) 제거

        'OpenSubtitles recommends using Nord VPN',
        'from 3.49 USD/month ----> osdb.link/vpn',
        '.*(Sync and).*',  # 삭제
        '.*(Sync by).*',  # 삭제
        '.*(Synced by).*',  # 삭제
        '.*(Subtitles by).*',  # 삭제
        '.*(Sync corrections ).*',# 삭제
        '.*(Original Air Date).*',  # 삭제
        ".*(D'you).*",  # 삭제
        ".*(y'know).*",  # 삭제

        '.*\[.*',   #[ 포함된 문장 제거
        '.*\].*',   #]
        '.*\(.*',   #( 포함된 문장 제거
        '.*\).*',   #)

        '.*\♪.*',  # '♪' 문장 제거
        '.*\♫.*',  # '♫' 문장 제거
        '.*\#.*',  # '#' 제거

        '^_', # '_' 제거
        '^—', # '—' 제거(다른 —)
        '^–', # '–' 제거(또 다른 –)
        '.*\-.*',  # '-' 문장 제거
        '.*\‐.*',  # '‐' 문장 제거 (다른 '-')
        '.*\–.*',  # '–' 문장 제거 (또 다른 '–')

        '\"', # '"' 제거
        '\"',  # " 제거
        '\"',  # "제거(다른 ")
        '”',  # ”제거(또 다른 ”)

        ####문제의 아이들#####
        "^(')",  # '문장 의  '제거
        "(')$",  # 문장' 의 '제거
        ".*('').*",  # " ''문장'' " 제거

        '.*(\.\s\.).*', # '. .'문장삭제
        '.*(<).*', # '<'문장제거
        '.*(>).*', #'>'문장제거
        '[A-Z].*\:\s',  # '이름:' 제거
        '.*\w+\.\w+\.+.*',   # 문자.문자.로 된 문장 제거 ex)L.A.
        '\s$',   #뒤에 공백이 있을 때
        '.*\:.*',    # ':'문장제거
        '.*\;.*',    # ';'문장제거
        '.*\=.*',    # '=' 문장제거
        '.*\@.*',    # '@' 문장제거
        '.*\*.*',    # '*' 문장제거
        '.*\?\?.*', # '??' 문장 제거
        '.*(www\.).*',   # 'www' 문장제거
        '.*(\.com).*',   # 'com' 문장제거
        '.*\?[0-9].*', #'?숫자' 문장 제거
        '.*\‐\‐.*', # '--'문장 제거
        '.*\.[0-9].*', # 소수점 문장제거
        '.*\s\?.*', #' ?' 문장제거
        '.*{.*', # '{' 문장제거
        '.*¶.*', # '¶' 문장제거
        '.*~.*', # '~' 문장제거
        ".*(\^).*",  # '^' 문장제거
        ".*(\w\?\w).*",  # '글자?글자' 문장제거
        '.*(\+).*', # '+'문장제거
        '.*(\.\,).*', # '.,'문장제거
        '.*(\.\?).*', # '.?'문장제거
        ".*('\w+').*" #'''포함 3글자 이상 문장제거


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

    change_dot=[   #...을 .으로 바꾸는 패턴
        'um...', 'Um...',
        'so...', 'So...',
        'uh...', 'Uh...',
        'oh...', 'Oh...'
    ]

    remove_dot=[    # . 제거 패턴
        'Mr.', 'mr.',
        'Mrs.', 'mrs.',
        'Dr.', 'dr.',
    ]

    lines = r.readlines()  # 전체 스크립트
    lines = list(map(lambda s: s.strip(), lines))  # 전체 스크립트에서 개행문자 삭제
    count = 0  # index, 라인 수
    file_list = list()  # 한 줄씩 입력하기 위해 생성한 빈 리스트

    for line in lines:

        for j in change_pattern:
            line = re.sub(pattern=j, repl=re.sub(pattern='-', repl='', string=j), string=line)

        for k in change_dot:
            line = re.sub(pattern=k, repl=re.sub(pattern='...', repl='.', string=k), string=line)

        for c in remove_dot:
            line = re.sub(pattern=c, repl=re.sub(pattern='.', repl='', string=c), string=line)

        for i in rm_pattern:
            line = re.sub(pattern=i, repl='', string=line)

        if line.isupper() == True:  # 문장 전체 대문자 제거
            line = line.replace(line, '')

        line = line.replace('!', '.')   # '!' -> '.'
        line = line.replace('&', 'and') # '&' -> 'and'
        line = line.replace('/', ' and ')   # '/' -> ' and '
        line = line.replace('%', ' percents')   # '%' -> ' percents'
        line = line.replace("ma'am", "maam")    # 'ma'am' -> 'maam'
        line = line.replace("Ma'am", "Maam") # 'Ma'am' -> 'Maam'
        line = line.replace(",.", ".")  # ',.' -> '.'
        line = line.replace("?.", "?")  # '?.' -> '?'
        line = line.replace("'.", ".")  # "'." -> "."
        line = line.replace(" .", ".")  # " ." -> "."
        line = line.replace("  ", " ")  # "\s\s" -> "\s"

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

    for i in file_list:  # '...','..', '…' 문장 삭제
        if re.search('.*\.\..*',i) == None and re.search('…',i) == None:
            w.write(i + '\n')

    print("==========================================")
    print("Name :", file_name)
    print("Total Lines :", count)
    print("Size :", getsize(file_path)/1024, 'KB')

    r.truncate(0)

    r.close()
    w.close()

def attachTag(file_name) :
    r = open('C:/Users/HancomIT/PycharmProjects/ScriptDataProcessing/raw_file/'+ file_name+'_raw.txt', 'r+', encoding='UTF-8')  # raw 파일 읽어오기
    w = open('C:/Users/HancomIT/PycharmProjects/ScriptDataProcessing/tag_file/'+file_name+'_tag.txt', 'a+', encoding='UTF-8')  # tag가 부착된 tag 파일 생성
    count = 0   # 태그 수

    while True:
        line = r.readline()
        if not line: break

        line = re.sub(pattern='\s', repl='\tO\n', string=line)
        line = re.sub(pattern='\,\tO', repl='\tCOMMA', string=line)
        line = re.sub(pattern='\.\tO', repl='\tPERIOD', string=line)
        line = re.sub(pattern='\?\tO', repl="\tQUESTION", string=line)
        line = re.sub(pattern="'s\tO", repl="\tO\n's\tO", string=line)
        line = re.sub(pattern="'re\tO", repl="\tO\n're\tO", string=line)
        line = re.sub(pattern="'m\tO", repl="\tO\n'm\tO", string=line)
        line = re.sub(pattern="'m\tO", repl="\tO\n'm\tO", string=line)
        line = re.sub(pattern="'ll\tO", repl="\tO\n'll\tO", string=line)
        line = re.sub(pattern="n't\tO", repl="\tO\nn't\tO", string=line)
        line = re.sub(pattern='^\tO', repl='', string=line)
        line= re.sub(pattern='^\s',repl='',string=line)

        w.write(line)
        count += 1

    print("count :", count)
    r.close()
    w.close()