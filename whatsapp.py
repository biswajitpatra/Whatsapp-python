import os
import string
import time
from tkinter import *
import sqlite3
from spellchecker import SpellChecker
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

selc = []
printable = set(string.printable)

spell=SpellChecker()
#spell.word_frequency.load_text_file('./my_free_text_doc.txt')

conn=sqlite3.connect("details.db")
c=conn.cursor()
c.execute("CREATE TABLE messaging (contact text,message text,io text)")

def result(gstring,contact):
     gstring=gstring.lower()
     c.execute("SELECT * FROM messaging WHERE contact=?",(contact,))
     rows=c.fetchall()
     c.execute("INSERT INTO messaging VALUES (?,?,'i')",(contact,gstring,))
     conn.commit()
     if(len(rows)==0):
        outsto("HI\n I am BIT.\n you can talk to me as BISWAJIT is somewhat busy at this moment",contact)
        return "HI\n I am BIT.\n you can talk to me as BISWAJIT is somewhat busy at this moment"
     
    # if(gstring.lower())
     gss=gstring.split()
     lugss=spell.unknown(gss)
     print(lugss)
     if len(lugss)==0:
          outsto("WORK IN PROGRESS",contact)
          return "work in progress"
     elif len(lugss)>2:
               outsto("Can we talk in simple English\n as i am used to it",contact)
               return "Can we talk in simple English\n as i am used to it" 
     elif len(lugss)<=2 :              
           for x in range(len(gss)):
             if gss[x] in lugss:
               gssx=spell.correction(gss[x])
               if gssx==gss[x]:
                    outsto("Can we talk in simple English\n as i am used to it",contact)
                    return "Can we talk in simple English\n as i am used to it"
               gss[x]=gssx          
           gstring=" ".join(gss)
           outsto("Did u mean \n"+gstring,contact)
           return "Did u mean \n"+gstring


def outsto(msg,contact):
     msg.replace("\n","")
     msg=msg.lower()
     c.execute("INSERT INTO messaging VALUES (?,?,'o')",(contact,msg,))
     conn.commit()


def refresh():
    table_preuser = driver.find_elements(By.XPATH,"//div[@class=\"_9tCEa\"]/div[last()]/div[1]")
    if len(table_preuser)!=0:
      table_preuser=table_preuser[0] 
      #print("title of chat..",table_preuser.get_attribute("class"))
      if table_preuser.get_attribute("class") == "_3_7SH _3DFk6 message-in tail" or table_preuser.get_attribute("class") == "_3_7SH _3DFk6 message-in":
       puser=driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div[1]/div/span').get_attribute("title")
       text_fu=table_preuser.find_elements(By.XPATH,'.//span[@dir="ltr"]')
       if len(text_fu)!=0:
          text_fu=text_fu[0].text
          text_fu = "".join(filter(lambda x: x in printable, text_fu))
          l1["text"] = puser+":"+text_fu
          Wfunc(puser, "BIT : "+result(text_fu,puser), 2)
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
               Wfunc(x.text, "BIT : "+result(text_fu,x.text), 1)
    master.after(500, refresh)     


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
                         EC.element_to_be_clickable((By.XPATH, x_arg)))
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
conn.close()
os.remove("details.db")
print("SUCCESSFULL EXIT")
