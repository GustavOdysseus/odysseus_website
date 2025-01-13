from typing import Any, Dict, Optional

from crewai.memory.memory import Memory


class UserMemory(Memory):
    """
    Classe UserMemory para manipulação de armazenamento e recuperação de memória do usuário.
    Herda da classe Memory e utiliza uma instância de uma classe que
    adere à Storage para armazenamento de dados, especificamente trabalhando com
    instâncias de MemoryItem.
    """

    def __init__(self, crew=None):
        try:
            from crewai.memory.storage.mem0_storage import Mem0Storage
        except ImportError:
            raise ImportError(
                "Mem0 is not installed. Please install it with `pip install mem0ai`."
            )
        storage = Mem0Storage(type="user", crew=crew)
        super().__init__(storage)

    def save(
        self,
        value,
        metadata: Optional[Dict[str, Any]] = None,
        agent: Optional[str] = None,
    ) -> None:
        # TODO: Mudar esta função, pois queremos cuidar do caso em que salvamos as memórias para o usuário
        data = f"Remember the details about the user: {value}"
        super().save(data, metadata)

    def search(
        self,
        query: str,
        limit: int = 3,
        score_threshold: float = 0.35,
    ):
        results = super().search(
            query=query,
            limit=limit,
            score_threshold=score_threshold,
        )
        return results
