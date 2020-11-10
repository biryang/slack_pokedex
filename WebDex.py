import requests
from bs4 import BeautifulSoup


def poke_dex_url(dex_num):
    URL = 'https://pokemonkorea.co.kr/pokedex?word=&characters=&area=&'
    poke_dex = dex_num
    res = requests.get(f"{URL}snumber={poke_dex}&snumber2={poke_dex}")
    dex_soup = BeautifulSoup(res.text, "html.parser")
    return dex_soup


def poke_dex_name(html):
    tag_name = f"#top > section > #pokedexlist > li > a > div.bx-txt > h3"
    poke_name = html.select(tag_name)
    return poke_name[0].text


def poke_dex_img(html):
    tag_name = f"#top > section > #pokedexlist > li > a > div.img > div > img"
    poke_img = html.select(tag_name)
    return poke_img[0]['src']


def poke_dex_info(dex_num):
    html = poke_dex_url(dex_num)
    name = poke_dex_name(html)
    img = poke_dex_img(html)
    return {'name': name, 'img': img}
