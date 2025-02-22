from off_chain.domain.repository.company_repository import CompanyRepository
from off_chain.domain.repository.compensation_repository import CompensationRepository
from off_chain.domain.repository.operation_repository import OperationRepository
from off_chain.domain.repository.product_repository import ProductRepository
from off_chain.domain.repository.threshold_repository import ThresholdRepository


class ControllerAzienda:

    # Restituisce tutte le soglie

    @staticmethod
    def lista_soglie():
        lista_soglie = ThresholdRepository.get_lista_soglie()
        return lista_soglie

    # Restituisce il dettaglio della soglia selezionata dato l'indice n
    @staticmethod
    def get_dettaglio_soglia(n):
        pass

    # Restituisce il dettaglio della co2/il numero di certificati della sua azienda
    @staticmethod
    def get_dettaglio_azienda(id_azienda):
        return CompanyRepository.get_azienda_by_id(id_azienda)

    # Modifica i dati dell sua azienda
    @staticmethod
    def modifica_dati_azienda(azienda):
        pass

    # Restituisce la lista di tutte le azioni compensative della sua azienda
    @staticmethod
    def lista_azioni_compensative(azienda):
        lista_azioni_compensative = CompensationRepository.get_lista_azioni(azienda)
        return lista_azioni_compensative

    # Restituisce la lista delle sue azioni compensative filtrate per data
    @staticmethod
    def lista_azioni_per_data(azienda, d1, d2):
        lista_azioni_per_data = CompensationRepository.get_lista_azioni_per_data(azienda, d1, d2)
        return lista_azioni_per_data

    # Restituisce la lista di tutte le azioni compensative della sua azienda
    @staticmethod
    def lista_azioni_compensative_ordinata(azienda):
        lista_azioni_compensative = CompensationRepository.get_lista_azioni_ordinata(azienda)
        return lista_azioni_compensative

    # Restituisce il dettaglio dell'azione compensativa selezionata
    # dato l'indice n e la lista (filtrata o meno)
    @staticmethod
    def get_dettaglio_azione(n, lista):
        pass

    # Aggiunge un'azione compensativa
    @staticmethod
    def aggiungi_azione(data, azienda, co2_compensata, nome_azione):
        CompensationRepository.inserisci_azione(data, azienda, co2_compensata, nome_azione)

        # Restituisce la lista di tutte le operazioni della sua azienda

    @staticmethod
    def lista_operazioni(azienda):
        lista_operazioni = OperationRepository.get_operazioni_by_azienda(azienda)
        return lista_operazioni

    # Restituisce la lista delle sue operazioni filtrate per data
    @staticmethod
    def lista_operazioni_per_data(self, azienda, d1, d2):
        lista_operazioni = self.database.get_operazioni_by_data(azienda, d1, d2)
        return lista_operazioni

    @staticmethod
    def lista_operazioni_ordinata_co2(azienda):
        lista_operazioni = OperationRepository.get_operazioni_ordinate_co2(azienda)
        return lista_operazioni

    # Restituisce il dettaglio dell'operazione selezionata dato l'indice n e la lista (filtrata o meno)
    @staticmethod
    def get_dettaglio_operazione(n, lista):
        pass

    # Restituisce gli elementi da visualizzare nella combo box
    @staticmethod
    def elementi_combo_box(azienda, operazione, destinatario=''):
        if azienda == "Agricola":
            return ThresholdRepository.get_prodotti_to_azienda_agricola()
        elif azienda == "Trasportatore":
            return ProductRepository.get_prodotti_to_azienda_trasporto(destinatario)
        elif azienda == "Trasformatore":
            return ProductRepository.get_prodotti_to_azienda_trasformazione(operazione)
        elif azienda == "Rivenditore":
            return ProductRepository.get_prodotti_to_rivenditore()

    # Aggiunge un'operazione
    @staticmethod
    def aggiungi_operazione(
            tipo_azienda, azienda, prodotto, data, co2, evento,
            quantita='', nuovo_stato=00, materie_prime=None
    ):
        if tipo_azienda == "Agricola":
            ProductRepository.inserisci_operazione_azienda_agricola(
                prodotto, quantita, azienda, data, co2, evento
            )
        elif tipo_azienda == "Trasportatore":
            OperationRepository.inserisci_operazione_azienda_trasporto(
                azienda, prodotto, data, co2, evento, nuovo_stato
            )
        elif tipo_azienda == "Trasformatore":
            OperationRepository.inserisci_operazione_azienda_trasformazione(
                azienda, prodotto, data, co2, evento, quantita, materie_prime
            )
        elif tipo_azienda == "Rivenditore":
            OperationRepository.inserisci_operazione_azienda_rivenditore(
                azienda, prodotto, data, co2, evento
            )

    # Restituisce le opzioni per la combo box del dialog per la composizione
    @staticmethod
    def get_prodotti_to_composizione(id_azienda):
        lista = ProductRepository.get_prodotti_to_composizione(id_azienda)
        return lista

    # Restituisce lo scarto dalla soglia di riferimento
    @staticmethod
    def scarto_soglia(self, co2, operazione, prodotto):
        soglia = ThresholdRepository.get_soglia_by_operazione_and_prodotto(operazione, prodotto)
        return soglia - float(co2)
