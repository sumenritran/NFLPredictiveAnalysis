import scrapy
from NFLScraper.items import NFLScraper
from scrapy import Selector

class NFLSpiderGames(scrapy.Spider):
    name = 'nfl_games'
    allowed_domains = ['pro-football-reference.com']    
    
    def start_requests(self):
        min_year = 2002
        max_year = 2018
    
        # NFL results from 2002-2017 (32 teams starting in 2002)    
        for i in range(min_year, max_year):
            yield scrapy.Request('http://www.pro-football-reference.com/years/' + str(i) + '/games.htm', self.parse)
        
    def parse(self, response):
        for i in response.xpath('//a[contains(text(),"boxscore")]/@href'):
            item = NFLScraper()
            url = response.urljoin(i.extract())
            request = scrapy.Request(url, self.contents)
            request.meta['item'] = item
            yield request

    def contents(self, response):                
        item = response.meta['item']
        
        # Extract JavaScript comment
        team_text = response.xpath('//div[@id="all_team_stats"]//comment()').extract()[0]
        info_text = response.xpath('//div[@id="all_game_info"]//comment()').extract()[0]
        week_text = response.xpath('//*[@id="all_other_scores"]/comment()').extract()[0]
        
        team_sel = Selector(text = team_text[4:-3].strip())
        info_sel = Selector(text = info_text[4:-3].strip())
        week_sel = Selector(text = week_text[4:-3].strip())
        
        # Season and week
        year = response.xpath('//*[@id="inner_nav"]/ul/li[5]/div/ul/li[1]/a/text()').extract()[0]
        item['year'] = int(year.split(' ')[0])
        item['week'] = week_sel.xpath('//*[@id="div_other_scores"]/div/h2/a/text()').extract()
        
        # Team names
        item['h_team'] = response.xpath('//*[@id="content"]/div[3]/table/tbody/tr[2]/td[2]/a/text()').extract()[0]
        item['a_team'] = response.xpath('//*[@id="content"]/div[3]/table/tbody/tr[1]/td[2]/a/text()').extract()[0]
        
        # Final team scores
        item['h_score'] = response.xpath('//*[@id="content"]/div[3]/table/tbody/tr[2]/td[last()]/text()').extract()[0]
        item['a_score'] = response.xpath('//*[@id="content"]/div[3]/table/tbody/tr[1]/td[last()]/text()').extract()[0]
        
        # Weather, vegas line, and over/under 
        weather = info_sel.xpath('//*[@id="game_info"]//td/text()').extract()[-3]
        
        item['temp'] = weather.split(' ')[0]
        item['line'] = info_sel.xpath('//*[@id="game_info"]//td/text()').extract()[-2]
        item['over'] = info_sel.xpath('//*[@id="game_info"]//td/text()').extract()[-1]
        
        # Time of possession
        item['h_poss'] = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[12]/td[2]/text()').extract()[0]
        item['a_poss'] = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[12]/td[1]/text()').extract()[0]
        
        # Number of first downs
        item['h_1dcv'] = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[1]/td[2]/text()').extract()[0]
        item['a_1dcv'] = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[1]/td[1]/text()').extract()[0]
        
        # Total rushing yards, attempts and TDs
        h_rush = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[2]/td[2]/text()').extract()[0]
        a_rush = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[2]/td[1]/text()').extract()[0]
        
        item['h_rtot'] = h_rush
        item['a_rtot'] = a_rush
        
        item['h_ratt'] = h_rush[:h_rush.find("-")]
        item['a_ratt'] = a_rush[:a_rush.find("-")]
        
        h_rush = h_rush[h_rush.find("-")+1:]
        a_rush = a_rush[a_rush.find("-")+1:]
        
        item['h_ryds'] = h_rush[:h_rush.find("-")]
        item['a_ryds'] = a_rush[:a_rush.find("-")]

        # Total sacks
        h_sack = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[4]/td[2]/text()').extract()[0]
        a_sack = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[4]/td[1]/text()').extract()[0]
        
        item['h_sack'] = h_sack[:h_sack.find("-")]
        item['a_sack'] = a_sack[:a_sack.find("-")]
        
        # Total passing stats
        item['h_ptot'] = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[3]/td[2]/text()').extract()[0]
        item['a_ptot'] = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[3]/td[1]/text()').extract()[0]
		
        # Net passing yards (passing yards - yards sacked)
        item['h_npyd'] = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[5]/td[2]/text()').extract()[0]
        item['a_npyd'] = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[5]/td[1]/text()').extract()[0]
        
        # Turnovers
        item['h_turn'] = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[8]/td[2]/text()').extract()[0]
        item['a_turn'] = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[8]/td[1]/text()').extract()[0]
        
        # Penalty yards
        h_peny = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[9]/td[2]/text()').extract()[0]
        a_peny = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[9]/td[1]/text()').extract()[0]
        
        item['h_peny'] = h_peny[h_peny.find("-")+1:]
        item['a_peny'] = a_peny[a_peny.find("-")+1:]
        
        # Third down conversions, attempts and conversion rate
        h_3d = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[10]/td[2]/text()').extract()[0]
        a_3d = team_sel.xpath('//*[@id="team_stats"]/tbody/tr[10]/td[1]/text()').extract()[0]
        
        h_3dcv = float(h_3d[:h_3d.find("-")])
        a_3dcv = float(a_3d[:a_3d.find("-")])
        
        h_3att = float(h_3d[h_3d.find("-")+1:])
        a_3att = float(a_3d[a_3d.find("-")+1:])
        
        item['h_3dcv'], item['a_3dcv'] = h_3dcv, a_3dcv
        item['h_3att'], item['a_3att'] = h_3att, a_3att
        
        yield item