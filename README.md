# LOG-ANALYSIS

Project Overview: In this project, the main operations to be done is to fetch results from a real-time database that gives information about a data. You have to connect to the database and get the information from the server and form into a report.


### Softwares needed:

* Python
* psycopg2
* PostgreSQL

A vagrant managed virtual machine(VM) is used to run the log analysis project which includes the above softwares. 
This will need Vagrant and VirtualBox software installed on your system.

### Setting up the Project:

---->Install Vagrant and VirtualBox.

---->Now you have to add a box in the vagrant which is used to run the project in your repository.

---->You also need to download the data from below link:
	https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
Now extract this file and place it in your repository.

### Starting the Virtual Machine:
->check the vagrant version
$ vagrant -v

->The following two commands would lead to launch the virtual machine
$ vagrant box add ubuntu/trusty-64
$ vagrant init ubuntu/trusty-64

->From your repository, launch the Vagrant Virtual Machine by using the commands:
$ vagrant up

->Now we need to log in using:
$ vagrant ssh

### Set up the database:
->Load the data file in database by using command:
$ psql -d news -f newsdata.sql


### The database includes the tables:

authors table --- information about article authors
articles table --- information about articles
log table --- information about log of each user
Now you have to do the following:


### Project Requirements:
1.What are the most popular three articles of all time?
```
Query1 =("select articles.title,"
           "count(*) as count from   log,"
           "articles where  articles.slug=substr(log.path,length('/article/')+1) "
           "group by articles.title order by count desc  limit 3;") 
```
2.Who are the most popular article authors of all time?
```
Query2 = (" select authors.name, count(*) as Num "
    "from articles, authors,log " 
    "where  articles.slug=substr(log.path,length('/article/')+1) "
    "and authors.id=articles.author "
    "group by authors.name "
    "order by Num desc;")
```
3.On which days did more than 1% of requests lead to errors?

```
Query3 = (" with Num_req AS (select time::date as day, count(*) "
        "from log group by time::date order by time::date), No_Errors as "
        "(select time::date as day, count(*) from log "
        "where status != '200 OK' group by time::date order by time::date), Errors_Rate as "
        "(select Num_req.day, No_Errors.count::float / Num_req.count::float * 100 "
        "as Error_Per from Num_req, No_Errors "
        "where Num_req.day = No_Errors.day)"
        "select * from Errors_Rate where Error_per > 1;")
```

### Run the Program :

Finally, Run the project file in vagrant by using:

vagrant@vagrant-ubuntu-trusty-64:/vagrant$ python LOG_Ananlysis_Project.py
