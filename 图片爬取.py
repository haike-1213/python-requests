#encoding=utf-8
import re,requests
import threading

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.63"
}

def get_url(i,dir):
    # print("当前页面:", i)
    res = requests.get(i, headers=headers)
    text = res.content.decode('gb18030')
    replace = re.compile(
        r'<li><a href="(?P<first_url>.{42,55}.html)" target="_blank"><span>[\u4e00-\u9fa5]*</span>.*?<span>\d{4}', re.S)
    toubupipeijieguoduixiang = replace.finditer(text)
    for i in toubupipeijieguoduixiang:
        t = threading.Thread(target=zu,args=(i,dir))
        t.start()



def zu(i,dir):
    toubupipeijieguo = i.group('first_url')
    print("当前组:", toubupipeijieguo)
    res = requests.get(toubupipeijieguo, headers=headers)
    text = res.content.decode('gb18030')
    replace = re.compile(r'\((?P<page>\d*)/\d\)</h1>', re.S)
    meizuyeshuduixiang = replace.search(text)
    meizuyeshu = meizuyeshuduixiang.group('page')
    print("当前页数:", meizuyeshu)
    a = toubupipeijieguo.split(".html")
    gaoqing_html = [
        f'{a[0]}_{i}.html' for i in range(2, int(meizuyeshu))
    ]
    gaoqing_html.append(toubupipeijieguo)
    for i in gaoqing_html:
        t = threading.Thread(target=img,args=(i,dir))
        t.start()


def img(i,dir):
    # print("当前大图:", i)
    res = requests.get(i, headers=headers)
    text = res.content.decode('gb18030')
    replace = re.compile(r'bigImg\'.{5,55}src=\"(?P<bigimg>.{50,70})\"', re.S)
    replace1 = re.compile(r'<h1>(?P<name>[\u4e00-\u9fa5]*.{0,5}) ', re.S)
    gaoqing_img = replace.search(text)
    name = replace1.search(text).group('name')
    bigimg = gaoqing_img.group('bigimg')
    # print("当前纯净图:", gaoqing_img.group('bigimg'))
    res1 = requests.get(gaoqing_img.group('bigimg'), headers=headers)
    with open(f'./{dir}/{name}.jpg', 'wb') as f:
        f.write(res1.content)
        print(f"成功下载{bigimg}")


if __name__ == "__main__":
    while   True:
        try:
            s = int(input('请输入爬取起始页:'))
            r = int(input('请输入结束页:'))
        except:
            continue
        if s<r:
            print('即将开始...')
            break
        else:
            print('起始页必须小于结束页面!')
    while   True:
        dir = input("请输入保存文件夹名称:")
        if not dir:
            dir = '默认高清图'
            break
        else:
            break
    import os
    try:
        os.makedirs(f"./{dir}")
    except:
        pass
    allurl_list = [
        [f'https://m.tupianzj.com/meinv/xiezhen/list_179_{page}.html' for page in range(s, r)],
        [f'https://m.tupianzj.com/meinv/xinggan/list_176_{page}.html' for page in range(s, r)],
        [f'https://m.tupianzj.com/meinv/guzhuang/list_177_{page}.html' for page in range(s, r)],
        [f'https://m.tupianzj.com/meinv/yishu/list_178_{page}.html' for page in range(s, r)],
        [f'https://m.tupianzj.com/meinv/siwa/list_193_{page}.html' for page in range(s, r)],
        [f'https://m.tupianzj.com/meinv/chemo/list_194_{page}.html' for page in range(s, r)],
        [f'https://m.tupianzj.com/meinv/qipao/list_223_{page}.html' for page in range(s, r)],
        [f'https://m.tupianzj.com/meinv/mm/list_218_{page}.html' for page in range(s, r)],
    ]
    all_page_url = []
    for i in allurl_list:
        for a in i:
            all_page_url.append(a)
    print(f"已准备好{len(all_page_url)}页")
    for i in all_page_url:
        t = threading.Thread(target=get_url,args=(i,dir))
        t.start()
        print('已开启页面地址:',i)



