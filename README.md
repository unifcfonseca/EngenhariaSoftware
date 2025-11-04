# 🎓 StudyUpp

O **StudyUpp** é uma plataforma desenvolvida na disciplina de **Engenharia de Software**, voltada para centralizar e organizar conteúdos universitários — permitindo o cadastro de alunos e professores, com autenticação e perfis distintos.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.11.9**
- **Django 5.2.7**
- **SQLite3** (banco de dados padrão)
- **Django Template Language (DTL)** para as páginas de login e cadastro

---


## ⚙️ Passo a Passo para Rodar o Projeto

### 1️⃣ Verifique a versão do Python

O projeto utiliza o **Python 3.11.9**.  
Verifique sua versão com o comando:

```bash
python3 --version
```

Se necessário, instale a versão correta antes de prosseguir.

---

### 2️⃣ Crie e ative o ambiente virtual

Na raiz do projeto, execute:

```bash
# Criação do ambiente virtual
python3.11 -m venv .venv

# Ativação (Linux / macOS)
source .venv/bin/activate

# Ativação (Windows)
.venv\Scripts\activate
```

---

### 3️⃣ Instale as dependências

Com o ambiente virtual ativo, instale os pacotes do projeto:

```bash
pip install -r requirements.txt
```

Se o arquivo `requirements.txt` ainda não existir, gere-o com:

```bash
pip freeze > requirements.txt
```

---

### 4️⃣ Crie o banco de dados e aplique as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5️⃣ Crie um superusuário (opcional)

Para acessar o painel administrativo do Django:

```bash
python manage.py createsuperuser
```

---

### 6️⃣ Execute o servidor de desenvolvimento

```bash
python manage.py runserver
```

O servidor estará disponível em:  
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 👥 Funcionalidades Atuais

- Sistema de **cadastro** e **login** de usuários (alunos e professores);
- Validação de e-mail institucional no registro;
- Páginas HTML simples via **Django Template Language**;
- Banco de dados **SQLite3** integrado automaticamente.

---

## 🧩 Próximos Passos

- Implementar upload e gerenciamento de videoaulas;
- Criar tela de pesquisa e filtros por disciplina e instituição;
- Adicionar módulo de estatísticas e visualizações.

---

## 🛠️ Comandos Úteis

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar servidor
python manage.py runserver

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

---

📘 **Desenvolvido para a disciplina de Engenharia de Software — FEI**