echo "$(tput setaf 3)$(tput bold)Instale o MySql 5.7$(tput sgr0)"
# https://www.programmersought.com/article/16525413294/
# https://askubuntu.com/questions/172514/how-do-i-uninstall-mysql
# sudo apt install default-libmysqlclient-dev

echo "$(tput setaf 3)$(tput bold)Instale MySql WorkBeanch$(tput sgr0)"
# sudo snap install mysql-workbench-community

echo "$(tput setaf 3)$(tput bold)Instale o postman$(tput sgr0)"
# sudo snap install postman

if [ ! -f venv ];then
  echo "$(tput setaf 3)$(tput bold)Criando venv$(tput sgr0)"
  python3 -m venv venv
  source venv/bin/activate
  pip3 install -r requirements.txt
fi

echo "$(tput setaf 3)$(tput bold)Antes de iniciar a aplicação inicialize o banco de acordo com o README.md$(tput sgr0)"
