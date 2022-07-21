

def clear(txt_db):
    txt_db = str(txt_db)
    test = ''
    if len(str(txt_db))>5:
        test += txt_db[0] + txt_db[1] + txt_db[-3] + txt_db[-2] + txt_db[-1]
        if test == "('',)":
            if len(txt_db) > 5:
                clear_txt = ''
                for i in range(2, len(str(txt_db))-3, 1):
                    clear_txt += txt_db[i]
                return clear_txt
        else:
            return txt_db
    else:
        return txt_db