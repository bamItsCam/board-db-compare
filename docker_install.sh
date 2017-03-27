curl -sSL https://get.docker.com/ | sh
+ sh -c 'sleep 3; yum -y -q install docker-engine'

sudo usermod -aG docker ec2-user

#logout

systemctl enable docker
systemctl start docker