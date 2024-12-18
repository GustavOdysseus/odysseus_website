import unittest
from datetime import datetime, timedelta
from calendar_agent import CalendarAgent
import os
from dotenv import load_dotenv

load_dotenv()

class TestCalendarAgent(unittest.TestCase):
    def setUp(self):
        """Setup para cada teste"""
        self.agent = CalendarAgent()
    
    def test_create_event(self):
        """Teste de criação de evento"""
        response = self.agent.process_request(
            "Crie uma reunião amanhã às 14h com título 'Sync do Time' e descrição 'Reunião semanal de sincronização'"
        )
        self.assertIsNotNone(response, "Resposta não deve ser None")
        self.assertNotIn("erro", response.lower(), "Não deveria retornar erro")
        
    def test_find_events_today(self):
        """Teste de busca de eventos para hoje"""
        response = self.agent.process_request("Quais eventos eu tenho hoje?")
        self.assertIsNotNone(response, "Resposta não deve ser None")
        self.assertNotIn("erro", response.lower(), "Não deveria retornar erro")
        
    def test_find_events_next_week(self):
        """Teste de busca de eventos para próxima semana"""
        response = self.agent.process_request("Encontre eventos para a próxima semana")
        self.assertIsNotNone(response, "Resposta não deve ser None")
        self.assertNotIn("erro", response.lower(), "Não deveria retornar erro")
        
    def test_list_calendars(self):
        """Teste de listagem de calendários"""
        response = self.agent.process_request("Mostre meus calendários")
        self.assertIsNotNone(response, "Resposta não deve ser None")
        self.assertNotIn("erro", response.lower(), "Não deveria retornar erro")
        
    def test_delete_event(self):
        """Teste de deleção de evento"""
        # Primeiro criar um evento
        create_response = self.agent.process_request(
            "Crie uma reunião hoje às 15h com título 'Teste de Deleção' e descrição 'Este evento será deletado'"
        )
        self.assertIsNotNone(create_response, "Resposta de criação não deve ser None")
        self.assertNotIn("erro", create_response.lower(), "Não deveria retornar erro na criação")
        
        # Agora tentar deletar
        delete_response = self.agent.process_request("Delete o evento 'Teste de Deleção' de hoje")
        self.assertIsNotNone(delete_response, "Resposta de deleção não deve ser None")
        self.assertNotIn("erro", delete_response.lower(), "Não deveria retornar erro na deleção")
        
    def test_update_event(self):
        """Teste de atualização de evento"""
        # Primeiro criar um evento
        create_response = self.agent.process_request(
            "Crie uma reunião amanhã às 10h com título 'Reunião Original' e descrição 'Descrição original'"
        )
        self.assertIsNotNone(create_response, "Resposta de criação não deve ser None")
        self.assertNotIn("erro", create_response.lower(), "Não deveria retornar erro na criação")
        
        # Agora atualizar
        update_response = self.agent.process_request(
            "Atualize o evento 'Reunião Original' de amanhã para às 11h e mude o título para 'Reunião Atualizada'"
        )
        self.assertIsNotNone(update_response, "Resposta de atualização não deve ser None")
        self.assertNotIn("erro", update_response.lower(), "Não deveria retornar erro na atualização")
        
    def test_error_handling(self):
        """Teste de tratamento de erros"""
        # Tentar criar evento com data inválida
        response = self.agent.process_request("Crie um evento em data_invalida")
        self.assertIn("erro", response.lower(), "Deveria retornar erro para data inválida")
        
        # Tentar deletar evento inexistente
        response = self.agent.process_request("Delete o evento 'Evento Inexistente'")
        self.assertIn("erro", response.lower(), "Deveria retornar erro para evento inexistente")

if __name__ == '__main__':
    unittest.main()
