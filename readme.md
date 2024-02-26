Redirected mongo db from /var/lib to /home/led/MAI/inf_search/mongodb in /etc/mongod.conf
mongod doc https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/


created symlink from /home/led/MAI/inf_search/mongodb to /var/lib/mongodb
and https://stackoverflow.com/questions/9587445/how-to-create-a-link-to-a-directory-on-linux 

sudo service mongodb start

sudo service mongodb status