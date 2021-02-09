import csv

def save_to_file(searched_contents):
    file = open("searched_news.csv", mode="w", encoding="UTF-8-SIG")
    #라이터 를 만들어서 writer변수에 넣어주자
    writer = csv.writer(file)
    #리스트형태로 넣어줘야 됩니다.
    writer.writerow(["키워드", "제목", "언론사", "날짜", "링크"])
    for content in searched_contents:
        #job은 리스트인데 안에 요소는 딕셔너리다
        #딕셔너리의 좋은점은 안에 키를 알면 value값을 가져올수 있다는것이다. 또는 Value값만 가져올 수도 있다.
        #list()로 감싸줘야하는데 이유는 데이터타입이 이상한걸 줘서 그렇다
        writer.writerow(list(content.values()))
    return