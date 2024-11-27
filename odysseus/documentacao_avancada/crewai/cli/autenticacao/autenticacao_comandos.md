# Autenticação na CLI do CrewAI

## 1. Visão Geral da Autenticação
O CrewAI utiliza Auth0 para autenticação, com um sistema de tokens seguros para gerenciar o acesso aos recursos premium e protegidos.

## 2. Processo de Autenticação
1. Registro/Login via dispositivo (Device Flow)
2. Validação de token JWT
3. Armazenamento seguro de credenciais

## 3. Comandos que Requerem Autenticação

### 3.1 Comandos CrewAI+
Todos os comandos relacionados ao CrewAI+ requerem autenticação prévia:
```bash
crewai deploy create
crewai deploy push
crewai deploy status
crewai deploy logs
crewai deploy remove
crewai deploy list
```

### 3.2 Comandos de Ferramentas
Comandos relacionados ao repositório de ferramentas:
```bash
crewai tool publish
```

## 4. Como Autenticar

### 4.1 Primeiro Acesso
```bash
crewai signup
```
Este comando irá:
1. Gerar um código de dispositivo
2. Abrir o navegador para autenticação
3. Solicitar confirmação do código
4. Armazenar o token de forma segura

### 4.2 Acessos Subsequentes
```bash
crewai login
```
Use este comando para:
- Renovar tokens expirados
- Trocar de conta
- Reautenticar após logout

## 5. Segurança

### 5.1 Armazenamento de Tokens
- Tokens são armazenados de forma criptografada
- Chaves de criptografia são gerenciadas localmente
- Renovação automática de tokens quando necessário

### 5.2 Validação
- Verificação de assinatura JWT
- Validação de audiência
- Verificação de expiração

## 6. Boas Práticas

### 6.1 Gerenciamento de Sessão
- Mantenha seus tokens atualizados
- Use `logout` quando necessário
- Não compartilhe credenciais

### 6.2 Segurança
- Não exponha tokens em logs
- Mantenha seu sistema atualizado
- Use conexões seguras

## 7. Troubleshooting

### 7.1 Problemas Comuns
1. Token Expirado
   - Solução: Execute `crewai login` novamente

2. Falha na Autenticação
   - Verifique sua conexão com internet
   - Confirme as credenciais
   - Tente o processo novamente

3. Erro de Validação
   - Verifique se o horário do sistema está correto
   - Tente renovar o token

### 7.2 Suporte
Para problemas de autenticação:
1. Verifique os logs
2. Consulte a documentação
3. Entre em contato com o suporte do CrewAI+

## 8. Notas Importantes

1. **Tokens**
   - São válidos por tempo limitado
   - Devem ser renovados periodicamente
   - São específicos por dispositivo

2. **Segurança**
   - Nunca compartilhe seus tokens
   - Mantenha suas credenciais seguras
   - Use senhas fortes

3. **Uso**
   - Autentique antes de usar recursos premium
   - Mantenha sua sessão ativa durante operações
   - Faça logout em dispositivos compartilhados
