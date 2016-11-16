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
    
#example JSON recieved: {"userdemand":"Apple"}
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
            query = "SELECT * FROM Companies WHERE Name like \"%" + userquery + "%\""
        else:
            return {'status':'found', 'symbol': str(row[0]), 'name': str(row[1]), 'market': str(row[2])}
        curr.execute(query)
        row = curr.fetchone()
        curr.close()
        if row == None:
            return {'status':'notfound'}
        else:
            return {'status':'found', 'symbol': str(row[0]), 'name': str(row[1]), 'market': str(row[2])}

    return {'status':'notfound'}


run(host='stocksymbolquery-tuggycode.rhcloud.com', port=5000, debug=True)








