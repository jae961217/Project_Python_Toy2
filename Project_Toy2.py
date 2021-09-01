import requests
from requests import models
from tmdb import TMDBHelper
from pprint import pprint


def popular_count():
    """
    popular 영화목록의 개수 출력.
    """
    tmdb = TMDBHelper('9fdc58305c6e8e783df774eb9638b740')
    url = tmdb.get_request_url(language='ko', region='KR')
    data = requests.get(url).json()
    pprint(data['results'][0])
    return len(data['results'])

def vote_average_movies():
    """
    popular 영화목록중 vote_average가 8 이상인 영화목록 출력.
    """
    res=[]
    tmdb = TMDBHelper('9fdc58305c6e8e783df774eb9638b740')
    url = tmdb.get_request_url(language='ko', region='KR')
    data = requests.get(url).json()
    for i in data['results']:
        if i['vote_average']>=8:
            res.append(i['title'])
    return res

def ranking():
    """
    popular 영화목록을 정렬하여 평점순으로 5개 출력.
    """
    res=[]
    tmp=dict()
    tmdb = TMDBHelper('9fdc58305c6e8e783df774eb9638b740')
    url = tmdb.get_request_url(language='ko', region='KR')
    data = requests.get(url).json()
    for i in data['results']:
        tmp[i['title']]=i['vote_average']
    tmp=sorted(tmp.items(), key=lambda x:x[1], reverse=True)
    for i in range(5):
        res.append(tmp[i][0])

    return res


def recommendation(title):
    """
    제목에 해당하는 영화가 있으면
    해당 영화의 id를 기반으로 추천 영화 목록을 출력.
    추천 영화가 없을 경우 [] 출력.
    영화 id검색에 실패할 경우 None 출력.
    """
    res=[]
    tmdb=TMDBHelper('9fdc58305c6e8e783df774eb9638b740')

    movie_id = tmdb.get_movie_id(title)
    if movie_id!=None:
        url=tmdb.get_request_url(method=f'/movie/{movie_id}/recommendations',language='ko',region='KR')
        data = requests.get(url).json()
        for i in data['results']:
            res.append(i['title'])
        return res
    else:
        return None

def credits(title):
    """
    제목에 해당하는 영화가 있으면
    해당 영화 id를 통해 영화 상세정보를 검색하여
    주연배우 목록과 목록을 출력.
    영화 id검색에 실패할 경우 None 출력.
    """
    cast=[]
    crew=[]
    tmdb=TMDBHelper('9fdc58305c6e8e783df774eb9638b740')

    movie_id = tmdb.get_movie_id(title)
    if movie_id!=None:
        url=tmdb.get_request_url(method=f'/movie/{movie_id}/credits',language='ko',region='KR')
        data = requests.get(url).json()
        for i in data['cast']:
            if i['cast_id']<10:
                cast.append(i['original_name'])

        for i in data['crew']:
            if i['department']=='Directing':
                crew.append(i['original_name'])
    print(cast,crew)
    res={'cast':cast, 'crew':crew}
    return res

if __name__ == '__main__':
    print(popular_count())

    pprint(vote_average_movies())

    pprint(ranking())

    pprint(recommendation('기생충'))
    pprint(recommendation('그래비티'))
    pprint(recommendation('검색할 수 없는 영화'))

    pprint(credits('기생충'))
    pprint(credits('검색할 수 없는 영화'))