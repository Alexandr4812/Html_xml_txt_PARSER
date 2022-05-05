import requests
from bs4 import BeautifulSoup

def clean_text(text):
    return ' '.join(text.replace('\r\n', '').replace('\n\n', '\n').split())     
    
def mainconfig(xmlfile):
    tpr = ""       
    result = []
    with open(xmlfile, "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, features="xml")
        for tag in soup.find_all("loc"):
            result.append(tag.text)        
               
    for i in range(0, len(result) - 1):
        url = result[i]
                   
        resp = requests.get(url)
        resp.encoding = "windows-1251"   
        
        main_text = ""
        response = BeautifulSoup(resp.text, "lxml")  
        
        title_tag = response.select('table [width="70%"] td font font')[0]
        title = clean_text(title_tag.text)

        title_second_tag = response.select('table td font[size="5"]')[0]
        title_second = clean_text(title_second_tag.text)
        title_second = title_second.replace(title, " ")

        comments = ""

        if response.select('table td font[color="#999966"]'):
            for i in range(0, len(response.select('table td font[color="#999966"]'))):
                comments_tag = response.select('table td font[color="#999966"]')[i].text
                comments += f"\n\n<u>Примечание {str(i+1)}:</u>\n<em>{clean_text(comments_tag)}</em>"
        else:
            pass

        for node in response.select('table td[style="text-align: justify"]'):
            node = node.text
            n = node.replace("страница 1 / 1", '')
            main_text += n

        main_text_result = f"<a href='{url}'>{title}</a>\n{title_second}\n\n{clean_text(main_text)}{comments}\n___separator___\n"
        
        tpr += main_text_result


    return tpr

with open("udana_test.txt", "w") as f:
    f.write(mainconfig("udana.xml"))


#print(mainconfig("udana.xml"))