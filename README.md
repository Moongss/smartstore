# 네이버 스마트스토어 상품 상세페이지 크롤러

네이버 스마트스토어 상품 페이지의 "상세 정보 펼쳐보기" 버튼을 누를시 나오는 자세한 상품정보 페이지를 이미지로 저장하는 크롤러입니다. 해당 프로젝트를 진행하며 상품 페이지 크롤링을 위해 selenium, GUI를 위해 tkinter, 전체 화면 캡처를 위해 [Selenium-Screenshot](https://pypi.org/project/Selenium-Screenshot/) 모듈을 사용했습니다.

### 사용법
1. 이 프로젝트를 다운로드 합니다.
2. 아래 명령어를 쉘에 입력합니다.
   ```sh
   pyinstaller.exe -F -n=smartstore --add-binary "chromedriver.exe;." \
                      --icon=./util/logo.ico ./screenshot.py
   ```
3. ``dist``폴더로 가서 ``smartstore.exe``를 실행합니다.
4. **경로저장**: `찾아보기` 버튼을 눌러 사진 저장폴더를 먼저 지정합니다.
5. **URL설정**: **https://** 로 시작하는 상품 페이지 주소를 붙여 넣으면 됩니다.
   ```
   Good Example: ``https://smartstore.naver.com/{SELLER_ID}/products/{PRODUCT_ID}``
   Bad Example: ``smartstore.naver.com/{SELLER_ID}/products/{PRODUCT_ID}``
   ```
6. `캡처` 버튼을 누르면 실행됩니다.
   * 결과는 `{SELLER_ID}_{PRODUCT_ID}.jpg`로 저장됩니다.
   * 프로그램이 저장된 폴더를 자동으로 열어줍니다!


### 주의사항

1. `.exe`파일을 만들때 `-w` 옵션을 넣지 않으면 로그가 뜨는데, 여러번 시도했을때 같은로그가 여러줄 뜰 수 있습니다. 이는 무시해도 좋습니다.
2. 사진이 저장되면 뜨는 toast에서 icon이 없다는 오류가 뜰 경우, `smartstore.exe`와 같은 경로에 `./util/logo.ico`를 넣어주면 됩니다.
   ```
   ./
   ㄴsmartstore.exe
   ㄴutil/
      ㄴlogo.ico
   ```


### 문의사항

기능 추가나, 새로운 버그가 있다면 PR 남겨주기 바랍니다.

---

# Naver Smart Store Product Details Page Crawler

This crawler saves the detailed product information page as an image when you press the "Explore detailed information" button on the Naver Smart Store product page. During the project, we used selenium for product page crawling, tkinter for GUI, and [Selenium-Screenshot](https://pypi.org/project/Selenium-Screenshot/) module for full screen capture.

### How to use it
1. Download this project.
2. Enter the command below in the shell.
   ```sh
   pyinstaller.exe -F -n=smartstore --add-binary "chromedriver.exe;." \
                      --icon=./util/logo.ico ./screenshot.py
   ```
3. Go to the `dist` folder and run `smartstore.exe`.
4. **Save Path**: Click the 'Browse' button to specify the Save Picture folder first.
5. **URL Settings**: Paste the product page address that starts with **https://**.
   > Good Example: ``https://smartstore.naver.com/{SELLER_ID}/products/{PRODUCT_ID}``
   > Bad Example: ``smartstore.naver.com/{SELLER_ID}/products/{PRODUCT_ID}``
6. It is executed by pressing the `Capture` button.
   * The results are saved as `{SELLER_ID}_{PRODUCT_ID}.jpg`.
   * Automatically opens the folder where the program is stored!


### Precautions

1. If you do not include the `-w` option when creating the `.exe` file, the log appears, but if you try multiple times, the same log may appear in multiple rows. This is negligible.
2. If you see an error that says no icon in the toast that appears when the picture is saved, you can put `./util/logo.ico` in the same path as `smartstore.exe`.
   ```
   ./
   ㄴsmartstore.exe
   Butil/
      ㄴlogo.ico
   ```

### Contact

Please add features or leave PR if you have any new bugs.