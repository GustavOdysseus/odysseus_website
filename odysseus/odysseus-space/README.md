# Odysseus Space - CrewAI Visual Interface

Uma interface visual 3D imersiva para gerenciar agentes, tarefas e tripulações do CrewAI em um ambiente espacial interativo.

## Características

- **Visualização 3D Imersiva**: Interface espacial completa com modelos 3D realistas de personagens e ambiente
- **Agentes como Personagens**: Agentes representados como personagens 3D humanoides com animações
- **Tarefas como Módulos Holográficos**: Visualização interativa de tarefas com efeitos holográficos
- **Estação Espacial Central**: Hub central para visualizar e gerenciar a tripulação
- **Efeitos Visuais Avançados**: Bloom, aberração cromática e outros efeitos para maior imersão
- **Interface Responsiva**: Controles intuitivos e informações detalhadas sob demanda

## Tecnologias Utilizadas

- React.js para a interface do usuário
- Three.js (via @react-three/fiber) para renderização 3D
- Jotai para gerenciamento de estado
- TailwindCSS para estilização
- React Spring para animações suaves

## Requisitos

- Node.js 16+
- NPM ou Yarn
- WebGL compatível com navegador moderno

## Instalação

1. Clone o repositório:
```bash
git clone [url-do-repositório]
```

2. Instale as dependências:
```bash
npm install
```

3. Adicione os modelos 3D necessários em `/public/models/` (veja `/public/models/README.md` para detalhes)

4. Inicie o servidor de desenvolvimento:
```bash
npm start
```

## Estrutura do Projeto

```
odysseus-space/
├── public/
│   └── models/          # Modelos 3D (GLB)
├── src/
│   ├── components/
│   │   ├── characters/  # Componentes de personagens
│   │   ├── environment/ # Componentes do ambiente
│   │   └── tasks/       # Componentes de tarefas
│   ├── scenes/          # Cenas principais
│   ├── state/           # Gerenciamento de estado
│   └── styles/          # Estilos CSS
└── package.json
```

## Uso

1. **Visualização de Agentes**:
   - Clique em um agente para ver seus detalhes
   - Observe o status atual e especialidades
   - Interaja com animações e efeitos visuais

2. **Gerenciamento de Tarefas**:
   - Visualize tarefas como módulos holográficos
   - Clique para ver detalhes e progresso
   - Observe conexões entre agentes e tarefas

3. **Navegação**:
   - Use controles orbitais para navegar pelo ambiente
   - Zoom in/out para diferentes perspectivas
   - Interaja com a estação espacial central

## Contribuindo

1. Fork o projeto
2. Crie sua branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE.md para detalhes.

## Agradecimentos

- CrewAI pelo framework incrível
- Comunidade Three.js pelos recursos e inspiração
- Contribuidores de modelos 3D
