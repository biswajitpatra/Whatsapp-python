from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time
from tkinter import *

def Wfunc(target,string):
    target=target.get()
    string=string.get(1.0,"end-1c")
    print("send to:",target,"\nMsg is:",string)
    group_search=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="side"]/div[1]/div/label/input')))        
    group_search.send_keys(target)      
    x_arg = '//span[contains(@title,"' + target + '")]'
    print(x_arg)
    group_title = wait.until(EC.presence_of_element_located(( 
        By.XPATH, x_arg)))
    group_title.click()
    print("clicked.........")
    inp_xpath='//div[@class="_2S1VP copyable-text selectable-text"][@dir="ltr"][@data-tab="1"]'
    input_box = wait.until(EC.presence_of_element_located(( 
        By.XPATH, inp_xpath)))   
    input_box.send_keys(string + Keys.ENTER)
    time.sleep(1)
    input_box.clear()
    

driver = webdriver.Chrome()  
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)
print("started initiation.........")

master=Tk()
master.title("WhatsApp python api")
Label(master,text="Enter the name",width=50).pack()
t1=Entry(master)
t1.pack()
Label(master,text="Enter the message").pack()
t2=Text(master)
t2.pack()
w=Button(master,text='SEND',command=lambda: Wfunc(t1,t2))
w.pack()



master.mainloop()



driver.quit()
