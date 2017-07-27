
# coding: utf-8

# In[35]:

import pandas as pd
import os
from time import gmtime, strftime,localtime
from sqlalchemy import create_engine

# 阿里云数据库
DB_ALI   = create_engine('mysql+mysqlconnector://***************@******************:3306/**', echo=False)
# 本地数据库
DB_ALI   = create_engine('mysql+mysqlconnector://zhoub:zhoub-ses@192.168.2.224:3306/setek_main', encoding='utf-8', echo=False)
EXPORT_PATH='/data1/public/zhoubo/export_users_table/'
if not os.path.exists(EXPORT_PATH):
    EXPORT_PATH='./'

# In[36]:

import re

reg_b = re.compile(r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows ce|xda|xiino", re.I|re.M)
reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M)
def pc_phone(text):
    if text:
        b = reg_b.search(text)
        v = reg_v.search(text)
        if b or v:
            return u'手机'
    return 'pc'


# In[37]:

sql = 'SELECT users.`name`, users.`phone`,p.`district`,users.`ua`, users.`phone_district`, users.`fee`, users.`premium`, FROM_UNIXTIME(users.`created_at`) AS REGIST_T , FROM_UNIXTIME(o.created_at) AS PAY_T FROM `users` LEFT JOIN `order_lists` AS o ON users.id=o.user_id JOIN `profiles` AS p ON users.id=p.user_id WHERE users.id!=211'
df = pd.read_sql(sql, con=DB_ALI)

df['ua']=df['ua'].apply(pc_phone)


# In[38]:

df.to_excel(os.path.join(EXPORT_PATH, 'user-'+strftime("%Y-%m-%d-%H", localtime())+'.xlsx'), encoding='utf8', engine='xlsxwriter')


# In[41]:

# sql = 'SELECT users.`name`, users.`phone`,p.`district`, users.`ua`, users.`phone_district`, users.`fee`, users.`premium`, FROM_UNIXTIME(users.`created_at`) AS REGIST_T , FROM_UNIXTIME(o.created_at) AS PAY_T FROM `users` JOIN `order_lists` AS o ON users.id=o.user_id JOIN `profiles` AS p ON users.id=p.user_id WHERE users.fee>1'
# df = pd.read_sql(sql, con=DB_ALI)

# df['ua']=df['ua'].apply(pc_phone)


# In[42]:

# df.to_excel(os.path.join(EXPORT_PATH, 'premium-user-'+strftime("%Y-%m-%d-%H", gmtime())+'.xlsx'))


# In[ ]:



