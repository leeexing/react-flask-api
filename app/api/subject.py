# -*- coding: utf-8 -*-
import requests
import re
from flask import Blueprint
from bs4 import BeautifulSoup
from ..util import ResponseHelper
from ..conf import headers

api_subject = Blueprint('subject', __name__)

reg_num = re.compile(r'\d+')

@api_subject.route('/subject/<subject_id>')
def get_subject_data(subject_id=None):
    """分类浏览"""
    url = 'https://music.douban.com/subject/{}'.format(subject_id)
    music_crawler_content = requests.get(url, headers=headers).content
    music_crawler_soup = BeautifulSoup(music_crawler_content, 'lxml')
    data = {
        'dataType': 'subject',
        'article': {},
        'aside': {}
    }
    data['title'] = music_crawler_soup.select('#wrapper h1')[0].get_text().strip()
    article = music_crawler_soup.select('.article')[0]
    cover_detail = {
        'rate': {},
    }
    # !专辑相关信息
    cover_detail['cover'] = article.select('#mainpic img')[0].get('src')
    cover_detail['info'] = re.split(r'\n+', article.select('#info')[0].get_text().replace(' ', ''))[1:-1]
    cover_detail['rate']['score'] = float(article.select('.rating_self strong')[0].get_text())
    cover_detail['rate']['star'] = int(reg_num.findall(article.select('.rating_right .ll')[0].get('class')[1])[0])
    cover_detail['rate']['rateingPeople'] = int(article.select('.rating_people span')[0].get_text())
    cover_detail['rate']['stars5'] = article.select('.stars5 + .power + span')[0].get_text()
    cover_detail['rate']['stars4'] = article.select('.stars4 + .power + span')[0].get_text()
    cover_detail['rate']['stars3'] = article.select('.stars3 + .power + span')[0].get_text()
    cover_detail['rate']['stars2'] = article.select('.stars2 + .power + span')[0].get_text()
    cover_detail['rate']['stars1'] = article.select('.stars1 + .power + span')[0].get_text()
    cover_detail['summary'] = article.select('#link-report span')[0].get_text().strip()
    cover_detail['trackList'] = article.select('.track-list')[0].get_text().strip()
    data['article']['coverDetail'] = cover_detail
    # !喜欢听【】的人也喜欢的唱片
    knnlike = []
    knnlike_dls = article.select('#db-rec-section .subject-rec-list')
    for dl in knnlike_dls:
        like = {}
        like['cover'] = dl.select('dt img')[0].get('src')
        like['href'] = dl.select('dt a')[0].get('href')
        like['name'] = dl.select('dd a')[0].get_text()
        knnlike.append(like)
    data['article']['subjectRecList'] = knnlike
    # !短评
    short_comment = {
        'hot': [],
        'new': []
    }
    short_comment['total'] = int(reg_num.findall(article.select('.mod-hd h2 a')[0].get_text())[0])
    short_comment['totalHref'] = article.select('.mod-hd h2 a')[0].get('href')
    hot_comments = article.select('#comment-list-wrapper .hot .comment-item')
    for hot in hot_comments:
        hot_obj = {}
        user_stars = hot.select('.comment-info .user-stars')
        hot_obj['author'] = hot.select('.comment-info a')[0].get_text()
        hot_obj['authorLink'] = hot.select('.comment-info a')[0].get('href')
        hot_obj['starts'] = user_stars[0].get('class')[1] if user_stars else 0
        hot_obj['time'] = hot.select('.comment-info .user-stars + span')[0].get_text() if user_stars else hot.select('.comment-info span')[0].get_text()
        hot_obj['voreCount'] = int(hot.select('.comment-vote .vote-count')[0].get_text())
        hot_obj['content'] = hot.select('.comment-content')[0].get_text().strip()
        short_comment['hot'].append(hot_obj)
    new_comments = article.select('#comment-list-wrapper .new .comment-item')
    for new in new_comments:
        new_obj = {}
        user_stars = new.select('.comment-info .user-stars')
        new_obj['author'] = new.select('.comment-info a')[0].get_text()
        new_obj['authorLink'] = new.select('.comment-info a')[0].get('href')
        new_obj['starts'] = user_stars[0].get('class')[1] if user_stars else 0
        new_obj['time'] = new.select('.comment-info .user-stars + span')[0].get_text() if user_stars else new.select('.comment-info span')[0].get_text()
        new_obj['voreCount'] = int(new.select('.comment-vote .vote-count')[0].get_text())
        new_obj['content'] = new.select('.comment-content')[0].get_text().strip()
        short_comment['new'].append(new_obj)
    data['article']['shortComment'] = short_comment
    # !乐评
    music_reviews = {
        'reviewsList': []
    }
    music_comments = article.select('.music-content')[0]
    music_reviews['total'] = music_comments.select('header .pl')[0].get_text()
    review_lists = music_comments.select('.review-list > div')
    for review in review_lists:
        review_obj = {}
        review_obj['avator'] = review.select('.avator img')[0].get('src')
        review_obj['avatorLink'] = review.select('.avator')[0].get('href')
        review_obj['name'] = review.select('.name')[0].get_text()
        review_obj['stars'] = review.select('.name + span')[0].get('class')[0]
        review_obj['time'] = review.select('.main-meta')[0].get_text()
        review_obj['title'] = review.select('.main-bd h2')[0].get_text()
        review_obj['titleLink'] = review.select('.main-bd h2 a')[0].get('href')
        review_obj['shortContent'] = review.select('.short-content')[0].get_text().strip()
        review_obj['actionUp'] = review.select('.action .up span')[0].get_text()
        review_obj['actionDown'] = review.select('.action .down span')[0].get_text().strip()
        review_obj['actionUp'] = review.select('.action .reply')[0].get_text().strip()
        music_reviews['reviewsList'].append(review_obj)
    data['article']['musicComment'] = music_reviews
    # !论坛
    music_discussion = []
    discussions = article.select('#db-discussion-section tr')[1:]
    for discussion in discussions:
        disc_obj = {}
        disc_obj['comment'] = discussion.select('.pl')[0].get_text()
        disc_obj['from'] = discussion.select('.pl')[1].get_text().replace('来自', '')
        disc_obj['fromLink'] = discussion.select('.pl')[1].select('a')[0].get('href')
        disc_obj['reply'] = discussion.select('.pl')[2].get_text()
        disc_obj['time'] = discussion.select('.pl')[3].get_text()
        music_discussion.append(disc_obj)
    data['article']['discussion'] = music_discussion
    # -aside
    aside = music_crawler_soup.select('.aside')[0]
    # !豆瓣成员标签
    tags_section = {
        'tags': []
    }
    tag_sections = aside.select('#db-tags-section')[0]
    tags_section['title'] = tag_sections.select('h2')[0].get_text()
    for item in tag_sections.select('a'):
        tags_section['tags'].append(item.get_text())
    data['aside']['tags'] = music_discussion
    # !豆列推荐
    recomend = []
    for item in aside.select('#db-doulist-section li'):
        rec_obj = {}
        rec_obj['title'] = item.select('a')[0].get_text()
        rec_obj['titleLink'] = item.select('a')[0].get('href')
        rec_obj['author'] = item.select('.pl')[0].get_text()
        recomend.append(rec_obj)
    data['aside']['recommend'] = recomend
    # !谁听这张唱片
    collector = []
    for item in aside.select('#collector > .ll'):
        obj = {}
        obj['cover'] = item.select('img')[0].get('src')
        obj['listener'] = item.select('+ div')[0].select('a')[0].get_text()
        obj['listenTime'] = item.select('+ div')[0].select('.pl')[0].get_text()
        collector.append(obj)
    data['aside']['collector'] = collector
    return ResponseHelper.return_true_data(data=data)
