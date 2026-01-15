-- Script de migração para atualizar a estrutura do banco de dados
-- Execute este script no banco de dados PostgreSQL

-- 1. Adicionar coluna caminho_foto na tabela clientes (se não existir)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'caminho_foto'
    ) THEN
        ALTER TABLE clientes ADD COLUMN caminho_foto VARCHAR;
    END IF;
END $$;

-- 2. Remover colunas antigas de procedimento da tabela clientes (se existirem)
DO $$
BEGIN
    -- Remove data_procedimento
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'data_procedimento'
    ) THEN
        ALTER TABLE clientes DROP COLUMN data_procedimento;
    END IF;
    
    -- Remove tipo_procedimento
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'tipo_procedimento'
    ) THEN
        ALTER TABLE clientes DROP COLUMN tipo_procedimento;
    END IF;
    
    -- Remove qtd_tonalizante
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'qtd_tonalizante'
    ) THEN
        ALTER TABLE clientes DROP COLUMN qtd_tonalizante;
    END IF;
    
    -- Remove valor_procedimento
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'valor_procedimento'
    ) THEN
        ALTER TABLE clientes DROP COLUMN valor_procedimento;
    END IF;
    
    -- Remove observacao (se existir na tabela clientes)
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'observacao'
    ) THEN
        ALTER TABLE clientes DROP COLUMN observacao;
    END IF;
    
    -- Remove corte
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'corte'
    ) THEN
        ALTER TABLE clientes DROP COLUMN corte;
    END IF;
END $$;

-- 3. Criar tabela procedimentos (se não existir)
CREATE TABLE IF NOT EXISTS procedimentos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    data_procedimento DATE NOT NULL,
    tipo_procedimento VARCHAR NOT NULL,
    qtd_tonalizante FLOAT,
    valor_procedimento FLOAT NOT NULL,
    observacao VARCHAR,
    corte BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_cliente FOREIGN KEY (cliente_id) 
        REFERENCES clientes(id) ON DELETE CASCADE
);

-- 4. Criar índices na tabela procedimentos
CREATE INDEX IF NOT EXISTS idx_procedimentos_cliente_id ON procedimentos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_procedimentos_data ON procedimentos(data_procedimento);

-- Verificar estrutura final
SELECT 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns
WHERE table_name = 'clientes'
ORDER BY ordinal_position;

SELECT 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns
WHERE table_name = 'procedimentos'
ORDER BY ordinal_position;

