from subprocess import Popen, PIPE
import requests
import webbrowser


def execute_return(cmd):
    args = cmd.split()
    proc = Popen(args, stdout = PIPE, stderr = PIPE)
    output, error = proc.communicate()
    return output, error


def make_request(error):
    response = requests.get("https://api.stackexchange.com"+"/2.3/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(error))
    return response.json()


def get_urls(json_dict):
    url_list = []
    count = 0
    for item in json_dict["items"]:
        if item["is_answered"]:
            url_list.append(item["link"])
        count += 1
        if count == 3 or count == len(item):
            return url_list
    

def open_url(url_list):
    for url in url_list:
        webbrowser.open(url)


if __name__ == "__main__":
    operation, error = execute_return("python test.py")
    error_message = error.decode("utf-8").split("\r\n")[-2]
    print(error_message)
    if error_message:
        filter_error = error_message.split(":")
        jsons = [make_request(filter_error[0]), make_request(filter_error[1]), make_request(error_message)] 
        open_url(get_urls(jsons[0]))
        open_url(get_urls(jsons[1]))
        open_url(get_urls(jsons[2]))
    else:
        print("No errors found")



