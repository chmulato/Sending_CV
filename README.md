# Sending_CV - Automação de Envio de Currículos

![Preview](img/sending_cv.png)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow.svg)

Um sistema completo para **automatizar o envio de currículos** e **acompanhar respostas** de processos seletivos, desenvolvido em Python com interface web usando Streamlit.

## Funcionalidades

### Implementadas

- **Envio automatizado de emails** com currículo anexado
- **Personalização automática** de mensagens por empresa/vaga
- **Controle de horários** de funcionamento (9h às 17h)
- **Limite diário** de envios para evitar spam
- **Sistema de logging** completo
- **Dashboard web** para monitoramento
- **Controle de follow-up** automático
- **Histórico completo** de interações

### Em Desenvolvimento

- Integração com APIs de vagas (LinkedIn, Catho)
- Notificações via Telegram
- Análise de sentimento das respostas
- Templates de follow-up personalizados
- Relatórios em PDF

## Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **Pandas** - Manipulação de dados Excel
- **YagMail** - Envio de emails via Gmail
- **Schedule** - Agendamento de tarefas
- **Streamlit** - Interface web
- **Plotly** - Gráficos interativos
- **PyYAML** - Configurações

## Pré-requisitos

1. **Python 3.8 ou superior**
2. **Conta Gmail** com senha de app configurada
3. **Arquivo de currículo** em PDF

## Instalação e Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/chmulato/Sending_CV.git
cd Sending_CV
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure suas credenciais

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com seus dados
```

### 4. Configure o Gmail

1. Ative a verificação em 2 etapas
2. Gere uma senha de app específica
3. Use essa senha no arquivo `config.yaml`

### 5. Prepare seus dados

- Adicione empresas no arquivo `empresas.xlsx`
- Coloque seu currículo como `currículo.pdf`
- Personalize o template em `templates/mensagem_email.txt`

## Como Usar

### Modo Interativo

```bash
python main.py
```

### Dashboard Web

```bash
streamlit run dashboard.py
```

### Configuração Manual

Edite o arquivo `config.yaml` conforme suas necessidades:

```yaml
email:
  usuario: "seu_email@gmail.com"
  senha_app: "sua_senha_de_app"

envio:
  max_envios_por_dia: 10
  delay_entre_emails: 30
  
followup:
  dias_para_seguimento: 7
  max_followups: 2
```

## Estrutura do Projeto

```markdown
Sending_CV/
├── main.py                 # Script principal
├── dashboard.py            # Interface Streamlit
├── config.yaml             # Configurações
├── requirements.txt        # Dependências Python
├── .env.example            # Exemplo de variáveis de ambiente
├── currículo.pdf           # Seu currículo (você deve adicionar)
├── empresas.xlsx           # Lista de empresas a contatar
├── log_respostas.xlsx      # Histórico de envios e respostas
├── templates/
│   └── mensagem_email.txt  # Template do email
├── test/
│   ├── __init__.py         # Módulo de testes
│   └── test_sending_cv.py  # Script de testes
└── README.md               # Este arquivo
```

## Dashboard

O dashboard web oferece:

- **Métricas em tempo real** (envios, respostas, taxa de conversão)
- **Gráficos interativos** de acompanhamento
- **Tabelas** com histórico completo
- **Controles** para ações rápidas
- **Filtros** por status e período

![Dashboard do Sending_CV](img/dashboard_preview.png)

## Segurança e Boas Práticas

- Uso de senhas de app (não a senha principal)
- Controle de limite de envios
- Logs detalhados para auditoria
- Configurações em arquivos separados
- Validação de dados de entrada

## Personalização

### Template de Email

Edite `templates/mensagem_email.txt` com suas informações:

```text
Prezados(as) Senhores(as),

Meu nome é {seu_nome}, e tenho {anos_experiencia} anos de experiência...
```

### Dados das Empresas

No arquivo `empresas.xlsx`:

| Empresa | Vaga | Email |
|---------|------|-------|
| TechCorp | Desenvolvedor Python | `rh@techcorp.com` |

## Testes

O projeto inclui um sistema de testes completo na pasta `test/`:

```bash
# Executar todos os testes
python test/test_sending_cv.py

# Verifica:
# - Estrutura de arquivos
# - Dependências instaladas
# - Configurações válidas
# - Carregamento de dados
# - Templates de email
# - Simulação de envios
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Disclaimer

- Use com responsabilidade e respeite os termos de uso dos provedores de email
- Não envie spam ou emails não solicitados
- Sempre personalize suas mensagens
- Respeite a LGPD e outras regulamentações de proteção de dados

## Contato

- **LinkedIn**: [Cara-Core Informática](https://www.linkedin.com/company/cara-core/)
- **Email**: [suporte@caracore.com.br](mailto:suporte@caracore.com.br)
- **GitHub**: [@chmulato](https://github.com/chmulato)

---

**Se este projeto foi útil, deixe uma estrela!**
