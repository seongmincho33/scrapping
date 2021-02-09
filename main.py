from naver import search as naver_news_search
from save import save_to_file
search = input("키워드를 입력하세요 : ")
result = naver_news_search(search)
save_to_file(result)

