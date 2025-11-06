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

---

### 4️⃣ Crie o banco de dados e aplique as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6️⃣ Execute o servidor de desenvolvimento

```bash
python manage.py runserver
```

O servidor estará disponível em:  
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---


📘 **Desenvolvido para a disciplina de Engenharia de Software — FEI**