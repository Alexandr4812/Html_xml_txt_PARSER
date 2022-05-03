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

        for node in response.select('table td[style="text-align: justify"]'):
            main_text += node.text    

        pr = f"<a href='{url}'>{title}</a>\n{title_second}\n\n{clean_text(main_text)}\n___separator___\n"
        
        tpr += pr

    return tpr

with open("itivuttaka.txt", "w") as f:
    f.write(mainconfig("itivuttaka.xml"))


#print(mainconfig("udana.xml"))