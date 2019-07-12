# coding=utf-8
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.weibo.com/login.php')

# username 处填入用户名
try:
    driver.execute_script(
        "document.getElementById('loginname').value='username';")
except:
    pass

# password 处填入密码
try:
    driver.execute_script(
        "document.querySelector('#pl_login_form > div > div:nth-child(3) > div.info_list.password > div > input').value='password';")
except:
    pass

# 按登陆按钮
time.sleep(5)
driver.find_element_by_xpath(
    '//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()

# 如果找到微博登陆后顶部条则返回成功
try:
    time.sleep(10)
    driver.find_element_by_id('plc_top')
    print("登陆成功")
    pass
except:
    # 请输入收到的验证码，每输入一位就按一下回车，输入最后一位后也需要按回车
    try:
        time.sleep(10)
        driver.find_element_by_id("message_sms_login").click()
        print("您开启了验证保护，请在终端输入输入验证码")
        print("每输入一位按一次回车")
        veriCode1 = input("验证码第1位:")
        veriCode2 = input("验证码第2位:")
        veriCode3 = input("验证码第3位:")
        veriCode4 = input("验证码第4位:")
        veriCode5 = input("验证码第5位:")
        veriCode6 = input("验证码第6位:")
    except Exception as e:
        print(e)
        pass
    print("登陆成功")
    time.sleep(2)
    driver.find_element_by_xpath(
        r'//*[@id="message_content"]/div/div[1]/input[1]').send_keys(veriCode1)
    time.sleep(1)
    driver.find_element_by_xpath(
        r'//*[@id="message_content"]/div/div[1]/input[2]').send_keys(veriCode2)
    time.sleep(1)
    driver.find_element_by_xpath(
        r'//*[@id="message_content"]/div/div[1]/input[3]').send_keys(veriCode3)
    time.sleep(1)
    driver.find_element_by_xpath(
        r'//*[@id="message_content"]/div/div[1]/input[4]').send_keys(veriCode4)
    time.sleep(1)
    driver.find_element_by_xpath(
        r'//*[@id="message_content"]/div/div[1]/input[5]').send_keys(veriCode5)
    time.sleep(1)
    driver.find_element_by_xpath(
        r'//*[@id="message_content"]/div/div[1]/input[6]').send_keys(veriCode6)
    time.sleep(1)
    driver.find_element_by_id("message_confirm").click()


time.sleep(5)
# 阿云嘎反黑站主页
driver.get("https://www.weibo.com/u/5536456430?refer_flag=1005055013_&is_all=1")
time.sleep(1)
totalscroll = 0
hreflist = []


# 滚动加载到底再回来顶部
while totalscroll < 4:
    scrolldown = "window.scrollTo(10000,document.body.scrollHeight)"
    driver.execute_script(scrolldown)
    time.sleep(4)
    totalscroll += 1

scrollup = "window.scrollTo(10000,0)"
driver.execute_script(scrollup)
# 滚动header
head = driver.find_element_by_xpath(
    r'//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]')
hheight = head.size["height"]
# 滚动headbar
bar = driver.find_element_by_xpath(r'//*[@id="Pl_Official_Nav__2"]/div')
bheight = bar.size["height"]
fheight = hheight + bheight
scroll = "window.scrollBy(10000, {})".format(fheight)
time.sleep(1)

# 遍历本页所有微博
totalwb = 0
wbs = "return document.getElementsByClassName('WB_feed_detail')"
wbelements = driver.execute_script(wbs)
while totalwb < len(wbelements):
    time.sleep(2)
    wb = wbelements[totalwb]
    wbheight = wb.size["height"]
    print("This is the {} th weibo").format(totalwb)

    # 如果有展开全文则点击展开全文并更新本条微博大小
    try:
        wb.find_element_by_class_name("WB_text_opt").click()
        wbheight = wb.size["height"]
    except:
        pass

    time.sleep(2)
    # 爬取本条微博内所有名为网页链接的超链接并存储
    try:
        a_elements = wb.find_elements_by_tag_name('a')
        alen = len(a_elements)
        lnr = 0
        for a_element in a_elements:
            title = a_element.get_attribute('title')
            wname = u'网页链接'
            wnameutf8 = wname.encode('utf-8')
            assert(wnameutf8.decode('utf-8') == wname)
            titleutf8 = title.encode('utf-8')
            if(titleutf8 == wnameutf8):
                link = a_element.get_attribute('href')
                if link not in hreflist:
                    print(link)
                    hreflist.append(link)
                    lnr += 1
    except Exception as e:
        print(e)

    print(lnr)
    scroll = "window.scrollBy(10000, {})".format(wbheight)
    driver.execute_script(scroll)
    totalwb += 1


for l in hreflist:
    driver.get(l)
    try:
        driver.find_element_by_link_text("有害信息").click()
        time.sleep(2)
        tobottom = "window.scrollTo(10000,document.body.scrollHeight)"
        driver.execute_script(tobottom)
        driver.find_element_by_link_text("其他有害信息").click()
        time.sleep(1)
        try:
            driver.find_element_by_xpath(
                r'//*[@id="pl_report_complaint_h5"]/section[2]/dl/dd/label/span').click()
            time.sleep(1)
            driver.find_element_by_xpath(
                r'//*[@id="pl_report_complaint_h5"]/section[2]/dl/dt/a').click()
        except NoSuchElementException:
            driver.find_element_by_xpath(
                r'//*[@id="pl_report_complaint"]/div[1]/div[2]/p[3]/label/input').click()
            time.sleep(1)
            driver.find_element_by_xpath(
                r'//*[@id="pl_report_complaint"]/div[1]/div[2]/a').click()
        except:
            print(l)
            pass
        time.sleep(8)
    except:
        pass

print("反黑完成！")
