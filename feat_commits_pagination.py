import requests
import itertools

def get_commit_branch(url):

    for i in itertools.count():
        try:
            resp = requests.get(url)
            print(resp.status_code)

        
        
            url = resp.links["next"]["url"]

        except KeyError:
            print("Im the last one")
            break



if __name__ == '__main__':
    url = 'https://api.github.com/repos/Shy-Boys-Club/dotties/commits'
    get_commit_branch(url)
