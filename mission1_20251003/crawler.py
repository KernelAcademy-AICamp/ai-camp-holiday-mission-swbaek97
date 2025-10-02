import json
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver


URL = "https://nol.yanolja.com/reviews/domestic/1000111922?sort=HOST_CHOICE"


def crawl_yanolja_reviews():
    review_list = []  # 리뷰 저장할 리스트
    driver = webdriver.Chrome()  # 크롬 드라이버 초기화
    driver.get(URL)  # 야놀자 리뷰 페이지 접속

    time.sleep(3)

    # 리뷰 페이지가 스크롤을 해야 아래 리뷰가 더 불러와지기 때문에 스크롤 해야 함
    scroll_count = 8
    for i in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    html = driver.page_source
    soup = bs(html, "html.parser")

    # 우리가 필요한 정보는 1. 리뷰 텍스트, 2. 리뷰 작성일, 3. 별점
    # 페이지에서 가져오기 위한 위치
    review_containers = soup.select(
        "#__next > section > div > div.css-1js0bc8 > div > div > div"
    )
    review_dates = soup.select(
        "#__next > section > div > div.css-1js0bc8 > div > div > div > div.css-1toaz2b > div > div.css-1ivchjf > p"
    )

    for i in range(len(review_containers)):
        review_text = (
            review_containers[i].find("p", class_="content-text css-vjs6b8").text
        )
        review_stars = review_containers[i].select('path[fill="currentColor"]')
        star_cnt = sum(1 for star in review_stars if not star.has_attr("fill-rule"))
        review_date = review_dates[i].get_text(strip=True)

        review_dict = {"review": review_text, "stars": star_cnt, "date": review_date}

        review_list.append(review_dict)

    with open("./resource/reviews.json", "w") as f:
        json.dump(review_list, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    crawl_yanolja_reviews()
