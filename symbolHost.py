from bottle import route, run, get, post, request, template

import sqlite3 as lite


#############################
#     LOCAL STORAGE DB      #
#############################

try:
    symbolDB = lite.connect("symbols.db")
except lite.Error as e:
    print("Error %s:" % e.args[0])
    sys.exit(1)
    
#GET request, where ?ask={Query}
@route('/v1/finance/symbolQuery')
def symbolQuery():
    if request.query.ask == "":
        return {'status':'notfound'}

    userquery = request.query.ask
    
    with symbolDB:
        curr = symbolDB.cursor()
        query = "SELECT * FROM Companies WHERE Symbol like \"" + userquery + "\""
        curr.execute(query)
        row = curr.fetchone()
        if row == None:
            query = "SELECT * FROM Companies WHERE SName like \"%" + userquery + "%\""
        else:
            curr.close()
            return {'status':'found', 'symbol': str(row[0]), 'name': str(row[1]), 'market': str(row[2])}
        curr.execute(query)
        rows = curr.fetchall()
        if rows == []:
            userquery = userquery.split()[0]
            query = "SELECT * FROM Companies WHERE SName like \"%" + userquery + "%\""
            curr.execute(query)
            rows2 = curr.fetchall()
            curr.close()
            if rows2 == []:
                return {'status':'notfound'}
            else:
                choices = []
                hashedChoices = {}
                for row in rows2:
                    hashedChoices[row[1]] = row
                    choices.append(row[1])
                chosen = hashedChoices[process.extractOne(userquery, choices, scorer=fuzz.token_sort_ratio)[0]]
                symbol = chosen[0].split()[0]
                return {'status':'found', 'symbol': str(symbol), 'name': str(chosen[1]), 'market': str(chosen[2])}
        else:
            curr.close()
            choices = []
            hashedChoices = {}
            for row in rows:
                hashedChoices[row[1]] = row
                choices.append(row[1])
            chosen = hashedChoices[process.extractOne(userquery, choices, scorer=fuzz.token_sort_ratio)[0]]
            symbol = chosen[0].split()[0]
            return {'status':'found', 'symbol': str(symbol), 'name': str(chosen[1]), 'market': str(chosen[2])}

    return {'status':'notfound'}


run(host='symbolLookup-boat.rhcloud.com', port=208, debug=True)




        



