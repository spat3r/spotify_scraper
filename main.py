from grab_episodelist import *
from grab_transcripts import *

def main():
    try:
        with open("config.txt", "r", encoding='utf-8') as f:
            configuration = json.load(f)
    except:
        configuration = {}

    configuration["username"] = "username"
    configuration["password"] = "password"
    configuration["show_json"] = "show.txt"
    configuration["show_url"] = "https://open.spotify.com/show/6VaJwyS2KXxiXqR77jqzmP"

    with open('config.txt', 'w', encoding='utf-8') as f:
        json.dump(configuration, f, ensure_ascii=False, indent=2)

    grab_transcripts()
    grab_episodelist()

if __name__ == '__main__':
    main()