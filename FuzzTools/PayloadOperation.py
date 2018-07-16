import sqlite3


def getConnection():
    conn = sqlite3.connect('FUZZ.db')
    return conn


def getPayloadLists():
    ResultLists = []
    conn = getConnection()
    c = conn.cursor()
    cursor = c.execute("SELECT NAME,BODY,PAYLOADTYPE FROM PAYLOAD")
    for row in cursor:
        ResultLists.append({"NAME": row[0], "BODY": row[1], "PAYLOADTYPE": row[2]})
    conn.close()
    return ResultLists

def getPayload(payloadname):
    conn = getConnection()
    cursor = conn.cursor()
    temp = cursor.execute("SELECT NAME,PAYLOADTYPE,BODY FROM PAYLOAD WHERE NAME = ?", (payloadname))
    lists = []
    if len(temp)>0:
        lists= temp[0][2].split('\n')
        conn.close()
        return {'NAME':payloadname,'TYPE':temp[0][1],'BODY':lists}
    else:
        conn.close()
        return None
def UpdatePayload(payloadname, body, TYPE):
    conn = getConnection()
    cursor = conn.cursor()
    temp = cursor.execute("SELECT * FROM PAYLOAD WHERE NAME = ?", (payloadname))
    try:
        if len(temp) > 0:
            cursor.execute("UPDATE PAYLOAD SET BODY = ? , PAYLOADTYPE = type WHERE NAME = ?", (body, TYPE, payloadname))
        else:
            cursor.execute("INSERT INTO PAYLOAD (NAME,BODY,PAYLOADTYPE) VALUES (?,?,?)", (payloadname, body, TYPE))
        conn.commit()
    except Exception as e:
        conn.rollback()
    conn.close()
