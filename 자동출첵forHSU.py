from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, pyautogui as pag, os, pywinauto, pygetwindow as gw 

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 함수
# 이클래스로 가서 로그인 
def gotoeclass():
    while True:    
        userid = pag.prompt(text = "아이디를 입력해주세요", title = _maintitle)
        userpw = pag.prompt(text = "비밀번호를 입력해주세요", title = _maintitle)
        _confirm_accnt = pag.confirm(
            text = "아이디: %s , 비밀번호: %s 맞나요?"%(userid,userpw),
            title = "계정 확인", buttons=['yes','no']
            )
        if _confirm_accnt == "yes":
            driver.get("https://learn.hansung.ac.kr/login.php")
            id = driver.find_element(By.NAME,"username")
            id.send_keys(userid)
            pw = driver.find_element(By.NAME,"password")
            pw.send_keys(userpw)
            pw.send_keys(Keys.RETURN)
            time.sleep(1)
            break
        else:
            pass
            
# 플레이 함수
def _play_video():
          
        vod = driver.find_elements(
            By.CSS_SELECTOR,
            ".total_sections li#section-%s ul .vod .activityinstance > a" %주차
            )
        count = int(len(vod))
        print("vod 강의 개수 %s개 확인함"% len(vod))
        # VOD
        for cls in range(count):
            win = gw.getWindowsWithTitle('Chrome')[0] # 윈도우 타이틀에 Chrome 이 포함된 모든 윈도우 수집, 리스트로 리턴
            if win.isActive == False:
                pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
            win.activate()
            print("활성화함")
            vod[cls].click() 
            time.sleep(2)
            
            sw = driver.window_handles[1]
            driver.switch_to.window(sw)
            
            pag.press("enter")
            time.sleep(2)
            ttm = driver.find_element(By.CSS_SELECTOR, ".jw-text-duration").get_attribute('innerText')
            tm = driver.find_element(By.CSS_SELECTOR, ".jw-text-elapsed").get_attribute('innerText')
            if ttm == tm:
                pb = driver.find_element(By.CSS_SELECTOR,".jw-video")
                pb.click()
                time.sleep(2)
            else:
                print("이어보기로 플레이됨")

            try:
                _fastplay = driver.find_element(By.CSS_SELECTOR,".jw-icon-tooltip > .jw-overlay >ul")
                print("이미 플레이한 영상임")
                driver.close()
            except:
                while True:
                    ttm = driver.find_element(By.CSS_SELECTOR, ".jw-text-duration").get_attribute('innerText')
                    tm = driver.find_element(By.CSS_SELECTOR, ".jw-text-elapsed").get_attribute('innerText')
                    if tm == ttm:
                        break
                    time.sleep(5)
                driver.close()
                
            driver.switch_to.window(mw)
            time.sleep(2)
 
# 출석여부확인, 결석 or 지각이면 영상플레이
def _check_attendance():
    name = driver.find_element(By.CSS_SELECTOR,".coursename > h1 > a").text
    def _print_complt():
         print("%s %s주차 출석 완료" %(name,주차));print("")
    print("<%s> 출석 여부 확인 중..." %name)
    try:
        _abstcount = driver.find_element(By.CSS_SELECTOR,".count02 span").text
        _latecount = driver.find_element(By.CSS_SELECTOR,".count03 span").text
        if int(_abstcount) > 0 or int(_latecount) > 0:
            _play_video()
            _print_complt()
        else:
            _print_complt()
            
        """
        attendence = driver.find_elements(By.CSS_SELECTOR,".piece_16")
        absent = driver.find_elements(By.CSS_SELECTOR,".name_text0")
        for a3 in range(len(absent)):
            if attendence[int(주차)-1] == absent[a3]:
                _play_video()
                _print_complt()
                _absent = "none"
        try:
            if _absent == "none":
                pass
        except:
            late = driver.find_elements(By.CSS_SELECTOR,".name_text2")
            for a4 in range(len(late)):
                if attendence[int(주차)-1] == late[a4]:
                    _play_video()
                    _print_complt()
                    _late = "none"
            try:
                if _late == "none":
                    pass
            except:
                _print_complt()
        """
    except:
        _print_complt()   
    
#과목선택
def select_class():
    for sjt in range(범위[0],범위[1]+1):
        while True:
            try:
                one = driver.find_elements(By.CSS_SELECTOR,".label-under") 
                one[sjt].click()
                break
            except:
                pag.alert(text = "팝업 지우고 확인 눌러주세요!!", title = "팝업이 제거되지 않음")
        try:
            _check_attendance() # 출석여부확인
            driver.back()
        except:
            driver.back()
            
# Intro
try:   
    _maintitle = "<<Um's Auto Player for HSU 1.0>>"
    pag.alert(text = "안녕하세요 <자동출석플레이어>입니다!",
                title = _maintitle)
    time.sleep(1)

    pag.alert(text = "로그인되면 팝업을 꼭 없애주세요!\n(수업을 가리는게 있으면 오류가 납니다.)",
                title = _maintitle)

    time.sleep(1)


    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    mw = driver.window_handles[0]

    gotoeclass()

    pag.alert(text = "확인을 누르면 '인증 확인'으로 넘어갑니다! (10초정도 걸림)"
                        ,title = _maintitle)
    #팝업 검사
    while True:
        try:
            poptest = driver.find_element(By.CSS_SELECTOR,".label-under")
            poptest.click()
            try:
                time.sleep(1)
                _sendkakao = driver.find_elements(By.CSS_SELECTOR,".btn.btn-xs.btn-primary") #인증버튼 
                _sendkakao[1].click()
                time.sleep(1)
                _sendkakao2 = driver.find_element(By.ID,"btn-send-kakao")
                _sendkakao2.click()
                while True:
                    _nextregister= pag.prompt(text = "인증을 완료하고 y를 입력해주세요", title=_maintitle)
                    if _nextregister == "y":
                        driver.back()
                        break                   
                    else:
                        print("");print("입력오류");print("")
            except:
                pag.alert(text = "인증이 확인되었습니다.",
                                title = _maintitle)
                driver.back()
                time.sleep(2)
            break
        except:
            return_test = pag.alert(text = "팝업 지우고 나서 확인 눌러주세요!!", title = "팝업이 제거되지 않음")
            
    # 범위 = [1,7] # 범위 임의 지정
    # 주차 = "10"
    # weather_of_autoend = "n"

    # 주차 입력 받기
    while True:
        주차 = pag.prompt(text = "출석할 주차 입력 (숫자만)", title = _maintitle)
        if 주차.isdigit() == True and 1<= int(주차) <=16:
            break    
        else:
            print("");print("입력 오류");print("")
            
    # 범위 입력 받기  
    while True:
        _whole_play = pag.confirm("수업 전체를 플레이할까요?", title = _maintitle, buttons=['yes','no'])
        if _whole_play == 'yes':
            count_class = driver.find_elements(By.CSS_SELECTOR,".course_label_re_02")
            number_class = len(count_class)
            범위 = [0,number_class-1]
            print(범위)
            break
        elif _whole_play == 'no':
            while True:
                범위 = []
                질문 = ["몇 번째 수업부터 할까요?","몇 번째 수업까지 할까요?"]
                for a in range(2):
                    while True:
                        _from_to = pag.prompt("%s(숫자만):\n (커뮤니티는 제외해주세요)." %질문[a], title = _maintitle)
                        try:
                            if _from_to.isdigit() == True and int(_from_to) >= 1:
                                범위.append(int(_from_to))
                                범위[a] = 범위[a] - 1
                                break
                        except:     
                            print("");print("입력 오류");print("")
                if 범위[0] <= 범위[1]:
                    break
                else:
                    print("");print("＃범위 입력 오류. 다시 입력 해주세요!");print("")
            break

    # 컴퓨터 자동 종료 여부 
    while True:
        weather_of_autoend = pag.prompt(text = "출첵 끝나면 컴퓨터를 끌까요?(y or n 입력)", title=_maintitle)
        if weather_of_autoend == "y" or weather_of_autoend == "n":
            break
        else:
            print("");print("입력오류");print("")

    # 출석체크 시작
    print("");print("출석체크 시작!")
    time.sleep(2)

    # 1st play for attendence
    select_class()
    print("출석체크 완료!")
    driver.close()

    if weather_of_autoend == "y":
        print("3초 뒤 컴퓨터가 종료됩니다.")
        _count_down = ["3","2","1"]
        for a1 in _count_down:
            print(a1)
            time.sleep(1)
        driver.quit()
        os.system('shutdown -s -t 0')
            
    elif weather_of_autoend == "n":
        print("");print("Goodbye Seeyou!")
        time.sleep(3)
        driver.quit()
except:
    pag.alert(text = "오류 발생. 프로그램을 다시 실행해주세요;(",
                title = _maintitle)
    









