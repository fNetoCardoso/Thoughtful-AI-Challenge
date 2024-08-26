from config import Config
from scraper import NewsScraper
def main():
    config = Config()
    scraper = NewsScraper(config = config,
                          button_selector = "div.site-header__search-trigger button", 
                          input_selector = "input.search-bar__input", 
                          select_id_selector = "search-sort-option", 
                          result_selector = "div.search-result__list", 
                          title_selector = ".gc__title",
                          query_search = "gaza",
                          filter_option = "date",
                          submit_search_button_selector = "div.search-bar__button button",
                          description_selector=".gc__excerpt",
                          date_selector = ".gc__date__date",
                          image_selector = ".gc__image-wrap"
    )
    scraper.run()
    #scraper.search_news(search_phrase)
    #scraper.filter_results(category)
    #news_items = scraper.scrape_news(search_phrase, months)
    #save_to_excel(news_items, config.OUTPUT_DIR)
    #scraper.close()

if __name__ == "__main__":
    #search_phrase = "economy"
    #category = "Business"
    #months = 1
    main()
