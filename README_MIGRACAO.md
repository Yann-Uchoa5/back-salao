# Script de Migração do Banco de Dados

## Problema
A estrutura da tabela `clientes` no banco de dados não corresponde ao modelo atual após a refatoração.

## Solução

Execute o script SQL `migrate_db.sql` no seu banco de dados PostgreSQL.

### Opção 1: Via Docker (Recomendado)

```bash
# Copie o script para o container
docker cp migrate_db.sql db-salao:/tmp/migrate_db.sql

# Execute o script
docker exec -i db-salao psql -U postgres -d salao_db < migrate_db.sql
```

### Opção 2: Via psql direto

```bash
psql -h localhost -p 5433 -U postgres -d salao_db -f migrate_db.sql
```

### Opção 3: Via pgAdmin ou outra ferramenta gráfica

1. Abra o pgAdmin ou sua ferramenta preferida
2. Conecte ao banco `salao_db`
3. Abra o arquivo `migrate_db.sql`
4. Execute o script

## O que o script faz:

1. ✅ Adiciona a coluna `caminho_foto` na tabela `clientes` (se não existir)
2. ✅ Remove colunas antigas de procedimento da tabela `clientes`:
   - `data_procedimento`
   - `tipo_procedimento`
   - `qtd_tonalizante`
   - `valor_procedimento`
   - `observacao`
   - `corte`
3. ✅ Cria a tabela `procedimentos` (se não existir)
4. ✅ Cria os índices necessários
5. ✅ Define a foreign key entre `procedimentos` e `clientes`

## ⚠️ ATENÇÃO

- **Se você tem dados importantes na tabela clientes**, faça backup antes de executar o script
- Os dados de procedimentos antigos serão perdidos se estiverem na tabela `clientes`
- Se você quiser migrar dados antigos, será necessário criar um script adicional

## Após executar o script

Reinicie o servidor da aplicação e teste novamente.

