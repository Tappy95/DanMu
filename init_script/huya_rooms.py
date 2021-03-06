import json

import redis
import requests

redis_conn = None


def get_huya_urls():
    params = {
        "m": 'LiveList',
        "do": 'getLiveListByPage',
        # "gameId": 2135,
        "tagAll": 0,
        "page": '1',
    }
    redis_conn.delete('huya_room_ls')

    for i in range(1, 10):
        params['page'] = i
        resp = requests.get('https://www.huya.com/cache.php', params=params)
        info = json.loads(resp.text)
        room_ids = [room['profileRoom'] for room in info['data']['datas']]
        for room_id in room_ids:
            room_url = 'https://www.huya.com/' + room_id
            redis_conn.lpush('huya_room_ls', room_url)
            print(room_url)


def get_redis_conn():
    global redis_conn
    redis_conn = redis.Redis(host='47.105.131.58', port=6379, db=1, decode_responses=True)
    return redis_conn


if __name__ == '__main__':
    get_redis_conn()
    print('done work')
    get_huya_urls()
    print('done work')
    input('输入任意key结束')
