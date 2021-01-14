from selenium import webdriver
import time
import datetime
import pyodbc
import pandas as pd

print("PROGRAM START TIME ", datetime.datetime.now())
# store hour for next hour to run if condition
h = 0
# same above
m = 0


# read data from database
def read(conn):
    # open file present in dir name log.txt
    f = open('Log.txt', 'w+')
    print("Read")
    cursor = conn.cursor()
    sql_query0 = pd.read_sql_query('SELECT       (SUM(cast(CPR.WeightPayable As decimal)/1000))  FROM  CMS_Token TKN '
                                   'INNER JOIN      CMS_TokenVariety CTV ON TKN.TokenNO = CTV.Fk_TokenNo INNER JOIN	'
                                   '	Set_Variety SV ON CTV.Fk_Variety = SV.VarietyID INNER JOIN      CMS_CPRHeader '
                                   'CPR ON TKN.TokenNO = CPR.Fk_TokenNo WHERE    (CAST(CPR.CPRDate AS date) <= '
                                   'GETDATE());',
                                   conn)

    sql_query1 = pd.read_sql_query('SELECT count( CMS_GrossWeight.GrossWeight) from CMS_GrossWeight', conn)
    sql_query2 = pd.read_sql_query('SELECT count(CMS_Token.TokenNO) from CMS_Token', conn)
    sql_query3 = pd.read_sql_query('SELECT COUNT( CMS_TareWeight.TareWeight) FROM CMS_TareWeight', conn)
    sql_query4 = pd.read_sql_query(
        'DECLARE @TopOfHour DATETIME; SET @TopOfHour = DATEADD(HOUR, DATEPART(HOUR, GETDATE()), DATEDIFF(DAY, 0, '
        'GETDATE())); SELECT (SUM(cast(CPR.WeightPayable As decimal)/1000))  FROM    CMS_Token TKN INNER JOIN      '
        'CMS_TokenVariety CTV ON TKN.TokenNO = CTV.Fk_TokenNo 	INNER JOIN		Set_Variety SV ON CTV.Fk_Variety = '
        'SV.VarietyID    INNER JOIN      CMS_CPRHeader CPR ON TKN.TokenNO = CPR.Fk_TokenNo WHERE  CPR.CPRDate BETWEEN '
        '  DATEADD(HOUR, -1, @TopOfHour) AND   DATEADD(HOUR, 0, @TopOfHour) ',
        conn)
    IN_YARD = sql_query1 - sql_query3
    OUT_YARD = sql_query2 - sql_query1
    TOTAL_VEHICLE = IN_YARD + OUT_YARD
    f.writelines(f' TODATE =  {str(sql_query0)}')
    f.write('\n')
    f.writelines(f'    ,                         HOURLY = {str(sql_query4)}')
    f.writelines(f'  ,  IN_YARD = {str(IN_YARD)}')
    f.writelines(f'  , OUT_YARD = {str(sql_query2 - sql_query1)}')
    f.writelines(f'  , TOTAL_Bal = {str(TOTAL_VEHICLE)}')

    f.close()


def fix_text_list():
    # read data from file
    f = open('Log.txt', 'r')
    list = f.readlines()

    converted_list = []
    for element in list:
        converted_list.append(element.strip())

    final_list = [i.lstrip('0') for i in converted_list]
    x = float(final_list[1])
    final_list[1] = str(x)
    f.close()
    return final_list


# Make  a connection to sql server
conn = pyodbc.connect(
    "Driver=SQL Server Native Client 11.0;"
    "Server= name;"
    "Database=name;"
    "UID=userid;"
    "PWD=password;"
    "Trusted_Connection=yes"
)

# read(conn)
# conn.close()

while True:
    current_Time = datetime.datetime.now()
    current_Hour = current_Time.hour
    current_Minute = current_Time.minute
    if current_Hour == h + 1:
    # if current_Minute == m + 3:
        print(current_Munite, "Munite")

        # function call for run query
        read(conn)
        # save the QR code Scan one time QR Code then save until logout
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=C:\\Users\\OK\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
        options.add_argument('--profile-directory=Default')

        # Register the drive
        chrome_browser = webdriver.Chrome(executable_path='C:\chromedriver', options=options)
        chrome_browser.get('https://web.whatsapp.com/')
        # Sleep to scan the QR Code
        time.sleep(15)
        # selected username
        user_name = 'Test'

        # Select  the title having user name
        user = chrome_browser.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
        user.click()
        time.sleep(5)

        list = fix_text_list()
        # Typing message into message box
        message_box = chrome_browser.find_element_by_xpath('//div[@class="DuUXI"]')
        message_box.send_keys(list)
        time.sleep(2)
        # Click on send button
        message_box = chrome_browser.find_element_by_xpath('//div[@class="_3qpzV"]')
        message_box.click()

        time.sleep(10)
        # close browser
        chrome_browser.quit()

    h = current_Hour
    #optional
    m = current_Minute
