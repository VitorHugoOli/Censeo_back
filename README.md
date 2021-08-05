# Censeo
The main purpose of this project is to create an application where teachers and students can evaluate their classes, and through charts, data and suggestions, find the best way to improve their classes. 
 
The application will enable teachers to create classes where they can edit the content. In the end of each class, the students will have access to a few questions, regarding the performance and other class characteristics. Those questions will be treated and analyzed in order to create charts, where teachers will be able to see the weakest and the strongest spots in their classes. Another feature is the suggestion system, that allows teachers to create topics for students to suggest solutions for the next classes.

The app also creates a competitive rank between students, comparing classmates or even the whole institution. This rank will be fed with the answers and suggestions given by the students. Another parameter to evaluate the rank is how fast the students answer the questions after the end of each class. Teachers can also give extra points by the relevance of their suggestions

## Technology and Links

**DataBase Manager**: [MySql](https://www.mysql.com/)  
*Diagram*:[Censeo Diagram](https://drive.google.com/open?id=1TG0wa70fVVKVtDKn0c5IjtpRNCDYjEGH)

**Back end**: [Django](https://www.djangoproject.com/)    
[*Aplication hierarchy*](https://drive.google.com/file/d/1pFeOhQmmYEceoHbMsKbKVEmnUHq6xHZi/view?usp=sharing)  
*End points*:[]()

**Front End**:[Flutter](https://flutter.dev/)  
*mockups*:[Figma](https://www.figma.com/file/Tqbx83SUd99tr2ojksv6a8/Censeo)



## Installation back-end

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the packages.

```bash
./install.sh
```
## Fluxo inicial de criação
- Cria Bd através do script sql na pasta root
- Realizar as migrações no BD
```bash
python manage.py migrate
```
- Create superuser(Matricula e senha)
```bash
python manage.py createsupeeuser
```
No painel administrativos ou pelas rotas criadas no postman
- Create Faculdade
- Create User Prof(Matricula, Senha; O restante será preenchido no primeiro login)
- Create Cursos
- Create Disciplinas
- Create Turma
- Create Prof Has Turma
- Create Dias Fixos
- Create User Aluno(Matricula, Senha; O restante será preenchido no primeiro login)
- Create Aluno Has Turma 

## Configurations

```bash

```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

##

## Considerations
This project was developed with the support of my professor advisor [Daniel Mendes](http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4442975Y6)

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
