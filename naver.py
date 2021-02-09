import requests
from bs4 import BeautifulSoup

URL = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
URL_NEXT_PAGES = "https://search.naver.com/search.naver?&where=news&query=%ED%83%B1%ED%81%AC&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=89&start="

#마지막페이지 얼마인지 구하기
def get_last_page(input_search):
    result = requests.get(f"{URL}{input_search}")
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class":"sc_page_inner"})
    links = pagination.find_all("a")
    max_page = int(links[-1].string)
    print("Last Page is : ", max_page)
    return max_page

#제목
def news_titles(html):
    titles = []
    for news_block in html:
        title = news_block.find("div", {"class" : "news_area"}).find("a", {"class" : "news_tit"})["title"]
        titles.append(title)
    return titles

#언론사
def news_presses(html):
    presses = []
    for news_block in html:
        press = news_block.find("div", {"class" : "news_area"}).find("a", {"class":"info"}).get_text(strip=True)
        presses.append(press)
    return presses

#날짜
def news_dates(html):
    dates = []
    for news_block in html:
        date = news_block.find("div").find("span", {"class" : "info"}).get_text(strip=True)
        dates.append(date)
    return dates

#링크
def news_links(html):
    links = []
    for news_block in html:
        link = news_block.find("div", {"class" : "news_area"}).find("a", {"class":"news_tit"})["href"]
        links.append(link)
    return links

#스크래핑한 정보를 하나의 리스트로 묶어줍니다.
def make_one_list_dic(first, second, third, fourth, fifth):
    into_list = []
    for i in range(0, len(second)):
        make_into_one_dic = {"keyword":first, "title":second[i], "press":third[i], "date":fourth[i], "link":fifth[i]}
        into_list.append(make_into_one_dic)
    return into_list

#스크래핑함수
def extract(last_page, input_search):
    wanted_things = []
    for page in range(last_page):
        print(f"Scrapping naver page : {page+1}")
        result = requests.get(f"{URL}{input_search}{((page+1)-1)*10 + 1}")
        html = BeautifulSoup(result.text, "html.parser")
        news_blocks = html.find_all("div", {"class" : "news_wrap api_ani_send"})
        titles = news_titles(news_blocks)
        presses = news_presses(news_blocks)
        dates= news_dates(news_blocks)
        links = news_links(news_blocks)
        
        #wanted_thing의 []안에는 요소가{} 이므로 이걸 하나씩 꺼내서 wanted_things 리스트에 옮겨줘야합니다.
        wanted_thing = make_one_list_dic(input_search, titles, presses, dates, links)
        for i in range(0, len(wanted_thing)):
            wanted_things.append(wanted_thing[i])
    #원하던 정보값을 [ {}, {}, {}, ....] 이런형식으로 넘깁니다.   
    return wanted_things
        

def search(input_search):
    last_page = get_last_page(input_search)
    result = extract(last_page, input_search)
    return result
    