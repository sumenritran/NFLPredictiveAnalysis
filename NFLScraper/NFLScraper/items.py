# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NFLScraper(scrapy.Item):
    year = scrapy.Field()           # Season played
    week = scrapy.Field()           # Week played
    h_team = scrapy.Field()         # Home team
    a_team = scrapy.Field()         # Away team
    h_score = scrapy.Field()        # Home team score
    a_score = scrapy.Field()        # Away team score
    temp = scrapy.Field()           # Temperature of game    
    line = scrapy.Field()           # Vegas game spread 
    over = scrapy.Field()           # Vegas over/under line
    h_poss = scrapy.Field()         # Home team time of possesion
    a_poss = scrapy.Field()         # Away team time of possesion
    h_1dcv = scrapy.Field()         # Home team 1st downs
    a_1dcv = scrapy.Field()         # Away team 1st downs
    h_rtot = scrapy.Field()         # Home team rushing stats
    a_rtot = scrapy.Field()         # Away team rushing stats
    h_ratt = scrapy.Field()         # Home team rushing attempts
    a_ratt = scrapy.Field()         # Away team rushing attempts
    h_ryds = scrapy.Field()         # Home team rushing yards
    a_ryds = scrapy.Field()         # Away team rushing yards
    h_sack = scrapy.Field()         # Times home team was sacked
    a_sack = scrapy.Field()         # Times away team was sacked  
    h_ptot = scrapy.Field()         # Home team total passing stats
    a_ptot = scrapy.Field()         # Away team total passing stats
    h_npyd = scrapy.Field()         # Home team net passing yards
    a_npyd = scrapy.Field()         # Away team net passing yards
    h_turn = scrapy.Field()         # Home team turnovers
    a_turn = scrapy.Field()         # Away team turnovers
    h_peny = scrapy.Field()         # Home team penalty yards
    a_peny = scrapy.Field()         # Away team penalty yards
    h_3dcv = scrapy.Field()         # Home team 3rd down conversions
    a_3dcv = scrapy.Field()         # Away team 3rd down conversions
    h_3att = scrapy.Field()         # Home team 3rd down attempts
    a_3att = scrapy.Field()         # Away team 3rd down attempts