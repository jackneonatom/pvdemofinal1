sudo apt update
sudo apt upgrade
sudo apt install nginx
systemctl status nginx
sudo apt install vim
sudo vim /etc/nginx/sites-available/default
cd /var/www/html
ls
sudo chmod 777 /var/www/html/
curl -fsSL https://get.docker.com -o get-docker.sh

sh get-docker.sh
# installing mongodb on standard linux system
docker run --restart=always -d -p 27017:27017 --name mongodb mongo

# install mongo on raspberry pi 3b
sudo docker pull mongo:3.6
sudo docker run -d --name my-mongo -p 27017:27017 mongo:3.6
# ---------------------------------------------------------------------------

sudo docker ps
cat default
cd ~
sudo raspi-config #then change the hostname to whatever you want itsudo -H ./install
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

logout #have to logout to reload node js when installed

nvm install 20
npm install pm2 -g
pm2 start app.py
pm2 monit
python3 --version
pm2 stop app.py
sudo apt install python3-fastapi
sudo apt install python3-motor
python3 app.py
pm2 status
pm2 delete app
pm2 start app.py --interpreter python3
pm2 logs app
pm2 startup  #only need to run once
# startup should then return a path and a command that you need to run to actually do the startup
sudo env PATH=$PATH:/home/demo/.nvm/versions/node/v20.15.0/bin /home/demo/.nvm/versions/node/v20.15.0/lib/node_modules/pm2/bin/pm2 startup systemd -u demo --hp /home/demo
pm2 save


# when CORS policy still wasnt working after putting it in orgins make sure to do a pm2 stop and start again,


# to access database through docker

sudo docker exec -it 30f30a01f072 bash
mongo PVdemo
show dbs
 use PVdemo
 show collections
 db.readings.find()