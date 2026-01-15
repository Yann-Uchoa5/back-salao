-- Script para corrigir a tabela clientes removendo colunas antigas
-- Execute este script no banco de dados PostgreSQL

-- 1. Verificar quais colunas existem atualmente
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'clientes'
ORDER BY ordinal_position;

-- 2. Remover colunas antigas de procedimento (se existirem)
DO $$
BEGIN
    -- Remove data_procedimento
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'data_procedimento'
    ) THEN
        ALTER TABLE clientes DROP COLUMN data_procedimento;
        RAISE NOTICE 'Coluna data_procedimento removida';
    END IF;
    
    -- Remove tipo_procedimento
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'tipo_procedimento'
    ) THEN
        ALTER TABLE clientes DROP COLUMN tipo_procedimento;
        RAISE NOTICE 'Coluna tipo_procedimento removida';
    END IF;
    
    -- Remove qtd_tonalizante
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'qtd_tonalizante'
    ) THEN
        ALTER TABLE clientes DROP COLUMN qtd_tonalizante;
        RAISE NOTICE 'Coluna qtd_tonalizante removida';
    END IF;
    
    -- Remove valor_procedimento
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'valor_procedimento'
    ) THEN
        ALTER TABLE clientes DROP COLUMN valor_procedimento;
        RAISE NOTICE 'Coluna valor_procedimento removida';
    END IF;
    
    -- Remove observacao (se existir na tabela clientes)
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'observacao'
    ) THEN
        ALTER TABLE clientes DROP COLUMN observacao;
        RAISE NOTICE 'Coluna observacao removida';
    END IF;
    
    -- Remove corte
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'corte'
    ) THEN
        ALTER TABLE clientes DROP COLUMN corte;
        RAISE NOTICE 'Coluna corte removida';
    END IF;
END $$;

-- 3. Garantir que caminho_foto existe e é nullable
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'clientes' AND column_name = 'caminho_foto'
    ) THEN
        ALTER TABLE clientes ADD COLUMN caminho_foto VARCHAR;
        RAISE NOTICE 'Coluna caminho_foto adicionada';
    ELSE
        -- Garantir que é nullable
        ALTER TABLE clientes ALTER COLUMN caminho_foto DROP NOT NULL;
        RAISE NOTICE 'Coluna caminho_foto já existe e foi garantida como nullable';
    END IF;
END $$;

-- 4. Verificar estrutura final
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'clientes'
ORDER BY ordinal_position;

