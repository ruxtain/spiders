#! /Users/michael/anaconda3/bin/python
# @Date:   2018-08-08 09:20:29

import requests
import json

# 请求 json 的头
raw_headers = """Accept: application/json
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cache-Control: no-cache
Connection: keep-alive
Cookie: referer=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DseUzu-w-TEYsSLforsBdKlDt7_eLl2tYYGfJouq8Ho1H9JTb3y97CnmofbPlF1oY%26wd%3D%26eqid%3D8029001100017d6a000000065b4c40da; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAAFvklEQVRYR62XeWxUdRDHP7MtVykgAQmKIDdS0EJgtxiO7moMBiWAEkAJ%2FiEoimIigsQjUbwCCISKSkQOQ0ESCAGpgoKwLZWA3XIUoXhCBLkvFbAF6Y6Zt7%2BWbg8s2kk23be%2F33tvPvOdmd9UUFWAsYsWMXnWLLrv20dJQoL95JmKjAU%2BAG4TOFu2UMMvCt2AfOBmgYs1vK3Strnn5np%2BVmdSEaTb%2Fv1Efb7yIGOAjw0EGAYcE1jvQUI6kAq8H7tkHDACOAnMFNjrQPYBzwJ%2B4IrttzX3jHbA68BNwGYXtKjFFmgEWFT75rwzbGjBuH5o4rUgl4cqA3l88WLmTJrE4KwsfNEoospfSUl8m5Y2F3jKgawCtgu84pyYALwKtAZmAC8Ai4Guzun2QGPAQMy%2BAPoBTYA04Dhw2H0%2BAyYCc4DJwDrgQeA3IAcYvWtCkNy3hlYpShzIorEWhCqt2IF8AuQJvOlA7AZ7aXcXvb5AAXAnMdXuAU45kMECnyvUIabGz8AQoDdQ5D7T3HUKsBYQ2yNQsuXd4drjoxwyt7%2BEJlzLmFJv40CmzphBakGB1YWnyOV69SzNLCVmVQPyODDFgZhTy4H65UIxADjnaqSlwB8ac24eEADuBz4ERpa7x6J%2FrwPJFZhpa5syRmmvD8Jkbpt6fZCaFDtgingPr%2BCQRd5SwEBedmDfAP2B806RrgLfu%2FvCgNWBpaqlkt2%2F0znfHLjbfS9T%2F4ZAXpw5k5TCwuq6VhtgOvAw8KT7a4UdAe4DfgUWAt85YAukRdwArUYsPcc7JZ5xax2A2cAjTpVRDqgPsMaUFLB0iykyb%2FO%2Fp9aYzExGrFzJ0LVrK4JY17KuZCB1gZVACNjg8r8ZYBVoabbApYgVve35ynxwqbUCeAK4ah1JYKnGmoSpaMptA5ZatwNuBzKAjQKf2jO%2FnD9aO6%2FZTdbycddPreobtFhOVzLNyRuJcEYGBKxlXmvXW%2FNvQXUQCbJJ%2BvW2jhRnGg4nIsnTUG2Iz7de0ntvrPbdbkGz8yftaX509rl6RXzX7MT1u9aNgMScaXgSJJk6dVtL31TrTJ5pdt4GkIGgYyUYWBIHmbsrlZKrW0GsJXvbvTMl6H%2BuymDZe2i4BxE7VD07lvQnqzpa9sZbWde6ERDn8IcgT4O%2BJsHAG95v4UP1kTOngQvoxTYSClkalZmGI%2FkIvYAVKOsQXYCShE87SXraoYo%2BaHZeBohB7l7Tbn%2FP4LF2NL2cRO6th9jV%2FFjc9v8OEt7ZEYkWohyUkP%2BOGFzEOtbboAslGLB6KAdRCqmnJRiwgxINR6YjTEV1toQCdh7FmQeO9oBo24zUHUdaFCUz6qe7OJF0gZUVVPnPIM4Ri3BP0D4SDEQ0O7IX1RQSNUX6p%2F0YB7I1L50SNiMSlqDfuhyau7MXJdE8lCUS8tt4Uw7cqyVL2WJTNyO14G9RGF%2BYxqU6V8jsvLt2FHHpNQHEBspMGkSfp0isEvdJMNCzUnTN6asl3yKslmDAOwA9kNhvSyorWAqiv5uCNjSWglxMvMyyLntqESRWE5asxaBrvJoRJkq63%2BDi0yQn0hNVi%2F4PEgrYSINuzX%2BAqGYByyTof6wKRazrNaFBtE1Gp%2B1nEqI%2Bxh8IYCBLu9SiIk6V5SCPOifOo0ltJNSt0rju2m6sQjWpve3R7IgNioMRnSLpATsY4%2BGz83JA%2BqEMzEjdtumusy0JHe3AwcbnyGp7oPYUuZbnJTtAEk0VCQYequhQ6bVmR2wkGe5NvcpBBBsyPXg4VYwkHwRaogySkP9rDec%2Fheh80OIjyX%2FUb3WpMaLC2naFHG70O0MOpdD2QlN2NT%2FK%2Fyr2cg7anHQnaF8r%2BupAYgpGtrhT365OQcJwCfbKLadYM3yMkAH%2B1W7%2Fe6hOQCShxBdlR4vD5Lc46r1i%2BC%2FdaXWpCXubHa8dkOs5XltrNf4PsdoXStUjSm05WNPn%2FBvIPy92jcKA9S0KAAAAAElFTkSuQmCC%2CMacIntel.1440.900.24; _ga=GA1.2.1423125488.1531724002; UM_distinctid=164a1dd7498606-0d4aad3e3c4f1c-163b6953-13c680-164a1dd7499249; __auc=3a64014f164a1dd78205cd40fae; _uab_collina=153172401732072202858255; Hm_lvt_d4a0e7c3cd16eb58a65472f40e7ee543=1533644159; sid=l7OUsUAMr1QBFPPX784pr05AHYd.x8tDCW3VaGNdDvm74N2801vg1wSHidWahbRwRgZ2lWM; __asc=96c91cf716516fce540a0cd6203; CNZZDATA1256903590=531732945-1531721540-null%7C1533687142; uid=15357596; Hm_lpvt_d4a0e7c3cd16eb58a65472f40e7ee543=1533689025; _cnzz_CV1256903590=is-logon%7Clogged-in%7C1533689026039%26urlname%7Cyg7t1cvwoo%7C1533689026039
Host: huaban.com
Pragma: no-cache
Referer: http://huaban.com/favorite/beauty
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36
X-Request: JSON
X-Requested-With: XMLHttpRequest"""

# 请求一般网页的头
simple_headers = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cache-Control: no-cache
Connection: keep-alive
Host: img.hb.aicdn.com
Pragma: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"""

def get_headers(raw_headers):
    headers = {}
    for line in  raw_headers.splitlines():
        title, content = line.split(':', 1)
        headers[title.strip()] = content.strip()
    return headers

def get_images_from_pin(last_pin, base_url):
    r1 = requests.get(base_url.format(last_pin), headers=get_headers(raw_headers))
    cookies = r1.cookies
    js_data = json.loads(r1.text)

    for pin in js_data["pins"]:
        pin_id = pin['pin_id']
        key = pin['file']['key']
        url = "http://img.hb.aicdn.com/{}".format(key)
        r2 = requests.get(url, headers=get_headers(simple_headers), cookies=cookies)
        with open('images/{}.jpeg'.format(pin_id), 'wb') as f:
            c = r2.content
            if c:
                print(url, 'is saved')
                f.write(c)
    return pin_id # last one


def main():
    base_url = 'http://huaban.com/favorite/beauty?jkkeugp4&max={}&limit=20&wfl=1'
    last_pin = 1779409061
    while True:
        last_pin = get_images_from_pin(last_pin, base_url)

if __name__ == '__main__':
    main()






