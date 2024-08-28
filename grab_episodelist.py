
def grab_episodelist(config_json = "config.txt"):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-search-engine-choice-screen')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=options)

    show = {}
    finished_episodes = {}

    with open(config_json, "r", encoding='utf-8') as f:
        config_dict = json.load(f)

    driver.get(config_dict["show_url"])
    # driver.maximize_window()

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
        print("accepted cookies")
    except Exception as e:
        print('no cookie button')

    episode_list = {}
    episode_count = 0

    while True:
        try:
            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Load more episodes')]"))))
            # print("more episodes loaded")
        except Exception as e:
            break

    WebElement = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='infinite-scroll-list']")))
    show_soup = BeautifulSoup(WebElement[0].get_attribute('innerHTML'), 'html.parser')
    href_results = show_soup.find_all(href=re.compile("episode"))

    for episode in href_results:
        episode_tag = f"episode_{episode_count}"
        episode_list[episode_tag] = {}
        episode_list[episode_tag]["tag"] = episode_tag
        episode_list[episode_tag]["title"] = episode.text
        episode_list[episode_tag]["href"] = 'https://open.spotify.com' + episode.get('href')
        episode_count += 1
    

    with open(config_dict["show_json"], 'w', encoding='utf-8') as f:
        json.dump(episode_list, f, ensure_ascii=False, indent=2)

    driver.implicitly_wait(10)

    driver.quit()


if __name__ == '__main__':
    grab_episodelist()