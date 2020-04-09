# logger = logging.getLogger()
# formatter = logging.Formatter(
#     "%(asctime)s - %(thread)d - %(levelname)s - %(message)s"
# )
# logger.setLevel(logging.INFO)
# if logger.hasHandlers():
#     logger.handlers.clear()
# file_name = f"{os.getcwd()}/logs/{datetime.now()}"
# handler = logging.handlers.TimedRotatingFileHandler(file_name, when="midnight")
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# handler = logging.StreamHandler(stdout)
# handler.setFormatter(formatter)
# logger.addHandler(handler)

#
# driver = webdriver.Firefox(firefox_binary=FirefoxBinary("/usr/bin/firefox-dev"))
# driver.get(url)
#
# # execute script to scroll down the page
# # driver.execute_script(
# #     "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# # sleep for 30s
# time.sleep(5)
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# log(soup.prettify())
# driver.quit()