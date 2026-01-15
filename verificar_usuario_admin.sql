-- Script para verificar e atualizar usuário como admin
-- Execute este script para verificar se seu usuário está marcado como admin

-- 1. Ver todos os usuários e seus status de admin
SELECT id, username, email, is_admin, is_active 
FROM usuarios 
ORDER BY id;

-- 2. Se seu usuário não estiver como admin, execute este comando (substitua 'SEU_USERNAME' pelo seu username):
-- UPDATE usuarios SET is_admin = TRUE WHERE username = 'SEU_USERNAME';

-- 3. Para tornar TODOS os usuários como admin (use com cuidado):
-- UPDATE usuarios SET is_admin = TRUE;

