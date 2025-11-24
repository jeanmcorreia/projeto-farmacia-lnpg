# API Farmácia LNPG

API RESTful construída com Flask para apoiar o fluxo operacional de uma farmácia: cadastro de clientes e funcionários, controle de estoque via movimentações, gestão de medicamentos e registro de vendas. A aplicação é totalmente stateless e persiste os dados em arquivos CSV, permitindo uma execução simples sem banco de dados tradicional.

## Destaques
- CRUD completo para clientes, funcionários e medicamentos.
- Registro de movimentações de estoque (entradas/saídas) com histórico e vínculo ao funcionário.
- Processamento de vendas com cálculo automático do valor total e itens vinculados.
- Documentação automática via Swagger/OpenAPI disponível em `/docs`.
- Persistência em CSV (`db/`) para facilitar inspeções rápidas dos dados.

## Stack principal
- Python 3.11+ / Flask 3
- Flask-Smorest (rotas, serialização e OpenAPI)
- Marshmallow (schemas e validações)
- CSV “flat files” como camada de armazenamento

## Estrutura do projeto
```
projeto-farmacia-lnpg/
├─ app.py
├─ requirements.txt
├─ db/
│  ├─ clientes.csv
│  ├─ funcionarios.csv
│  ├─ medicamentos.csv
│  ├─ movimentacoes.csv
│  ├─ vendas.csv
│  └─ itens_venda.csv
├─ repositories/      # CRUD genérico para cada CSV
├─ services/          # Regras de negócios e validações
├─ resources/         # Blueprints Flask-Smorest (camada HTTP)
├─ schemas/           # Definições Marshmallow
└─ tests/             # (placeholder para futuros testes automatizados)
```

## Pré-requisitos
- Python 3.11 ou superior
- Pip (instalado junto ao Python)
- (Opcional) Virtualenv para isolar dependências

## Como executar localmente
1. **Clone o repositório**
   ```bash
   git clone https://github.com/<seu-usuario>/projeto-farmacia-lnpg.git
   cd projeto-farmacia-lnpg
   ```
2. **Crie e ative um ambiente virtual**
   - Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - Linux/macOS:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```
4. **Inicialize a API**
   ```bash
   python app.py
   ```
5. **Acesse**
   - API: `http://127.0.0.1:5000`
   - Documentação interativa (Swagger UI): `http://127.0.0.1:5000/docs`

Os CSVs são criados automaticamente na primeira execução (diretório `db/`).

### Importar collection no Postman
1. Inicie a API localmente (`python app.py`).
2. No Postman escolha **Import > Link**.
3. Informe `http://127.0.0.1:5000/openapi.json` e confirme.
4. A collection é criada já com o servidor local configurado a partir do campo `servers` do OpenAPI.

## Documentação da API
A API expõe blueprints independentes. Todos os endpoints retornam e recebem JSON, utilizando os schemas definidos em `schemas/`.

### Clientes (`/clientes`)
| Método | Caminho | Descrição |
| ------ | ------- | --------- |
| GET    | `/` | Lista todos os clientes |
| POST   | `/` | Cria um cliente (campos: `nome`, `cpf`, `telefone`, `email`) |
| GET    | `/<id_cliente>` | Busca por ID |
| PUT    | `/<id_cliente>` | Atualiza registro existente |
| DELETE | `/<id_cliente>` | Remove cliente |

### Funcionários (`/funcionarios`)
| Método | Caminho | Descrição |
| ------ | ------- | --------- |
| GET    | `/` | Lista todos os funcionários |
| POST   | `/` | Cria funcionário (`nome`, `cpf`, `cargo`, `email`) |
| GET    | `/<id_funcionario>` | Detalha um funcionário |
| PUT    | `/<id_funcionario>` | Atualiza funcionário |
| DELETE | `/<id_funcionario>` | Remove funcionário |
| GET    | `/cargo/<cargo>` | Filtra por cargo |

### Medicamentos (`/medicamentos`)
| Método | Caminho | Descrição |
| ------ | ------- | --------- |
| GET    | `/` | Lista medicamentos |
| POST   | `/` | Cria medicamento (`nome`, `fabricante`, `preco_unitario`, `quantidade_estoque`, `validade`) |
| GET    | `/<id_medicamento>` | Busca por ID |
| PUT    | `/<id_medicamento>` | Atualiza medicamento |
| DELETE | `/<id_medicamento>` | Remove medicamento |

### Movimentações (`/movimentacoes`)
| Método | Caminho | Descrição |
| ------ | ------- | --------- |
| GET    | `/` | Lista todas as movimentações registradas |
| POST   | `/` | Registra nova entrada/saída (`id_medicamento`, `tipo`, `quantidade`, `id_funcionario`) |
| GET    | `/<id_medicamento>` | Listagem filtrada por medicamento |

### Vendas (`/vendas`)
| Método | Caminho | Descrição |
| ------ | ------- | --------- |
| GET    | `/` | Lista todas as vendas com itens relacionados |
| POST   | `/` | Registra uma venda (`id_cliente`, `id_funcionario`, `itens[]`) |
| GET    | `/<id_venda>` | Busca detalhes completos da venda |

#### Exemplo de payload `POST /vendas`
```json
{
  "id_cliente": 1,
  "id_funcionario": 3,
  "itens": [
    {"id_medicamento": 10, "quantidade": 2},
    {"id_medicamento": 5, "quantidade": 1}
  ]
}
```
O serviço calcula o preço de cada item no momento da venda e atualiza o estoque automaticamente.

## Convenções e diretórios-chave
- `repositories/*`: lê/escreve diretamente nos CSVs, garantindo cabeçalhos corretos.
- `services/*`: camadas com regras de negócio (geração de IDs, validações extras, cálculos).
- `resources/*`: expõem endpoints HTTP e centralizam handlers/erros.
- `schemas/*`: definem contratos de entrada/saída e alimentam o Swagger.

## Testes

## Contribuições
1. Abra uma issue descrevendo o problema ou feature.
2. Crie um fork e branch temática (`feature/ajuste-x`).
3. Faça commit das alterações e envie um pull request descrevendo o que foi feito e como validar.

---