# Contexto do Projeto

Este sistema faz parte do projeto Open Source Cara Core Informática, que busca democratizar o acesso à tecnologia para automação de envio de currículos e análise ATS. O envio de e-mails é realizado de forma segura, transparente e educativa, respeitando a privacidade dos usuários e promovendo boas práticas.

# Recomendações de Segurança e Boas Práticas

- Nunca compartilhe sua Senha de App ou credenciais de e-mail com terceiros.
- Utilize contas de e-mail dedicadas para automações, separadas do uso pessoal.
- Mantenha a verificação em duas etapas sempre ativa.
- Revogue senhas de app não utilizadas ou suspeitas.
- Realize testes de envio em ambientes controlados antes de usar em produção.
- Respeite limites de envio para evitar bloqueios e garantir boa reputação do e-mail.

# Configuração de Senha de App para Envio de E-mails via SMTP do Gmail

Para permitir que um aplicativo externo envie e-mails utilizando sua conta Gmail via SMTP (Simple Mail Transfer Protocol), é fundamental utilizar uma "Senha de App" (App Password) em vez da sua senha principal do Gmail. Esta medida de segurança é implementada pelo Google para proteger sua conta, uma vez que o acesso a aplicativos menos seguros foi desativado.

Siga os passos abaixo para configurar a Senha de App e as informações SMTP necessárias:

## Passo 1: Ativar a Verificação em Duas Etapas (2FA) na sua Conta Google

A geração de uma Senha de App exige que a Verificação em Duas Etapas esteja ativa em sua conta Google. Se ainda não estiver, proceda da seguinte forma:

1. Acesse sua Conta Google através do navegador: <https://myaccount.google.com>

2. No menu de navegação lateral esquerdo, selecione a opção "Segurança".

3. Localize a seção "Como você faz login no Google" e clique em "Verificação em duas etapas".

4. Siga as instruções fornecidas para concluir a configuração da Verificação em Duas Etapas. Este processo geralmente requer um dispositivo móvel para verificação.

## Passo 2: Gerar a Senha de App

Após a ativação bem-sucedida da Verificação em Duas Etapas, você poderá gerar a Senha de App específica para seu aplicativo.

1. Retorne à sua Conta Google: <https://myaccount.google.com>

2. No menu de navegação lateral esquerdo, selecione a opção "Segurança".

3. Na seção "Como você faz login no Google", clique em "Senhas de app".

4. Pode ser solicitada uma nova autenticação para confirmar sua identidade.

5. Na tela "Senhas de app":
   - No campo "Selecionar app", escolha a opção "E-mail".
   - No campo "Selecionar dispositivo", selecione "Outro (Nome personalizado)".
   - Insira um nome descritivo para o seu aplicativo (ex: "Sistema de Notificações", "Aplicativo Web") e clique em "Gerar".

6. Uma senha exclusiva de 16 caracteres será exibida em destaque. Esta é a sua Senha de App.

**Atenção:** Copie ou anote esta senha imediatamente. Por motivos de segurança, ela não será exibida novamente após o fechamento desta janela.

## Passo 3: Configurar o Aplicativo com as Credenciais SMTP do Gmail

Com a Senha de App em mãos, utilize-a nas configurações SMTP do seu aplicativo. As configurações padrão para o SMTP do Gmail são as seguintes:

- **Servidor SMTP:** smtp.gmail.com
- **Porta SMTP (para TLS/STARTTLS):** 587 (recomendado para a maioria dos aplicativos modernos)
- **Porta SMTP (para SSL):** 465 (alternativa, mas menos comum atualmente)
- **Nome de Usuário:** Seu endereço de e-mail completo do Gmail (ex: `seu.email@gmail.com`)
- **Senha:** A Senha de App de 16 caracteres gerada no Passo 2.
- **Método de Criptografia/Segurança:** TLS ou SSL (TLS é geralmente preferível ao usar a porta 587).

### Instruções de Configuração no Aplicativo

1. Acesse as configurações de envio de e-mail ou SMTP dentro do seu aplicativo.

2. Preencha os campos correspondentes com as informações detalhadas acima.

3. Salve as configurações e realize um teste de envio de e-mail para confirmar o funcionamento correto da integração.

Ao seguir estes passos, seu aplicativo estará apto a enviar e-mails de forma segura e confiável utilizando sua conta Gmail.