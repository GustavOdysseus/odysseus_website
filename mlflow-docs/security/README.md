# Segurança com MLflow

## Visão Geral

A segurança é um aspecto crítico em projetos de machine learning. Este guia aborda as melhores práticas de segurança ao usar MLflow, incluindo autenticação, autorização, proteção de dados e conformidade.

## Autenticação

### 1. Configuração de Autenticação
```python
# src/security/auth.py
import mlflow
import jwt
import bcrypt
from typing import Dict, Any, Optional

class MLflowAuth:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.secret_key = config['secret_key']
        
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)
        
    def verify_password(
        self,
        password: str,
        hashed: str
    ) -> bool:
        return bcrypt.checkpw(
            password.encode(),
            hashed.encode()
        )
        
    def generate_token(
        self,
        username: str,
        expiration: int = 3600
    ) -> str:
        payload = {
            'username': username,
            'exp': expiration
        }
        return jwt.encode(
            payload,
            self.secret_key,
            algorithm='HS256'
        )
        
    def verify_token(self, token: str) -> Optional[Dict]:
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=['HS256']
            )
        except jwt.InvalidTokenError:
            return None
```

### 2. Integração com SSO
```python
# src/security/sso.py
from oauthlib.oauth2 import WebApplicationClient
import requests
from typing import Dict, Any

class SSOIntegration:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = WebApplicationClient(config['client_id'])
        
    def get_auth_url(self) -> str:
        return self.client.prepare_request_uri(
            self.config['auth_url'],
            redirect_uri=self.config['redirect_uri'],
            scope=['openid', 'email']
        )
        
    def handle_callback(
        self,
        code: str
    ) -> Dict[str, Any]:
        token_url = self.config['token_url']
        
        token_response = requests.post(
            token_url,
            data=self.client.prepare_token_request(
                token_url,
                code=code,
                redirect_uri=self.config['redirect_uri']
            )
        )
        
        return self.client.parse_request_body_response(
            token_response.text
        )
```

## Autorização

### 1. Controle de Acesso
```python
# src/security/acl.py
from typing import Dict, Any, List
import mlflow

class AccessControl:
    def __init__(self):
        self.client = mlflow.tracking.MlflowClient()
        
    def check_permission(
        self,
        user: str,
        resource: str,
        action: str
    ) -> bool:
        # Verificar permissões no banco
        permissions = self._get_user_permissions(user)
        
        return any(
            self._match_permission(p, resource, action)
            for p in permissions
        )
        
    def grant_permission(
        self,
        user: str,
        resource: str,
        action: str
    ):
        # Adicionar permissão
        permission = f"{action}:{resource}"
        self._add_permission(user, permission)
        
    def revoke_permission(
        self,
        user: str,
        resource: str,
        action: str
    ):
        # Remover permissão
        permission = f"{action}:{resource}"
        self._remove_permission(user, permission)
```

### 2. Políticas de Segurança
```python
# src/security/policies.py
from typing import Dict, Any, List
import re

class SecurityPolicy:
    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = rules
        
    def evaluate(
        self,
        context: Dict[str, Any]
    ) -> bool:
        for rule in self.rules:
            if not self._check_rule(rule, context):
                return False
        return True
        
    def _check_rule(
        self,
        rule: Dict[str, Any],
        context: Dict[str, Any]
    ) -> bool:
        condition = rule['condition']
        value = context.get(rule['field'])
        
        if condition == 'equals':
            return value == rule['value']
        elif condition == 'pattern':
            return bool(re.match(rule['value'], str(value)))
        elif condition == 'range':
            return rule['min'] <= value <= rule['max']
            
        return False
```

## Criptografia

### 1. Criptografia de Dados
```python
# src/security/crypto.py
from cryptography.fernet import Fernet
import base64
from typing import Dict, Any

class DataEncryption:
    def __init__(self, key: bytes = None):
        if key is None:
            key = Fernet.generate_key()
        self.fernet = Fernet(key)
        
    def encrypt_value(self, value: str) -> str:
        return self.fernet.encrypt(
            value.encode()
        ).decode()
        
    def decrypt_value(self, encrypted: str) -> str:
        return self.fernet.decrypt(
            encrypted.encode()
        ).decode()
        
    def encrypt_dict(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            key: self.encrypt_value(str(value))
            for key, value in data.items()
        }
        
    def decrypt_dict(
        self,
        data: Dict[str, str]
    ) -> Dict[str, str]:
        return {
            key: self.decrypt_value(value)
            for key, value in data.items()
        }
```

### 2. Proteção de Credenciais
```python
# src/security/credentials.py
from typing import Dict, Any
import keyring
import os

class CredentialManager:
    def __init__(self, service_name: str):
        self.service_name = service_name
        
    def store_credential(
        self,
        username: str,
        password: str
    ):
        keyring.set_password(
            self.service_name,
            username,
            password
        )
        
    def get_credential(
        self,
        username: str
    ) -> str:
        return keyring.get_password(
            self.service_name,
            username
        )
        
    def delete_credential(
        self,
        username: str
    ):
        keyring.delete_password(
            self.service_name,
            username
        )
```

## Proteção de Dados

### 1. Anonimização
```python
# src/security/anonymization.py
import hashlib
import pandas as pd
from typing import List, Dict, Any

class DataAnonymizer:
    def __init__(self, salt: str = None):
        self.salt = salt or os.urandom(16).hex()
        
    def anonymize_value(self, value: str) -> str:
        return hashlib.sha256(
            f"{value}{self.salt}".encode()
        ).hexdigest()
        
    def anonymize_dataframe(
        self,
        df: pd.DataFrame,
        columns: List[str]
    ) -> pd.DataFrame:
        df_copy = df.copy()
        
        for col in columns:
            df_copy[col] = df_copy[col].apply(
                self.anonymize_value
            )
            
        return df_copy
```

### 2. Auditoria
```python
# src/security/audit.py
import logging
from datetime import datetime
from typing import Dict, Any

class SecurityAuditor:
    def __init__(self, log_path: str):
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler(log_path)
        self.logger.addHandler(handler)
        
    def log_access(
        self,
        user: str,
        resource: str,
        action: str,
        success: bool
    ):
        self.logger.info(
            f"Access: user={user} "
            f"resource={resource} "
            f"action={action} "
            f"success={success} "
            f"timestamp={datetime.now()}"
        )
        
    def log_security_event(
        self,
        event_type: str,
        details: Dict[str, Any]
    ):
        self.logger.warning(
            f"Security Event: type={event_type} "
            f"details={details} "
            f"timestamp={datetime.now()}"
        )
```

## Exemplos de Uso

### 1. Configuração de Segurança
```python
# Configurar autenticação
auth_config = {
    'secret_key': 'your-secret-key',
    'token_expiration': 3600
}
auth = MLflowAuth(auth_config)

# Configurar SSO
sso_config = {
    'client_id': 'your-client-id',
    'auth_url': 'https://auth.example.com/oauth',
    'token_url': 'https://auth.example.com/token',
    'redirect_uri': 'http://localhost:5000/callback'
}
sso = SSOIntegration(sso_config)

# Configurar controle de acesso
acl = AccessControl()
acl.grant_permission('user1', 'experiment/123', 'read')
```

### 2. Proteção de Dados
```python
# Criptografar dados sensíveis
encryption = DataEncryption()
sensitive_data = {
    'api_key': 'secret-key',
    'password': 'secret-password'
}
encrypted_data = encryption.encrypt_dict(sensitive_data)

# Anonimizar dados
anonymizer = DataAnonymizer()
df = pd.DataFrame({
    'name': ['John', 'Jane'],
    'email': ['john@example.com', 'jane@example.com']
})
anonymized_df = anonymizer.anonymize_dataframe(
    df,
    ['name', 'email']
)

# Auditar acessos
auditor = SecurityAuditor('security.log')
auditor.log_access(
    'user1',
    'model/123',
    'download',
    True
)
```

## Próximos Passos

1. [Monitoramento Avançado](../monitoring/advanced.md)
2. [Troubleshooting](../troubleshooting/README.md)
3. [Manutenção](../maintenance/README.md)
