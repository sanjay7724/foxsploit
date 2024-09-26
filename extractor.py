import os
import subprocess
import shutil
import csv
import sqlite3

"""
1) Find the current user
2) check for the user's firefox profiles
3) copy artifacts  and extract information
"""

curr_dir = os.getcwd()


def getuser():
    a = subprocess.Popen(["echo","%USERNAME%"],shell=True,stdout=subprocess.PIPE).stdout.read()
    return a.decode().strip()

def copyfiles(username):
    curr_dir = os.getcwd()
    print(f"Current directory: {curr_dir}")
    FIREFOX_LOCATION = os.path.join("C:\\Users", username, "AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
    print(f"Firefox profile location: {FIREFOX_LOCATION}")
    if not FIREFOX_LOCATION:
        print("Incorrect location")
        return
    
    profiles = os.listdir(FIREFOX_LOCATION)
    if not profiles:
        print("No profiles found...")
        return
    print(profiles)
    
    profile_dir = FIREFOX_LOCATION+"\\"+profiles[0]
    files = os.listdir(profile_dir)
    file_list = ['cookies.sqlite','formhistory.sqlite','places.sqlite']
    for file in files:
        src = profile_dir+"\\"+file
        dest = curr_dir+"\\"+file
        if file in file_list:
            print(file)
            #src = profile_dir+"\\"+file
            print(src)
            #dest = curr_dir+"\\"+file
            print(dest)
            if file in dest:
                os.remove(dest)
                shutil.copy(src,dest)
                print("File copied successfully")
        
            shutil.copy(src,dest)
            
    return

def extract_cookies():
    data = []
    conn = sqlite3.connect('cookies.sqlite')
    cursor = conn.cursor()
    print("Dumping cookies")
    cursor.execute("Select name, value, host, lastAccessed from moz_cookies")
    history = cursor.fetchall()
    for name,value,host,lastAccessed in history:
        details = {"name":name,
                   "value":value,
                   "host":host,
                   "lastAccessed":lastAccessed}
        data.append(details)
        #print(data)
    with open ('cookies.csv','w',newline='') as csvfile:
        fieldnames = ['name','value','host','lastAccessed']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return
    
def extract_formhistory():
    data = []
    conn = sqlite3.connect('formhistory.sqlite')
    cursor = conn.cursor()
    print("Dumping form history")
    cursor.execute("select * from moz_formhistory")
    history = cursor.fetchall()
    for fieldname,value,timesUsed,firstUsed,lastUsed in history:
        details = {
                   "fieldname":fieldname,
                   "value":value,
                   "firstUsed":firstUsed,
                   "lastUsed":lastUsed
                   }
        data.append(details)
    #print(data)
    with open('formhistory.csv','w',newline='') as csv_file:
        fieldname = ['fieldname','value','firstUsed','lastUsed']
        writer = csv.DictWriter(csv_file,fieldnames=fieldname)
        writer.writeheader()
        writer.writerows(data)
    return data
    

def extract_history():
    data = []
    conn = sqlite3.connect('places.sqlite')
    cursor = conn.cursor()
    cursor.execute("""
        select url,title, last_visit_date from moz_places where url is NOT NULL order by last_visit_date desc
    """)
    history = cursor.fetchall()
    for url,title,last_visit_date in history:
        details = {"url":url,
                   "title":title,
                   "last_visit_date":last_visit_date}
        data.append(details)
    #print(data)
    with open('history.csv','w',newline='',encoding='utf-8') as csv_file:
        fieldname = ['url','title','last_visit_date']
        writer = csv.DictWriter(csv_file,fieldnames=fieldname)
        writer.writeheader()
        writer.writerows(data)
    return data
    # os.chdir(dirs[0])
    # os.listdir()
    
    

if __name__ == "__main__":
    banner = """
     ███████████                       █████████            ████            ███   █████   
░░███░░░░░░█                      ███░░░░░███          ░░███           ░░░   ░░███    
 ░███   █ ░   ██████  █████ █████░███    ░░░  ████████  ░███   ██████  ████  ███████  
 ░███████    ███░░███░░███ ░░███ ░░█████████ ░░███░░███ ░███  ███░░███░░███ ░░░███░   
 ░███░░░█   ░███ ░███ ░░░█████░   ░░░░░░░░███ ░███ ░███ ░███ ░███ ░███ ░███   ░███    
 ░███  ░    ░███ ░███  ███░░░███  ███    ░███ ░███ ░███ ░███ ░███ ░███ ░███   ░███ ███
 █████      ░░██████  █████ █████░░█████████  ░███████  █████░░██████  █████  ░░█████ 
░░░░░        ░░░░░░  ░░░░░ ░░░░░  ░░░░░░░░░   ░███░░░  ░░░░░  ░░░░░░  ░░░░░    ░░░░░  
                                              ░███                                    
                                              █████                                   
                                             ░░░░░                                    
    """
    print(banner)
    user = getuser()
    print("[+] Copying files...")
    copyfiles(user)
    print("[+] Extracting history...")
    extract_history()
    print("[+] Extracting form history...")
    extract_formhistory()
    print("[+] Extracting cookies....")
    extract_cookies()
    print("DONE")