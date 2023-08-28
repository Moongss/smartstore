# coding = utf-8
import gc
import threading
import time

import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename, askopenfilenames
from tkinter import messagebox
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from Screenshot import Screenshot

import os
import warnings
from win10toast import ToastNotifier
import logging

from PIL import Image
from io import BytesIO
import os, sys

seller_id = 'get-dream'
download_path = 'result'
goods_code = '8991558015'
goods_url = 'https://smartstore.naver.com/get-dream/products/8991558015'

# to avoid bomb error 
# https://stackoverflow.com/questions/51152059/pillow-in-python-wont-let-me-open-image-exceeds-limit
Image.MAX_IMAGE_PIXELS = None

class ScreenShot():
    def __init__(self, date):
        super().__init__()

        self.toaster = ToastNotifier()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(u'%(asctime)s [%(filename)s:%(lineno)d] [DEBUG] %(message)s ')

        self.streamingHandler = logging.StreamHandler()
        self.streamingHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.streamingHandler)

        self.num = 1
        self.num2 = 1

        self.img_location = None
        self.img_size = None
        self.opt = webdriver.ChromeOptions()

        ## new
        self.opt.add_argument('--headless')
        self.opt.add_argument('--start-maximized')
        self.opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        if getattr(sys, 'frozen', False):
            chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
            self.driver = webdriver.Chrome(service=Service(executable_path=chromedriver_path), options=self.opt)
        else:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.opt)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 3)

        ## need goods code. 
        ## case1. 파일 불러오기
        ## case2. csv 불러오기

        self.logger.debug(f"SELLER ID : {seller_id}")
        self.logger.debug(f"GOODS_URL : {goods_url}")
        self.logger.debug(f"GOODS_CODE : {goods_code}")
        self.logger.debug(f"DOWNLOAD_PATH : {download_path}")
        self.url = f"https://smartstore.naver.com/{seller_id}/products/{goods_code}"

    def remove_floating_tab(self):
        try:
            #왜 자꾸 안됨?
            self.driver.execute_script('window.scrollTo(0, 0);')
            page_height = self.driver.execute_script('return document.documentElement.scrollHeight') 
            page_width = self.driver.execute_script('return document.documentElement.scrollWidth')
            self.driver.set_window_size(page_width, page_height)

            self.driver.switch_to.default_content()
            self.driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight / 2);')

            self.driver.execute_script('''
                document.body.style.overflow='hidden';
                var x = document.getElementById('_productFloatingTab');
                x.style.opacity = 0;     
                x.style.display = 'none';              
            ''')
        except:
            self.remove_floating_tab()
            pass

    def click_more_button(self):
        try:
            self.logger.debug(f"상품페이지 항목을 찾는중...({self.num}회)")
            self.driver.switch_to.default_content()
            self.driver.find_element(By.XPATH, f'//*[@id="INTRODUCE"]/div/div[{self.num}]/div/div/button').click()
            self.logger.debug("상품페이지 항목을 찾는데 성공했습니다.")
        except:
            self.num += 1
            self.click_more_button()
            pass

    def find_goods_img(self):
        try:
            page_height = 50000
            page_width = self.driver.execute_script('return document.documentElement.scrollWidth')
            self.driver.set_window_size(page_width, page_height)  # the trick
            # time.sleep(0.5)

            goods_elem = self.driver.find_element(By.XPATH, f'//*[@id="INTRODUCE"]/div/div[{self.num}]/div/div/div')

            self.img_location = goods_elem.location
            self.img_size = goods_elem.size
            # self.logger.debug(f"상품페이지 위치 : {self.img_location['x']}, {self.img_location['y']}")
            # self.logger.debug(f"상품페이지 사이즈 : {self.img_size['width']}, {self.img_size['height']}")

            self.logger.debug(f"공지사항 여부를 확인중입니다.")
            if int(self.img_size['height']) <= 5000:
                self.logger.debug("공지사항 여부가 감지되었습니다. 2차 캡쳐를 시작합니다.")
                self.find_goods_img2()
                return
            self.logger.debug(f"공지사항이 없는 것으로 확인되었습니다.")
        except:
            self.find_goods_img()

    # 공지사항 있는 경우
    def find_goods_img2(self): 
        try:
            self.num2 += 1
            self.logger.debug(f"[2차] 상품페이지 항목을 찾는중...({self.num2}회)")

            page_height = 50000
            page_width = self.driver.execute_script('return document.documentElement.scrollWidth')
            self.driver.set_window_size(page_width, page_height)  # the trick
            # time.sleep(0.5)

            goods_elem = self.driver.find_element(By.XPATH, f'//*[@id="INTRODUCE"]/div/div[{self.num}]/div[{self.num2}]/div/div')

            self.img_location = goods_elem.location
            self.img_size = goods_elem.size

            if int(self.img_size['height']) <= 5000:
                self.find_goods_img2()
                return

            self.logger.debug("[2차] 상품페이지 항목을 찾는데 성공했습니다.")
        except:
            self.find_goods_img2()

    def crop_goods_image(self):
        # tmp = self.driver.get_screenshot_as_png()
        # new module to capture full screenshot  
        ob = Screenshot.Screenshot()
        ob.full_screenshot(self.driver, save_path=r'.', image_name='./screenshot.png', is_load_at_runtime=True,
                                        load_wait_time=3)
        goods_page = Image.open('./screenshot.png')
        
        margin = int(self.img_size['width'] - 860) / 2 #img size 680px
        left = self.img_location['x']
        top = self.img_location['y']
        right = self.img_location['x'] + self.img_size['width']
        bottom = self.img_location['y'] + self.img_size['height']

        goods_img = goods_page.crop((int(left + margin), top, int(right - margin), bottom))
        goods_img.save(os.path.join(f'{download_path}', f'{seller_id}_{goods_code}.png'))

        self.toaster.show_toast(f"캡쳐 완료", "파일을 확인하세요.",
                                icon_path='./util/logo.ico', duration=10, threaded=True)
    def debug(self):
        while True:
            if input() == ' ':
                break

    def __del__(self):
        self.driver.close()
        self.driver.quit()

    def run(self) -> None:
        self.driver.get(self.url)
        time.sleep(1.5)

        self.remove_floating_tab()
        self.click_more_button()

        self.logger.debug("캡쳐 준비 완료")

        screenshot_path = './screenshot.png'
        self.driver.save_screenshot(screenshot_path)
        self.logger.debug("캡쳐를 시작합니다.")
        self.find_goods_img()
        self.crop_goods_image()
        self.logger.debug("캡처 완료 되었습니다.")

        os.startfile(download_path)
        if os.path.isfile(screenshot_path):
            os.remove(screenshot_path)


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    root = tk.Tk()
    root.title('스마트스토어 상품 페이지 캡처 프로그램')
    root.minsize(400, 300)  # 최소 사이즈

    def run():
        global seller_id
        global download_path
        global goods_code
        global goods_url

        download_path = str(listbox_download_folder.get(0))
        goods_url = str(url.get())
        seller_id = goods_url.split('/')[3]
        goods_code = goods_url.split('/')[5]

        screenshot = ScreenShot(1)
        screenshot.run()
        del screenshot
        gc.collect()

    '''기능 추가'''
    def select_directory():
        try:
            foldername = askdirectory(initialdir="./")
            if foldername:
                listbox_download_folder.delete(0, "end")
                listbox_download_folder.insert(0, foldername)
        except:
            messagebox.showerror("에러", "오류가 발생했습니다.")

    def select_file():
        # try:
        #     filename = askopenfilename(initialdir="./", filetypes=(("Excel files", ".xlsx .xls .csv"), ('All files', '*.*')))
        #     if filename:
        #         listbox2.delete(0, "end")
        #         listbox2.insert(0, filename)
        # except:
            messagebox.showerror("에러", "현재 지원하지 않는 기능입니다.")

    def refresh():
        try:
            reply = messagebox.askyesno("초기화", "정말로 초기화 하시겠습니까?")
            if reply:
                listbox_download_folder.delete(0, "end")
                inputbox_goods_page.delete(0, "end")
                inputbox_goods_page.configure(fg="gray")  # 글자색을 회색으로
                inputbox_goods_page.insert(0, placeholder_text)  # placeholder 재삽입
                messagebox.showinfo("성공", "초기화 되었습니다.")
        except:
            messagebox.showerror("에러", "오류가 발생했습니다.")

    def focus_in(*args):  # 엔트리창에 포커스되는 경우
        if url.get() == placeholder_text:  # placegholder가 있으면
            inputbox_goods_page.delete(0, "end")  # 엔트리 값 삭제(시작위치:0, 끝위치:"end")
            inputbox_goods_page.configure(fg="black")  # 글자색(fg-foreground)은 검정색으로

    def focus_out(*args):  # 엔트리창에 포커스가 떠나는 경우
        if not url.get():  # 엔트리에 값이 입력되어 있지 않으면
            inputbox_goods_page.configure(fg="gray")  # 글자색을 회색으로
            inputbox_goods_page.insert(0, placeholder_text)  # placeholder 재삽입

    '''1. 프레임 생성'''
    # 상단 프레임 (LabelFrame)
    frm1 = tk.LabelFrame(root, text="준비", pady=15, padx=15)   # pad 내부
    frm1.grid(row=0, column=0, pady=10, padx=10, sticky="w") # pad 내부
    root.columnconfigure(0, weight=1)   # 프레임 (0,0)은 크기에 맞춰 늘어나도록
    root.rowconfigure(0, weight=1)     

    # 하단 프레임 (Frame)
    frm2 = tk.Frame(root, pady=10)
    frm2.grid(row=1, column=0, pady=10)

    '''2. 요소 생성'''
    # 레이블
    label_download_folder = tk.Label(frm1, text='사진 다운로드 폴더 선택')
    label_goods_page = tk.Label(frm1, text='상품페이지 경로 입력')
    label_goods_warning = tk.Label(frm1, text='주의: 상품페이지가 너무 긴 경우 수동 저장을 권장합니다.\n')

    # 리스트박스
    listbox_download_folder = tk.Listbox(frm1, width=40, height=1)
    placeholder_text = "https://smartstore.naver.com/..."
    url = tk.StringVar()  # 엔트리에 입력하는 값

    inputbox_goods_page = tk.Entry(frm1, textvariable=url, fg="gray", width=40, font=('Arial', 10))
    inputbox_goods_page.insert(0, placeholder_text)
    inputbox_goods_page.bind("<FocusIn>", focus_in)  # FocusIn 이벤트에 focus_in 함수 바인딩
    inputbox_goods_page.bind("<FocusOut>", focus_out)  # FocusOut 이벤트에 focus_out 함수 바인딩
    # 버튼
    btn_find = tk.Button(frm1, text="찾아보기", width=8, command=select_directory)
    btn_capture = tk.Button(frm2, text="캡처", width=8, command=run)
    btn_clear = tk.Button(frm2, text="초기화", width=8, command=refresh)

    '''3. 요소 배치'''
    # 상단 프레임
    label_download_folder.grid(row=0, column=0, sticky="e")
    label_goods_page.grid(row=1, column=0, sticky="e", pady= 20)
    label_goods_warning.grid(row=2, column=1, sticky="n", pady= 5)
    listbox_download_folder.grid(row=0, column=1, columnspan=2, sticky="we")
    inputbox_goods_page.grid(row=1, column=1, columnspan=2, sticky="we")
    btn_find.grid(row=0, column=3)

    # 상단프레임 grid (2,1)은 창 크기에 맞춰 늘어나도록
    frm1.rowconfigure(2, weight=1)      
    frm1.columnconfigure(1, weight=1)   

    # 하단 프레임
    btn_capture.grid(row=0, column=1, padx=5)
    btn_clear.grid(row=0, column=2)

    '''실행'''
    root.mainloop()