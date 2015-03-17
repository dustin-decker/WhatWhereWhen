This file is a work in progress...

get mongo db per http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

sudo apt-get update

sudo apt-get install python python-dev python-pip mongodb-org Flask-BasicAuth Flask-Navigation libffi-dev libssl-dev libxml2-dev libxslt1-dev

sudo service mongod start //should be running


pip install Flask Flask-limiter Flask-flatpages pymongo pyOpenSSL==0.13

UPGRADE ALL PIP
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U


connect to a mongod
mongo //launch shell
show dbs //show db
use apitest1 //connect to/make db
db //shows current db name

db.createUser(
   {
     user: "user",
     pwd: "randomasspassword",
     roles: [ "dbAdmin", "userAdmin" ]
   }
)

db.addUser( {  
			user: "user",
			pwd: "randomasspassword",
            roles: [ "readWrite", "dbAdmin" ]
            } )