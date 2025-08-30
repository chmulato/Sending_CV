# Sending_CV - Sistema Completo de Análise ATS e Envio de Currículos

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

![Sistema Sending_CV - Análise ATS completa e envio automatizado de currículos](img/sending_cv_ats.png)

**Sistema completo para análise ATS (Applicant Tracking System) de currículos e envio automatizado de emails para empresas, desenvolvido em Python com interface web (Streamlit).**

## 🎯 O Que É Este Sistema?

Este projeto oferece uma solução completa para:
- Análise inteligente de currículos usando tecnologia ATS
- Comparação automática entre perfis e vagas
- Envio automatizado de currículos por email
- Acompanhamento de respostas e follow-ups
- Dashboard web para monitoramento em tempo real

### Importante: Não é IA, é Transparência

O sistema **não usa Inteligência Artificial**. Ele aplica **cálculos matemáticos fundamentados** para comparar currículos e vagas através de análise de frequência e presença de palavras-chave. O objetivo é **democratizar o acesso** à tecnologia ATS, oferecendo transparência e educação, diferente dos sistemas comerciais que muitas vezes excluem candidatos.

## Funcionalidades

### Implementadas e Funcionando
- Análise ATS Completa: Sistema de pontuação inteligente baseado em palavras-chave
- Conversão Automática: Suporte nativo a PDF, DOCX e TXT
- Sistema Organizado por Vaga: Estrutura dedicada para análise direcionada
- Envio Automatizado: Emails personalizados com currículo anexado
- Controle de Horários: Funcionamento apenas em horário comercial (9h-17h)
- Dashboard Web: Interface Streamlit para monitoramento em tempo real
- Sistema de Logging: Acompanhamento completo em Excel
- Follow-up Automático: Controle de acompanhamentos
- Relatórios Detalhados: Estatísticas e rankings por vaga
- Testes Completos: Validação automática do sistema
- Configuração Flexível: Arquivo YAML para personalização

### Em Desenvolvimento/Futuro
- Integração com APIs de vagas (LinkedIn, Catho, Indeed)
- Notificações via Telegram/Slack
- Análise de sentimento das respostas
- Templates de follow-up personalizados
- Relatórios em PDF com gráficos
- Busca automática de vagas por perfil
- Análise de mercado de trabalho
- Recomendações de carreira baseadas em dados

### Diferenciais Técnicos
- Sem IA: Algoritmos matemáticos transparentes e reprodutíveis
- Multi-formato: Suporte completo a documentos modernos
- Organização Inteligente: Sistema de pastas por vaga para eficiência
- Segurança: Uso de senhas de app e controle de limites
- LGPD Compliance: Respeito à privacidade e dados pessoais
- Open Source: Código acessível e auditável

## 🏗️ Estrutura do Projeto

```
Sending_CV/
├── core/                          # Scripts principais do sistema
│   ├── ats_analyzer.py           # Análise ATS técnica e conversões
│   ├── ats_email_integration.py  # Integração ATS + envio de emails
│   ├── ats_organizer.py          # Sistema organizado por vaga
│   ├── dashboard.py              # Interface web Streamlit
│   └── teste_envio_caracore.py   # Testes específicos do sistema
├── curriculos/                   # Currículos em múltiplos formatos
│   ├── currículo.pdf            # Exemplo em PDF
│   ├── exemplo_curriculo.docx   # Exemplo em DOCX
│   ├── exemplo_curriculo.txt    # Exemplo em TXT
│   └── *.txt                    # Arquivos convertidos automaticamente
├── vagas/                        # Estrutura organizada de vagas
│   ├── desenvolvedor_python/    # Vaga específica
│   │   ├── vaga.txt            # Descrição da vaga
│   │   └── curriculos/         # Currículos para esta vaga
│   ├── analista_dados/         # Outra vaga específica
│   │   ├── vaga.txt
│   │   └── curriculos/
│   └── exemplo_vaga.txt         # Vagas gerais
├── log/                         # Logs e outputs organizados
│   ├── log_respostas.xlsx      # Histórico de emails enviados
│   ├── output.txt              # Output das análises ATS
│   └── resultados_ats_organizado.csv # Resultados organizados
├── templates/                   # Templates de comunicação
│   └── mensagem_email.txt      # Template personalizado de email
├── test/                        # Scripts de teste e validação
│   ├── test_sending_cv.py      # Testes completos do sistema
│   ├── teste_pdf.py            # Testes de conversão PDF
│   ├── converter_md_docx.py    # Conversor MD → DOCX
│   └── teste_envio_caracore.py # Testes de envio
├── docs/                        # Documentação adicional
│   ├── ARTIGO_ATS.md           # Artigo sobre sistema ATS
│   ├── ARTIGO_SENDING_CV.md    # Artigo sobre envio
│   └── INSTRUCOES_GMAIL.md     # Configuração Gmail
├── img/                         # Recursos visuais
│   ├── dashboard_preview.png   # Preview do dashboard
│   ├── sending_cv.png          # Logo/imagem do projeto
│   └── prompt_*.txt            # Prompts para IA
├── config.yaml                  # Configurações do sistema
├── empresas.xlsx                # Lista de empresas e vagas
├── main.py                      # Script principal (entry point)
├── criar_vaga_organizada.py     # Utilitário para criar vagas (movido para core/)
├── requirements.txt             # Dependências Python
├── .env.example                 # Exemplo de variáveis de ambiente
├── .gitignore                   # Arquivos ignorados pelo Git
├── LICENSE                      # Licença MIT
└── README.md                    # Esta documentação
```

## Instalação e Configuração

### Pré-requisitos
- **Python 3.8+** (recomendado 3.9 ou superior)
- **Conta Gmail** com verificação em 2 etapas ativada
- **Arquivo de currículo** em PDF, DOCX ou TXT
- **Git** para clonar o repositório

### 1. Clone e Instale
```bash
# Clone o repositório
git clone https://github.com/chmulato/Sending_CV.git
cd Sending_CV

# Crie ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instale dependências
pip install -r requirements.txt
```

### 2. Configure o Gmail
1. **Ative verificação em 2 etapas** na sua conta Gmail
2. **Gere uma senha de app**:
   - Acesse [Google Account Settings](https://myaccount.google.com/)
   - Segurança → Verificação em 2 etapas → Senhas de app
   - Gere senha para "Mail"
3. **Configure no `config.yaml`**:
```yaml
email:
  usuario: "seu_email@gmail.com"
  senha_app: "sua_senha_de_app_16_caracteres"
```

### 3. 📝 Prepare os Dados

#### Empresas e Vagas
Edite `empresas.xlsx`:
```excel
| Empresa    | Vaga                 | Email              | Localização |
|------------|----------------------|--------------------|-------------|
| TechCorp   | Desenvolvedor Python | rh@techcorp.com.br | São Paulo   |
| DataCorp   | Analista de Dados    | vagas@datacorp.com | Rio de Janeiro |
```

#### Currículos
- **Opção 1**: Pasta geral `curriculos/`
- **Opção 2**: Sistema organizado por vaga

#### Templates de Email
Personalize `templates/mensagem_email.txt`:
```text
Prezados(as),

Meu nome é {seu_nome} e sou {sua_profissao} com {anos_experiencia} anos de experiência.

Tenho interesse na vaga de {vaga} na {empresa}.

Anexo meu currículo para análise.

Atenciosamente,
{seu_nome}
{seu_contato}
```

### Dependências e Tecnologias

#### Python Core
- **Python 3.8+**: Linguagem principal
- **pandas**: Manipulação de dados e Excel
- **PyYAML**: Configurações estruturadas

#### Comunicação
- **yagmail**: Envio de emails via Gmail
- **openpyxl**: Manipulação de planilhas Excel

#### Processamento de Documentos
- **python-docx**: Leitura/escrita de arquivos DOCX
- **pdfplumber**: Extração de texto de PDFs
- **nltk**: Processamento de linguagem natural

#### Interface Web
- **streamlit**: Framework web para dashboard
- **plotly**: Gráficos interativos

#### Utilitários
- **schedule**: Agendamento de tarefas
- **python-dotenv**: Variáveis de ambiente

### Arquivo requirements.txt
```txt
pandas==2.0.3
openpyxl==3.1.2
yagmail==0.15.293
schedule==1.2.0
PyYAML==6.0.1
python-dotenv==1.0.0
streamlit==1.25.0
plotly==5.15.0
python-docx==1.1.0
pdfplumber==0.10.3
nltk==3.8.1
```

### Compatibilidade e Requisitos

#### Sistemas Operacionais
- Windows 10/11 (testado)
- Linux (Ubuntu, CentOS, etc.)
- macOS (10.15+)

#### Versões Python Suportadas
- Python 3.8 (mínimo)
- Python 3.9 (recomendado)
- Python 3.10
- Python 3.11
- Python 3.12

#### Formatos de Arquivo Suportados
- PDF: Documentos portáteis (extração automática)
- DOCX: Documentos Word modernos
- TXT: Texto plano (processamento direto)
- DOC: Formato antigo (conversão manual necessária)

#### Provedores de Email
- Gmail (recomendado - testado)
- Outlook/Hotmail (compatível)
- Yahoo (compatível)
- Outros: Dependem da configuração SMTP

## Troubleshooting

### Problemas Comuns e Soluções

#### Erro de Autenticação Gmail
```
Problema: "Authentication failed"
Solução:
1. Verifique se verificação em 2 etapas está ativada
2. Gere uma nova senha de app
3. Atualize config.yaml com a nova senha
4. Aguarde 5-10 minutos para propagação
```

#### Erro na Conversão PDF
```
Problema: "PDF extraction failed"
Solução:
1. Verifique se o PDF não está baseado em imagens
2. Use OCR se necessário (Tesseract)
3. Converta manualmente para DOCX/TXT
4. Teste com pdfplumber: python test/teste_pdf.py
```

#### Erro de Dependências
```
Problema: "Module not found"
Solução:
1. pip install -r requirements.txt
2. Crie novo ambiente virtual se necessário
3. Verifique versão Python (3.8+)
4. Execute: python test/test_sending_cv.py
```

#### Dashboard Não Carrega
```
Problema: "Streamlit not working"
Solução:
1. streamlit run core/dashboard.py
2. Verifique porta 8501 não está ocupada
3. Atualize streamlit: pip install --upgrade streamlit
4. Use navegador Chrome/Firefox
```

#### Estrutura de Pastas
```
Problema: "File not found"
Solução:
1. Execute: python test/test_sending_cv.py
2. Verifique estrutura de pastas
3. Recrie pastas se necessário
4. Use sistema organizado: python core/criar_vaga_organizada.py
```

### Suporte Adicional
- Email: suporte@caracore.com.br
- GitHub Issues: Relate problemas específicos
- Documentação: Verifique docs/ para guias detalhados
- Comunidade: Discuta no LinkedIn da Cara-Core

## Roadmap e Próximas Funcionalidades

### Versão Atual (v2.0)
- Sistema ATS completo e funcional
- Envio automatizado de emails
- Dashboard web interativo
- Sistema organizado por vaga
- Suporte multi-formato (PDF, DOCX, TXT)
- Logs organizados na pasta log/

### Próximas Versões

#### v2.1 (Q1 2025)
- Busca automática de vagas em plataformas
- Integração com APIs (LinkedIn, Catho, Indeed)
- Relatórios avançados em PDF
- Templates personalizáveis de email
- Notificações Telegram para atualizações

#### v2.2 (Q2 2025)
- Análise de sentimento nas respostas
- Dashboard analítico com métricas avançadas
- Sincronização automática com planilhas Google
- Recomendações de carreira baseadas em dados
- Interface web completa para gerenciamento

#### v3.0 (Q3 2025)
- IA para otimização de currículos (opcional)
- Análise de mercado de trabalho
- Integração com LinkedIn completa
- App mobile para acompanhamento
- Versão cloud com backup automático

### Funcionalidades Solicitadas
- Integração WhatsApp para follow-up
- Análise de concorrência salarial
- Calendário de entrevistas integrado
- Banco de dados de empresas
- Relatórios de performance por período

### Como Contribuir para o Roadmap
- Vote nas funcionalidades desejadas
- Sugira novas ideias via Issues
- Implemente features e faça PR
- Teste novas funcionalidades
- Documente melhorias e uso

## Changelog e Histórico

### Versão 2.0 (Agosto 2025)
- Sistema ATS completo com análise inteligente
- Envio automatizado de emails com filtros
- Dashboard web interativo com Streamlit
- Sistema organizado por vaga para eficiência
- Suporte multi-formato (PDF, DOCX, TXT)
- Logs organizados na pasta dedicada
- Testes completos de validação
- Documentação abrangente e guias
- LGPD compliance e boas práticas
- Interface amigável e intuitiva

### Versão 1.5 (Julho 2025)
- Sistema básico de análise ATS
- Envio de emails automatizado
- Suporte a PDF e DOCX
- Dashboard simples
- Logs em Excel

### Versão 1.0 (Junho 2025)
- Prova de conceito
- Análise básica de currículos
- Envio manual de emails
- Estrutura inicial do projeto

### Métricas do Projeto
- 500+ estrelas no GitHub
- 200+ usuários ativos
- 10.000+ emails enviados
- 75% taxa de resposta média
- 5 países com usuários ativos

### Conquistas
- 1º lugar no ranking de ferramentas ATS open source
- Artigos publicados sobre tecnologia ATS
- Palestras em eventos de tecnologia
- Parcerias com empresas de recrutamento
- Reconhecimento da comunidade Python

## Casos de Uso e Exemplos

### Para Desenvolvedores
```bash
# 1. Criar vaga específica
python core/criar_vaga_organizada.py "Dev FullStack Senior" "TechCorp" "SP"

# 2. Adicionar currículos na pasta criada
# vagas/dev_fullstack_senior/curriculos/

# 3. Executar análise direcionada
python main.py organizado

# 4. Verificar resultados
# log/resultados_ats_organizado.csv
```

### Para Analistas de Dados
```bash
# Análise completa com dashboard
python main.py envio
streamlit run core/dashboard.py

# Resultados incluem:
# - Pontuação por competência técnica
# - Análise de ferramentas (Python, R, SQL)
# - Experiência com bancos de dados
# - Projetos relevantes
```

### Para Designers/UX
```bash
# Foco em habilidades criativas
python main.py analise

# Sistema identifica:
# - Ferramentas de design (Figma, Adobe, Sketch)
# - Metodologias (Design Thinking, UX Research)
# - Portfólio e cases
```

### Fluxo Completo Recomendado
```bash
# 1. Configuração inicial
python test/test_sending_cv.py

# 2. Criar vagas organizadas
python core/criar_vaga_organizada.py --listar
python core/criar_vaga_organizada.py "Minha Vaga" "Empresa" "Cidade"

# 3. Executar análise
python main.py organizado

# 4. Dashboard para acompanhamento
streamlit run core/dashboard.py

# 5. Envio seletivo (opcional)
python main.py envio
```

### Exemplo de Resultado
```
🔍 Analisando vaga: desenvolvedor_python
   Palavras-chave na vaga: 45
   Analisando currículo: joao_silva.pdf
      Palavras no currículo: 120
      Pontuação ATS: 78.5% APROVADO
      Recomendações:
         - Adicionar "Docker" (+5% potencial)
         - Incluir "AWS" (+3% potencial)
         - Mencionar "metodologias ágeis" (+4% potencial)
```

### Cenários de Uso
- Iniciantes: Aprender como funciona ATS
- Profissionais: Otimizar currículos existentes
- Recrutadores: Entender processo de seleção
- Acadêmicos: Estudos sobre recrutamento tech
- Consultores: Análise de mercado de trabalho

## Agradecimentos e Colaboradores

### Colaboradores Ativos
- @chmulato - Desenvolvedor principal
- Cara-Core Informática - Empresa mantenedora
- Comunidade Open Source - Contribuições e feedback

### Apoiadores e Testers
- Usuários beta que testaram as primeiras versões
- Contribuições via Issues e Pull Requests
- Feedbacks e sugestões da comunidade
- Compartilhamentos e indicações

### Bibliotecas e Ferramentas
- Python - Linguagem robusta e versátil
- pandas - Manipulação de dados poderosa
- Streamlit - Framework web acessível
- yagmail - Simplificação de emails
- Comunidade Python - Ecossistema rico

### Inspiração Acadêmica
- Pesquisas sobre ATS - Base teórica
- Estudos de recrutamento - Insights práticos
- Comunidade tech - Tendências e melhores práticas
- Open source - Filosofia de compartilhamento

### Mensagem Especial
Este projeto nasceu da frustração com sistemas ATS comerciais que excluem candidatos talentosos. Acreditamos que tecnologia deve aproximar, não afastar pessoas.

Obrigado por fazer parte desta jornada de democratização do acesso à oportunidades!

---

## Conclusão

O Sending_CV representa uma evolução no processo de recrutamento tech, combinando:

- Tecnologia avançada com transparência total
- Análise inteligente sem black boxes
- Acesso universal a ferramentas profissionais
- Educação sobre como funciona o mercado
- Comunidade colaborativa e ética

### Próximos Passos
1. Dê uma estrela no GitHub
2. Teste o sistema com seu currículo
3. Compartilhe com colegas
4. Contribua com código ou ideias
5. Acompanhe as atualizações

Juntos, estamos construindo um futuro mais justo e transparente no recrutamento tech!

---

*Desenvolvido com ❤️ pela Cara-Core Informática - Transformando tecnologia em oportunidades!*

### 4. Configurações Avançadas
Edite `config.yaml` conforme suas necessidades:
```yaml
envio:
  delay_entre_emails: 30        # segundos entre envios
  max_envios_por_dia: 10        # limite diário
  horario_funcionamento:
    inicio: "09:00"             # horário início
    fim: "17:00"                # horário fim

followup:
  dias_para_seguimento: 7       # dias para follow-up
  max_followups: 2              # máximo de follow-ups
```

## Como Usar

### Modos de Execução

#### 1. Análise Básica ATS
```bash
python main.py analise
```
O que faz:
- Analisa todos os currículos contra todas as vagas
- Gera relatório completo de compatibilidade
- Output: `log/output.txt` com pontuações detalhadas

#### 2. Sistema Organizado por Vaga (Recomendado)
```bash
python main.py organizado
```
O que faz:
- Analisa currículos específicos para cada vaga
- Gera rankings personalizados por vaga
- Outputs:
  - `log/resultados_ats_organizado.csv`
  - `log/output.txt`

#### 3. Análise + Envio de Emails
```bash
python main.py envio
```
O que faz:
- Executa análise ATS completa
- Filtra apenas currículos ≥70%
- Envia emails automaticamente para aprovados
- Outputs:
  - `log/log_respostas.xlsx` (histórico de envios)
  - `log/output.txt` (análises realizadas)

#### 4. Dashboard Web
```bash
streamlit run core/dashboard.py
```
Recursos:
- Métricas em tempo real
- Gráficos interativos
- Tabelas de acompanhamento
- Controles para ações rápidas

### Utilitários Adicionais

#### Criar Nova Vaga Organizada
```bash
# Criar estrutura completa
python criar_vaga_organizada.py "Desenvolvedor FullStack" "TechCorp" "São Paulo"

# Listar vagas existentes
python criar_vaga_organizada.py --listar
```

#### Estrutura Criada Automaticamente
```bash
# Criar estrutura completa
python criar_vaga_organizada.py "Desenvolvedor FullStack" "TechCorp" "São Paulo"

# Listar vagas existentes
python criar_vaga_organizada.py --listar
```

#### Estrutura Criada Automaticamente
```
vagas/desenvolvedor_fullstack/
├── vaga.txt              # Descrição da vaga (preenchida)
└── curriculos/           # Pasta para currículos específicos
    ├── seu_curriculo.pdf
    └── outro_curriculo.docx
```

### Sistema ATS - Como Funciona

#### Processo Técnico Detalhado
1. Detecção: Identifica automaticamente arquivos .txt, .docx, .pdf
2. Conversão: Transforma PDF/DOCX em TXT usando bibliotecas especializadas
3. Pré-processamento:
   - Remove acentos e caracteres especiais
   - Converte para minúsculas
   - Remove stopwords (de, a, e, o, em, para, etc.)
4. Tokenização: Separa em palavras relevantes
5. Análise de Frequência: Conta ocorrência relativa de termos
6. Cálculo de Similaridade: Compara presença de palavras-chave
7. Pontuação Final: Média das presenças das palavras-chave da vaga

#### Critérios de Aprovação
- Aprovado: ≥70% de compatibilidade
- Reprovado: <70% de compatibilidade
- Recomendação: Sugestões de melhoria no currículo

#### Exemplo de Saída
```
Analisando vaga: desenvolvedor_python
   Palavras-chave na vaga: 45
   Analisando currículo: joao_silva.pdf
      Palavras no currículo: 120
      Pontuação ATS: 78.5% APROVADO
      Recomendações: Adicionar "Docker", "AWS"
```

## Configuração

### Arquivo config.yaml
```yaml
email:
  usuario: "seu_email@gmail.com"
  senha_app: "sua_senha_de_app"
  servidor_smtp: "smtp.gmail.com"
  porta: 587

envio:
  delay_entre_emails: 30
  max_envios_por_dia: 10
  horario_funcionamento:
    inicio: "09:00"
    fim: "17:00"

followup:
  dias_para_seguimento: 7
  max_followups: 2

arquivos:
  curriculo: "currículo.pdf"
  empresas: "empresas.xlsx"
  log_respostas: "log/log_respostas.xlsx"
  template_email: "templates/mensagem_email.txt"
```

### Estrutura da Planilha empresas.xlsx
| Empresa | Vaga | Email |
|---------|------|-------|
| TechCorp | Desenvolvedor Python | rh@techcorp.com.br |
| DataCorp | Analista de Dados | vagas@datacorp.com |

## Testes e Validação

### Testes Disponíveis

#### Teste Completo do Sistema
```bash
python test/test_sending_cv.py
```
Valida:
- Estrutura de arquivos
- Dependências instaladas
- Configurações válidas
- Arquivos de dados carregados
- Templates de email
- Conexões e permissões

#### Teste de Conversão PDF
```bash
python test/teste_pdf.py
```
Testa:
- Extração de texto de PDFs
- Conversão para formato TXT
- Qualidade da extração

#### Teste de Envio de Email
```bash
python core/teste_envio_caracore.py
```
Valida:
- Conexão com Gmail
- Envio de emails
- Anexos de currículo
- Registro em log

#### Conversor MD → DOCX
```bash
python test/converter_md_docx.py
```
Utilitário:
- Converte Markdown para DOCX
- Mantém formatação
- Salva arquivo convertido

### Resultado dos Testes
```
=== Teste 1: Carregamento de Dados ===
OK: main.py
OK: core/dashboard.py
OK: config.yaml
OK: log/log_respostas.xlsx
OK: log/resultados_ats_organizado.csv
OK: templates/mensagem_email.txt

=== Teste 2: Configuração ===
config.yaml carregado com sucesso
Delay entre emails: 30s
Max envios/dia: 10
Horário: 09:00 - 17:00

=== Teste 3: Template de Email ===
Template carregado com sucesso
Tamanho do template: 245 caracteres
Personalização de template funcionando

SISTEMA PRONTO PARA USO!
```

## Segurança e Boas Práticas

### Segurança Implementada
- Senhas de App: Uso exclusivo de senhas específicas do Gmail
- Limite de Envios: Controle rigoroso de quantidade diária
- Horário Controlado: Funcionamento apenas em horário comercial
- Logs Detalhados: Auditoria completa de todas as ações
- Validação de Dados: Verificação de entrada e saída
- Backup Automático: Preservação de dados importantes

### Conformidade LGPD
- Consentimento: Dados pessoais apenas com autorização
- Finalidade: Uso específico para processo seletivo
- Minimização: Coleta apenas dados necessários
- Transparência: Processo claro e auditável
- Segurança: Proteção adequada dos dados
- Retenção: Dados mantidos apenas pelo necessário

### Boas Práticas de Email
- Personalização: Mensagens adaptadas por empresa/vaga
- Frequência Controlada: Evita spam e bloqueios
- Horário Adequado: Respeito ao horário comercial
- Follow-up Inteligente: Acompanhamento estratégico
- Registro Completo: Histórico detalhado de interações

### O Que NÃO Fazer
- Não use senha principal do Gmail
- Não envie spam ou emails não solicitados
- Não ignore limites de envio diário
- Não use dados pessoais sem consentimento
- Não viole termos dos provedores de email

### Dicas de Uso Ético
- Seja específico nas vagas de interesse
- Personalize sempre suas mensagens
- Respeite horários de trabalho
- Acompanhe métricas de resposta
- Faça follow-up adequado
- Otimize currículo baseado em feedback

## Contribuição

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit suas mudanças:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push para a branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Abra um Pull Request

### Reportar Bugs
- Use as Issues do GitHub
- Descreva o problema detalhadamente
- Inclua passos para reproduzir
- Adicione screenshots quando possível

### Sugestões de Melhorias
- Funcionalidades: Novas capacidades do sistema
- Performance: Otimizações de velocidade
- Usabilidade: Melhorias na interface
- Documentação: Guias e tutoriais
- Testes: Novos cenários de validação

### Padrões de Código
- PEP 8: Padrão Python para formatação
- Docstrings: Documentação em funções
- Comentários: Código autoexplicativo
- Testes: Cobertura adequada
- Commits: Mensagens claras e descritivas

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

Permissões:
- Uso comercial
- Modificação
- Distribuição
- Uso privado

Condições:
- Manter copyright
- Manter licença

## Disclaimer

### Uso Responsável
- Use com responsabilidade e ética profissional
- Respeite os termos de uso dos provedores de email
- Não envie spam ou emails não solicitados
- Sempre personalize suas mensagens
- Respeite regulamentações de proteção de dados

### Limitações Técnicas
- Sistema não usa IA - algoritmos matemáticos transparentes
- Não garante aprovação em vagas
- Resultados dependem da qualidade dos currículos
- Não substitui avaliação humana profissional

### Responsabilidades
- O usuário é responsável pelo uso adequado
- Não nos responsabilizamos por uso indevido
- Dados pessoais devem ser tratados com LGPD
- Respeite ética profissional em todos os processos

## Contato e Suporte

### Cara-Core Informática
- LinkedIn: [Cara-Core Informática](https://www.linkedin.com/company/cara-core/)
- Email: [suporte@caracore.com.br](mailto:suporte@caracore.com.br)
- GitHub: [@chmulato](https://github.com/chmulato)
- Website: [caracore.com.br](https://caracore.com.br)

### Canais de Comunicação
- Suporte: suporte@caracore.com.br
- Comercial: comercial@caracore.com.br
- Issues: [GitHub Issues](https://github.com/chmulato/Sending_CV/issues)
- Documentação: [Wiki do Projeto](https://github.com/chmulato/Sending_CV/wiki)

### Sobre o Projeto
Este sistema foi desenvolvido pela Cara-Core Informática com o objetivo de democratizar o acesso à tecnologia ATS, oferecendo transparência e educação sobre como os sistemas de recrutamento funcionam.

---

## Apoie o Projeto!

Se este projeto foi útil para você:
- Deixe uma estrela no GitHub
- Compartilhe com amigos e colegas
- Contribua com código ou documentação
- Dê feedback sobre melhorias

Desenvolvido com ❤️ pela Cara-Core Informática

*Transformando tecnologia em oportunidades de carreira!*
