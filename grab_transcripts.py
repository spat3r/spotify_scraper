from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time as t
from datetime import date
from bs4 import BeautifulSoup
import json

def grab_transcripts(config_json = "config.txt"):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-search-engine-choice-screen')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=options)

    failed_episodes = {}
    show = {}
    finished_episodes = {}

    with open(config_json, "r", encoding='utf-8') as f:
        config_dict = json.load(f)

    username = config_dict["username"]
    password = config_dict["password"]
    driver.get("https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2F")

    username_field = driver.find_element(By.ID, 'login-username')
    username_field.clear()
    username_field.send_keys(username)

    password_field = driver.find_element(By.ID, 'login-password')
    password_field.clear()
    password_field.send_keys(password)

    driver.find_element(By.ID, "login-button").send_keys(Keys.ENTER)

    try:
        WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
        print("accepted cookies")
    except Exception as e:
        print('no cookie button')

    driver.implicitly_wait(30)

    # read list of 
    with open(config_dict["show_json"], "r", encoding='utf-8') as f:
        show = json.load(f)
    
    for episode in show.keys():
        with open(f"export/{show[episode]['tag']}.md", "w", encoding="utf-8") as text_file:
            text_file.write(f"# {show[episode]['title']}\n")
            text_file.write(f"---\ntags: [Podcast]\ndate: {date.today()}\n---\n")
            text_file.write("![](https://i.scdn.co/image/ab67656300005f1f3bd056f6f7ecd676eb017b90)\n")
            text_file.write("## Description: \n> {{Description}}\n")
            text_file.write(f"-> [Podcast Link]({show[episode]['href']})\n\n")
            text_file.write("## Notes:\n\n## Transcript:")

            driver.get(show[episode]["href"])
            driver.implicitly_wait(30)

            try:
                driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Transcript')]"))))
            except Exception as e:
                print("transcripts couldnt be loaded on the first time")
                try:
                    driver.implicitly_wait(30)
                    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Transcript')]"))))
                except Exception as e:
                    print("no transcript available")
                    failed_episodes[episode] = show[episode]
                    show.remove(episode)
                    continue

            episode_transcript = WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='root']")))
            
            for WebElement in episode_transcript:
                elementSoup = BeautifulSoup(WebElement.get_attribute('innerHTML'),'html.parser')
                episode_htmls = elementSoup.select('div.l6peddfW1BiAnd1a_mF3')
            
            for div in episode_htmls:
                string = "\n"
                # Get timestamp from button
                time_tag = div.find('button', class_='OexEjZt7Kf7pFUW701v8')
                if time_tag:
                    string += f"\n\n[{time_tag.get_text(strip=True)}]\n\n"
                
                # Grap text from the spans
                for text_content in div.find_all('span', class_='F3BJWbXwGSqNOwZHInLz'):
                    string += f"{text_content.get_text(strip=True)} "
                
                text_file.write(string)
                
            finished_episodes[episode] = show[episode]
            show.remove(episode)
            
        t.sleep(20)

    driver.implicitly_wait(10)

    driver.quit()
    with open('failed_episodes.txt', 'w', encoding='utf-8') as f:
        json.dump(failed_episodes, f, ensure_ascii=False, indent=2)
    with open(config_dict["show_json"], 'w', encoding='utf-8') as f:
        json.dump(show, f, ensure_ascii=False, indent=2)
    with open('finished_episodes.txt', 'w', encoding='utf-8') as f:
        json.dump(finished_episodes, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    grab_transcripts()