# M2a Salon - Sistema de Gestão para Salão de Beleza

Aplicação web desenvolvida com Django para gerenciamento de agendamentos, clientes, serviços e profissionais de um salão de beleza.

<details>
<summary><strong>1. Requisitos do Projeto</strong></summary>

- Python 3.12+ (REQUISITO PARA RODAR OS SCRIPTS INICIAIS)
- Ambiente virtual (venv)
- Django 4.2+
- SQLite (padrão)
- Bootstrap 5
- JavaScript
- Faker (para dados fictícios)
</details>

<details>
<summary><strong> 2. Instalação</strong></summary>

```bash
git clone https://github.com/JoonMarion/m2a_salon_test.git
cd m2a_salon_test
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
</details>

<details>
<summary><strong>  3. Configuração</strong></summary>

1. Crie o banco de dados:
```bash
python manage.py migrate
```

2. Crie um superusuário para acessar o admin:
```bash
python manage.py createsuperuser
```
</details>

<details>
<summary><strong> 4. Executando o servidor</strong></summary>

```bash
python manage.py runserver
```

Acesse [http://127.0.0.1:8000](http://127.0.0.1:8000) no navegador.
</details>

<details>
<summary><strong>5. Populando o banco com dados fictícios (opcional)</strong></summary>

Execute o comando:

```bash
python manage.py populate_db
```

Esse comando cria automaticamente:

- 15 tipos de serviços (ex: Corte, Maquiagem, etc)  
- 200 profissionais com especialidades aleatórias  
- 1000 clientes com dados realistas  
- 2000 agendamentos com diferentes status (`scheduled`, `completed`, `canceled`) distribuídos nos últimos 90 dias  

**Tempo de execução estimado**: cerca de **3 minutos e 30 segundos** em um processador **Intel Core i5 de 10ª geração**.

### Personalização

Se quiser alterar a quantidade de agendamentos criados, edite a variável `max_appointments` no script:

```python
max_appointments = 2000  # Altere para a quantidade desejada
```

#### Para alterar outras quantidades:

- **Clientes**:  
  Edite o valor do `range` na criação de clientes:  
  ```python
  for _ in range(1000):  # Altere 1000 para o número desejado
  ```

- **Profissionais**:  
  Edite o valor do `range` na criação de profissionais:  
  ```python
  for _ in range(200):  # Altere 200 para o número desejado
  ```

- **Serviços**:  
  Modifique a lista `service_names` para adicionar, remover ou alterar os serviços disponíveis:  
  ```python
  service_names = [
      'Corte de cabelo', 'Pintura de cabelo', ..., 'Design de sobrancelhas'
  ]
  ```

</details>

<details>
<summary><strong> 6. Autenticação</strong></summary>

- Acesso ao sistema requer login.
- Apenas usuários autenticados conseguem gerenciar dados.
</details>

<details>
<summary><strong> 7. Funcionalidades principais</strong></summary>

- Cadastro e gestão de **clientes**, **profissionais** e **serviços**
- Agendamento de serviços com status (agendado, concluído, cancelado)
- Filtros por data, profissional e status
- Modal dinâmico para criar/editar sem recarregar a página
- Relatórios por período
</details>

<details>
<summary><strong> 8. Estrutura do projeto</strong></summary>

```
.
├── m2a_salon/               
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py

├── m2a_salon_app/            
│   ├── admin.py
│   ├── apps.py
│   ├── autocompletes.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   ├── management/
│   │   └── commands/
│   │       └── populate_db.py
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── templates/
│   │   ├── home.html
│   │   ├── clients/list.html
│   │   ├── professionals/list.html
│   │   ├── services/list.html
│   │   ├── reports/completed_appointments.html
│   │   └── components/
│   │       ├── modal_form.html
│   │       └── modal_confirm_delete.html
│   ├── templatetags/
│   │   └── custom_tags.py
│   └── tests/
│       └── tests.py

├── static/
│   ├── css/
│   │   ├── global.css
│   │   ├── home.css
│   │   ├── professionals.css
│   │   └── sidebar.css
│   └── js/
│       ├── appointment_load_modal.js
│       └── sidebar.js

└── templates/
    └── base.html
```
</details>
