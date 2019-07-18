# coding=utf-8
from selenium import webdriver
import time
import Tkinter as tk
from selenium.common.exceptions import NoSuchElementException
from functools import partial
def entry():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.weibo.com/login.php')
    time.sleep(3)
    # 用户名 处填入用户名
    try:
        usernamejs = "document.getElementById('loginname').value= '{}'".format(e1.get())
        driver.execute_script(usernamejs)
    except Exception as e:
        print(e)
        pass

    # 密码 处填入密码
    try:
        passwordjs = "document.querySelector('#pl_login_form > div > div:nth-child(3) > div.info_list.password > div > input').value='{}';".format(e2.get())
        driver.execute_script(passwordjs)
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
        pass
    except:
        try:
            time.sleep(10)
            driver.find_element_by_id("message_sms_login").click()
        except Exception as e:
            print(e)
            print("Please try again, a problem occured")
            driver.quit()

        # 请输入收到的验证码，每输入一位就按一下回车，输入最后一位后也需要按回车
        print("Please type in vericode in the terminal")
        print("Press enter every time")
        veriCode1 = input("First number of your vericode:")
        veriCode2 = input("Second number of your vericode:")
        veriCode3 = input("Third number of your vericode:")
        veriCode4 = input("Fourth number of your vericode:")
        veriCode5 = input("Fifth number of your vericode:")
        veriCode6 = input("Sixth number of your vericode:")
        
        try:
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
        except: 
            print("Please try again, a problem occured")
            driver.quit()

    print("Successfully logged in")
    time.sleep(5)
    driver.get("https://www.weibo.com/u/5536456430?refer_flag=1005055013_&is_all=1")
    time.sleep(2)
    totalscroll = 0
    hreflist = []
    while totalscroll < 4:
        scrolldown = "window.scrollTo(10000,document.body.scrollHeight)"
        driver.execute_script(scrolldown)
        time.sleep(4)
        totalscroll += 1

    scrollup = "window.scrollTo(10000,0)"
    driver.execute_script(scrollup)
    head = driver.find_element_by_xpath(r'//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]')
    hheight = head.size["height"]
    bar = driver.find_element_by_xpath(r'//*[@id="Pl_Official_Nav__2"]/div')
    bheight = bar.size["height"]
    fheight = hheight + bheight
    scroll = "window.scrollBy(10000, {})".format(fheight)
    time.sleep(1)
    totalwb = 0
    totalhref = 0
    wbs = "return document.getElementsByClassName('WB_feed_detail')"
    wbelements = driver.execute_script(wbs)
    while totalwb < len(wbelements):
        time.sleep(2)
        wb = wbelements[totalwb]
        wbheight = wb.size["height"]
        print("This is the {} weibo").format(totalwb)
        # 如果有展开全文则点击展开全文并更新本条微博大小
        try:
            wb.find_element_by_class_name("WB_text_opt").click()
            wbheight = wb.size["height"]
        except:
            pass
        time.sleep(1)
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

    totalsuccess = 0
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
            totalsuccess += 1    
            print("You have reported {} weibo").format(totalsuccess)
            time.sleep(1)
        except:
            pass
    print("Success!")
    driver.quit()
print 
master = tk.Tk()
master.title("阿云奶盖的反黑小程序")
label1 = tk.Label(master, text="用户名").grid(row=0)
label2 = tk.Label(master, text="密码").grid(row=1)
e1 = tk.Entry(master)
e2 = tk.Entry(master)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
tk.Button(master, text="ok", command= entry).grid(row=2,column= 1)
master.mainloop()
