from Base import Base
from const import BaseURL
import json
import time
import re

class BlogScraper(Base):

    def __init__(self):
        super().__init__()
        self.debug = True
        self.scraper_type = "ForumScraper"
        self.log_setup()
        self.posts = []
        self.links =[]

    #
    # def product_iterator(self, url):
    #     soup, error = self.link_requestor(url)
    #     if status
    #     title = soup.find("h1")
    #     title = title.get_text() if title else False
    #     brand = soup.find("h2", attrs={"itemprop": "brand"})
    #     if not brand:
    #         brand = soup.find("div", text="Brand")
    #         brand = brand.findNext("div") if brand else False
    #     brand = brand.get_text() if brand else False
    #     mpn = soup.find("h2", attrs={"itemprop": "mpn"})
    #     if not mpn:
    #         mpn = soup.find("div", text="MPN")
    #         mpn = mpn.findNext("div") if mpn else False
    #     if mpn:
    #         mpn = mpn.get_text()
    #         if mpn.find(" ") == -1:#todo fake check
    #             return title, mpn, brand
    #         else:
    #             print(mpn)  # todo: remove line after r &D
    #     return False

    def get_links(self, url):
        start = 0
        while start <= 160:
            soup = self.link_requestor(f"{url}{start}")
            if self.status:
                tr_tags = soup.find_all("table")[1].find_all("tr")[1:]
                for tr in tr_tags:
                    td = tr.find('td')
                    link = td.find("a", attrs={"class": "topictitle"}).get('href')
                    self.links.append(
                        f"https://forum.mobilism.org/{link}")
                    if len(self.links)>10:
                        break
            break
            start += 40
        print(len(self.links))

    def get_details(self):
        for link in self.links:
            soup = self.link_requestor(link)
            if not self.status:
                self.logger.error(f"Found nothing against {link}")
                continue
            title = soup.find('h3').text
            post = str(soup.select_one('div.content'))
            post = re.sub(r'<br.>', '\n', post)
            post = re.sub(r"<.+?>", ' ', post)
            self.posts.append({'title':title, 'details': post})

    def demo(self, link):
        soup = self.link_requestor(link)
        if not self.status:
            self.logger.error(f"Found nothing against {link}")
            exit()
        title = soup.find('h3').text
        post = str(soup.select_one('div.content'))
        # post = re.sub(r'<br.>', '\n', post)
        # post = re.sub(r"<.+?>", '', post)
        print(post)
        self.posts.append({'title': title, 'details': post})
        self.logger.info(self.posts)

    def save_data(self):
        # todo change json path
        with open(f"posts.json", "w") as write_file:
            json.dump(self.posts, write_file, indent=4)

    def run(self):
        self.get_links(BaseURL)
        if not self.status:
            self.logger.error("No posts")
            return False
        self.get_details()
        self.save_data()
        self.logger.info(self.posts)
        return True

if __name__ == "__main__":
    # status = BlogScraper().run()
    # print(f"{status}")
    b = BlogScraper()
    b.demo('https://forum.mobilism.org/viewtopic.php?f=399&t=389017')
    b.save_data()