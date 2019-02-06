#!/usr/bin/env python3
import psycopg2


# Most popular three articles of all time
Title1 = (" MOST POPULAR THREE ARTICLES OF ALL THE TIMES")
Query1 = ("select articles.title,"
          "count(*) as count from   log,"
          "articles where  articles.slug=substr(log.path,"
          "length('/article/')+1)"
          "group by articles.title order by count desc  limit 3;")
# Most popular article authors of all time
Title2 = (" MOST POPULAR AUTHORS OF ALL THE TIMES ")
Query2 = (" select authors.name, count(*) as Num "
          "from articles, authors,log "
          "where  articles.slug=substr(log.path,length('/article/')+1) "
          "and authors.id=articles.author "
          "group by authors.name "
          "order by Num desc;")

# Request leads to error
Title3 = (" DAY OF MORE THAN 1% REQUESTS ARE LEADS TO ERROR")
Query3 = (" with Num_req AS (select time::date as day, count(*) "
          "from log group by time::date order by time::date), No_Errors as "
          "(select time::date as day, count(*) from log "
          "where status != '200 OK' group by time::date order by "
          "time::date), Errors_Rate as "
          "(select Num_req.day, No_Errors.count::float / "
          "Num_req.count::float * 100 "
          "as Error_Per from Num_req, No_Errors "
          "where Num_req.day = No_Errors.day)"
          "select * from Errors_Rate where Error_per > 1;")


# Connection to Database
def connection(Database_name="news"):
    # check database connection
    try:
        db_con = psycopg2.connect("dbname={}".format(Database_name))
        cursor = db_con.cursor()
        return db_con, cursor
    except Exception:
        print("Unable to connect to the database")


# getting data from Database
def Read_Query_res(Query):
    # Provide results
    db_con, cursor = connection()
    cursor.execute(Query)
    return cursor.fetchall()
    db_con.close()


def Show_Query_res(Results_query):
    # printing results
    print("\n")
    print("************************************************************")
    print("************************************************************")
    print("--------"+Results_query[1]+"----------")
    print("\n")
    for i, Res in enumerate(Results_query[0]):
        print(
            "\t" + str(i+1) + "." + str(Res[0]) +
            " - " + str(Res[1]) + " views")


def Show_Error_res(Results_query):
    # printing results
    print("\n")
    print("************************************************************")
    print("************************************************************")
    print("----------"+Results_query[1]+"----------")
    print("\n")
    for res in Results_query[0]:
        print("\t"+str(res[0])+" - "+str(res[1]) + "% errors")
        print("\n")

    print("************************************************************")
if __name__ == '__main__':
    # get results
    popular_Articles = Read_Query_res(Query1), Title1
    popular_Authors = Read_Query_res(Query2), Title2
    Error_Days = Read_Query_res(Query3), Title3

    # function call to print result
    Show_Query_res(popular_Articles)
    Show_Query_res(popular_Authors)
    Show_Error_res(Error_Days)
