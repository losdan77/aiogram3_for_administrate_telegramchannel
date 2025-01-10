from bs4 import BeautifulSoup
import requests
import lxml
import random

mass_user_agent = ['Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
                    'Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)',
                    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
                    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
                    'Mozilla/5.0 (X11; Linux i686; rv:7.0a1) Gecko/20110603 SeaMonkey/2.2a1pre',
                    'Mozilla/5.0 (X11; Linux i686; rv:7.0a1) Gecko/20110530 SeaMonkey/2.2a1pre',
                    'Mozilla/5.0 (X11; Linux i686; rv:7.0a1) Gecko/20110526 SeaMonkey/2.2a1pre'
                   ]

url = 'https://www.reddit.com/r/memes/'
text_div_class = 'block relative cursor-pointer group bg-neutral-background focus-within:bg-neutral-background-hover hover:bg-neutral-background-hover xs:rounded-[16px] px-md py-2xs my-2xs nd:visible'
photo_div_class = 'media-lightbox-img max-h-[100vw] h-full w-full object-contain overflow-hidden relative bg-black'

headers = {
    'User-Agent': random.choice(mass_user_agent)
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

photo_url = soup.find(class_=photo_div_class).find('img')['src']
title_text = soup.find(class_=text_div_class).find('a')
    
with open('photo_url.txt', 'r') as file:
    last_photo_url = file.readline()

if photo_url!=last_photo_url:
    with open('photo_url.txt', 'w') as file:
        file.write(photo_url)

    photo = requests.get(photo_url, headers=headers)

    with open('photo.png', 'wb') as file:
        file.write(photo.content)

print(title_text.text)