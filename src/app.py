from models.base import FacebookStreamingCrawl

if __name__ == '__main__':
    crawler = FacebookStreamingCrawl("https://www.facebook.com/MeiMeiCuteo/videos/9587671664592388")
    crawler.exec_crawl(retry_on_failure=1, delay_per_comment=0.5)
