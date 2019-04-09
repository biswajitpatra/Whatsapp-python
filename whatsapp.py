import os
import string
import time
from tkinter import *

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

selc = ["Friend prashant", "Friend Shriya Electrical Cet"]
printable = set(string.printable)


def result(gstring):
    return gstring


def refresh():
    table_preuser = driver.find_elements(By.XPATH,"//div[@class=\"_9tCEa\"]/div[last()]/div[1]")
    if len(table_preuser)!=0:
      table_preuser=table_preuser[0] 
      #print("title of chat..",table_preuser.get_attribute("class"))
      if table_preuser.get_attribute("class") == "_3_7SH _3DFk6 message-in tail":
       puser=driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div[1]/div/span').get_attribute("title")
       text_fu=table_preuser.find_elements(By.XPATH,'.//span[@dir="ltr"]')
       if len(text_fu)!=0:
          text_fu=text_fu[0].text
          text_fu = "".join(filter(lambda x: x in printable, text_fu))
          l1["text"] = puser+":"+text_fu
          Wfunc(puser, "ECHO :"+result(text_fu), 2)
       else:
          Wfunc(puser, "Emoji detected no reply", 2)   

         
    msg_psearch = driver.find_elements_by_xpath('//div[@class="_2EXPL CxUIE"]/div[2]/div[1]/div[1]/span[1]/span[@dir="auto"]')
    if msg_psearch == []:
         l1["text"] = "NO ONE"
    else:
         for x in msg_psearch:
               text_fu = x.find_element_by_xpath("./ancestor::div[3]/div[2]/div[1]/span")
               text_fu = text_fu.get_attribute("title")
               text_fu = "".join(filter(lambda x: x in printable, text_fu))
               l1["text"] = x.text+":"+text_fu
               print("DETECTED BLACKELNED"+l1["text"])
               Wfunc(x.text, "ECHO :"+result(text_fu), 1)
    master.after(1000, refresh)     


def Wfunc(target, string, panel):
    print("send to:", target, "\nMsg is:", string)
    if panel == 0:
        target = target.get()
        string = string.get(1.0, "end-1c")
    if panel == 1 or panel==0:
               try:
                    group_title = driver.find_element_by_xpath(
                         '//span[@title="' + target + '" and @class="_1wjpf"]')
               except NoSuchElementException:
                    group_search = wait.until(EC.presence_of_element_located(
                         (By.XPATH, '//*[@id="side"]/div[1]/div/label/input')))
                    group_search.send_keys(target)
                    x_arg = '//span[@title="' + target + '"]'
                    print(x_arg)
                    group_title = wait.until(
                         EC.presence_of_element_located((By.XPATH, x_arg)))
               group_title.click()
               print("clicked.........")
               inp_xpath = '//div[@class="_2S1VP copyable-text selectable-text"][@dir="ltr"][@data-tab="1"]'
               input_box = wait.until(EC.presence_of_element_located((
                    By.XPATH, inp_xpath)))
               input_box.send_keys(string)
               bts=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
               bts.click()
    elif  panel==2:
               inp_xpath = '//div[@class="_2S1VP copyable-text selectable-text"][@dir="ltr"][@data-tab="1"]'
               input_box = wait.until(EC.presence_of_element_located((
                    By.XPATH, inp_xpath)))
               input_box.send_keys(string)
               bts=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
               bts.click()




options = webdriver.ChromeOptions()
options.add_argument("user-data-dir="+os.getcwd())
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)
print("started initiation.........")

master = Tk()
master.title("WhatsApp python api")
Label(master, text="Enter the name", width=50).pack()
t1 = Entry(master)
t1.pack()
Label(master, text="Enter the message").pack()
t2 = Text(master)
t2.pack()
Button(master, text='SEND', command=lambda: Wfunc(target=t1, string=t2,panel=0)).pack()
Button(master, text="EXIT", command=master.destroy).pack()
l1 = Label(master, text="NOT UPDATED")
l1.pack()
refresh()


master.mainloop()


driver.close()
