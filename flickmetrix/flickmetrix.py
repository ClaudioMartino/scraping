import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scraping # import ../scraping.py
import string
import csv

f = open("../../Downloads/FlickMetrixC2.html", "r")
html = str(f.read())
f.close()

f = open("flick.csv", 'w')
writer = csv.writer(f)

strings = scraping.find_more_strings(html, '<div class="filmInfoContainer">', '<!--SHARE -->')
for i, st in enumerate(strings):
    title = scraping.find_string(st, '<h3 class="title ng-binding">', '</h3>')

    score_begin, score_end = scraping.find_next(st, 0, '<div class="megascore ng-binding" tooltip-enable="!isMobile" tooltip-placement="right" uib-tooltip="Average Rating" tooltip-class="customTooltip combinedScoreTooltip" style="position:relative;margin-bottom:14px;margin-top:3px;margin-left:auto;margin-right:auto;width:65px;height:65px;font-size:32px;line-height:65px;color:white;border-radius:100px;text-align:center;">', '</div>')
    score = st[score_begin:score_end].strip()

    year_begin, year_end = scraping.find_next(st, 0, '<div class="film-section ng-binding">', '&nbsp;</div>')
    year = st[year_begin:year_end]

    genre_begin, genre_end = scraping.find_next(st, year_end, '<div class="film-section ng-binding">', '</div>')
    genre = st[genre_begin:genre_end]

    tmp_director_begin, tmp_director_end = scraping.find_next(st, genre_end, '<!-- ngIf: ::(!(peoplePaths.includes(personURL(director)) && showPersonLink == true)) -->', '<!-- end ngIf: ::(!(peoplePaths.includes(personURL(director)) && showPersonLink == true)) -->')
    tmp_director = st[tmp_director_begin:tmp_director_end]
    director_begin, director_end = scraping.find_next(tmp_director, 0, '>', '<')
    director = tmp_director[director_begin:director_end]

    rt_cnt_begin, rt_cnt_end = scraping.find_next(st, tmp_director_end, '<a style="width:100%;cursor:inherit;" target="_blank" uib-tooltip="', ' Ratings')
    rt_cnt = st[rt_cnt_begin:rt_cnt_end]

    rt_begin, rt_end = scraping.find_next(st, rt_cnt_end,'<div class="rating-bar-score ng-binding">', '</div>')
    rt = st[rt_begin:rt_end]

    meta_cnt_begin, meta_cnt_end = scraping.find_next(st, rt_end, '<a style="width:100%;cursor:inherit;" target="_blank" uib-tooltip="', ' Ratings')
    meta_cnt = st[meta_cnt_begin:meta_cnt_end]

    meta_begin, meta_end = scraping.find_next(st, meta_cnt_end, '<div class="rating-bar-score ng-binding">', '</div>')
    meta = st[meta_begin:meta_end]

    imdb_cnt_begin, imdb_cnt_end = scraping.find_next(st, meta_end, 'style="width:100%;" target="_blank" uib-tooltip="', ' Ratings"')
    imdb_cnt = st[imdb_cnt_begin:imdb_cnt_end]

    imdb_begin, imdb_end = scraping.find_next(st, imdb_cnt_end, '<div class="rating-bar-score ng-binding">', '</div>')
    imdb = st[imdb_begin:imdb_end]

    lett_cnt_begin, lett_cnt_end = scraping.find_next(st, imdb_end, '<a style="width:100%;cursor:inherit;" uib-tooltip="', ' Ratings"')
    lett_cnt = st[lett_cnt_begin:lett_cnt_end]

    lett_begin, lett_end = scraping.find_next(st, lett_cnt_end, '<div class="rating-bar-score ng-binding">', '</div>')
    lett = st[lett_begin:lett_end]

    csv_out = [title, score, year, genre, director, rt_cnt, rt, meta_cnt, meta, imdb_cnt, imdb, lett_cnt, lett]
    print(csv_out)
    writer.writerow(csv_out)
 
f.close()
