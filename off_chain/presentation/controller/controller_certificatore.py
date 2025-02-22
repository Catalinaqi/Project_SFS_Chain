from off_chain.domain.repository.certification_repository import CertificationRepository
from off_chain.domain.repository.company_repository import CompanyRepository
from off_chain.domain.repository.product_repository import ProductRepository
from off_chain.domain.repository.threshold_repository import ThresholdRepository


class ControllerCertificatore:

    # Restituisce il dettaglio del prodotto selezionato dato l'indice n e la lista (filtrata o meno)
    @staticmethod
    def get_dettaglio_prodotto(lista, n):
        pass

    # Assegna un certificato (oppure lo rimuove) al prodotto selezionato di indice n
    @staticmethod
    def certifica(n, azienda, is_certificato=True):
        pass

    # Restituisce la lista di tutte le aziende
    @staticmethod
    def lista_aziende():
        pass

    # Restituisce il dettaglio dell'azienda selezionata dato l'indice n
    @staticmethod
    def get_dettaglio_azienda(id_azienda):
        return CertificationRepository.get_numero_certificazioni(id_azienda)

    # Restituisce tutte le soglie
    @staticmethod
    def lista_soglie():
        pass

    # Restituisce il dettaglio della soglia selezionata dato l'indice n
    @staticmethod
    def get_dettaglio_soglia(n):
        pass

    @staticmethod
    def lista_rivenditori():
        rivenditori = CompanyRepository.get_lista_rivenditori()
        return rivenditori

    @staticmethod
    def certificazione_by_prodotto(id_prodotto):
        certificazione = CertificationRepository.get_certificazione_by_prodotto(id_prodotto)
        return certificazione

    @staticmethod
    def inserisci_certificato(id_prodotto, descrizione, id_azienda_certificatore, data):
        CertificationRepository.inserisci_certificato(id_prodotto, descrizione, id_azienda_certificatore, data)

    # Restituisce la lista di tutti i prodotti finali
    @staticmethod
    def lista_prodotti():
        lista_prodotti = ProductRepository.get_lista_prodotti(ProductRepository.co2_consumata_prodotti)
        return lista_prodotti

    @staticmethod
    def prodotti_by_nome():
        prodotto = ProductRepository.get_prodotti_by_nome(ProductRepository.co2_consumata_prodotti)
        return prodotto

    # Restituisce la lista dei prodotti di un certo rivenditore r
    @staticmethod
    def lista_prodotti_rivenditore():
        lista_prodotti_by_rivenditore = ProductRepository.get_lista_prodotti_by_rivenditore(
            ProductRepository.co2_consumata_prodotti)
        return lista_prodotti_by_rivenditore

    # Restituisce la lista dei prodotti ordinati secondo la co2 consumata
    @staticmethod
    def lista_prodotti_ordinati_co2():
        lista_ordinata = ProductRepository.get_prodotti_ordinati_co2(ProductRepository.co2_consumata_prodotti)
        return lista_ordinata

    # Restituisce la lista dei prodotti certificati
    @staticmethod
    def lista_prodotti_certificati(self):
        lista_prodotti_certificati = self.database.get_prodotti_certificati()
        return lista_prodotti_certificati

    @staticmethod
    def lista_prodotti_certificati_rivenditore(self, r):
        lista = ProductRepository.get_prodotti_certificati_by_rivenditore(r)
        return lista

    @staticmethod
    def lista_prodotti_certificati_ordinata():
        lista = ProductRepository.get_prodotti_certificati_ordinati_co2(ProductRepository.co2_consumata_prodotti)
        return lista

    @staticmethod
    def lista_prodotti_certificati_by_nome(nome):
        lista = ProductRepository.get_prodotti_certificati_by_nome(ProductRepository.co2_consumata_prodotti, nome)
        return lista

    @staticmethod
    def is_certificato(id_prodotto):
        return CertificationRepository.is_certificato(id_prodotto)

    # Restituisce la lista delle operazioni per la produzione del prodotto selezionato
    @staticmethod
    def lista_operazioni_prodotto(id_prodotto):
        lista_operazioni = ProductRepository.get_storico_prodotto(id_prodotto)
        return lista_operazioni

    # Restituisce lo scarto dalla soglia di riferimento
    @staticmethod
    def scarto_soglia(co2, operazione, prodotto):
        soglia = ThresholdRepository.get_soglia_by_operazione_and_prodotto(operazione, prodotto)
        return soglia - float(co2)
