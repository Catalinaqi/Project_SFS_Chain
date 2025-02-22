import sqlite3

import pyotp
import re
import hashlib

from off_chain.domain.repository.database_repository import DatabaseRepository
from off_chain.domain.repository.company_repository import CompanyRepository
from off_chain.domain.repository.credential_repository import CredentialRepository


class ControllerAutenticazione:

    # Effettua la registrazione
    @staticmethod
    def registrazione(self, username, password, tipo, indirizzo):
        """Tenta di aggiungere un utente, gestendo eventuali errori."""
        try:
            # Genera una chiave segreta per l'autenticazione a due fattori
            secret_key = pyotp.random_base32()

            # Inserisce le credenziali e la chiave segreta nel database
            ControllerAutenticazione.inserisci_credenziali_e_azienda(username, password, tipo, indirizzo, secret_key)
            self.inserisci_credenziali_e_azienda(username, password, tipo, indirizzo, secret_key)

            # Restituisce il successo insieme alla chiave segreta
            return True, "Utente registrato con successo!", secret_key
        except ControllerAutenticazione.PasswordTooShortError as e:
            return False, str(e), None
        except ControllerAutenticazione.PasswordWeakError as e:
            return False, str(e), None

    # Effettua il login
    @staticmethod
    def login(username, password, otp_code=None):
        credenziali = CredentialRepository.get_lista_credenziali()
        if (username, password) not in [(t[1], t[2]) for t in credenziali]:
            return None
        else:
            # Cerca le credenziali dell'utente
            for credenziale in credenziali:
                if credenziale[1] == username and credenziale[2] == password:
                    id_ = credenziale[0]

                    # Recupera l'azienda dell'utente
                    azienda = CredentialRepository.get_azienda_by_id(id_)

                    # Recupera la chiave segreta OTP per questo utente
                    secret_key = credenziale[3]  # Supponiamo che la chiave segreta OTP sia nel campo 3 dell'azienda

                    # Verifica il codice OTP (se presente)
                    if otp_code:
                        totp = pyotp.TOTP(secret_key)
                        if not totp.verify(otp_code):  # Verifica se l'OTP è corretto
                            print('errore')
                            return None  # Se l'OTP non è valido, ritorna None

                    return azienda[0]  # Se le credenziali e l'OTP sono corretti, ritorna l'azienda dell'utente

    class PasswordTooShortError(Exception):
        """Eccezione per password con meno di 8 caratteri"""
        pass

    class PasswordWeakError(Exception):
        """Eccezione per password che non soddisfa i criteri di sicurezza"""
        pass

    class DatabaseError(Exception):
        pass

    class UniqueConstraintError(DatabaseError):
        pass

    @staticmethod
    def validate_password(password):
        """
        Validates the password based on security rules.
        """
        if len(password) < 8:
            raise ControllerAutenticazione.PasswordTooShortError("The password must be at least 8 characters long!")
        if not re.search(r'[A-Z]', password):
            raise ControllerAutenticazione.PasswordWeakError("The password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ControllerAutenticazione.PasswordWeakError("The password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ControllerAutenticazione.PasswordWeakError("The password must contain at least one number.")
        if not re.search(r'\W', password):
            raise ControllerAutenticazione.PasswordWeakError("The password must contain at least one special character (!, @, #, etc.).")

    @staticmethod
    def hash_password(password):
        """
        Hashes the password using SHA-256.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register_credential(username, password, topt_secret):
        """
        Validates password and registers a new credential.
        """
        try:
            ControllerAutenticazione.validate_password(password)
            hashed_password = ControllerAutenticazione.hash_password(password)
            return CredentialRepository.insert_credential(username, hashed_password, topt_secret)
        except Exception as e:
            raise Exception(f"Registration error: {str(e)}")

    @staticmethod
    def inserisci_credenziali_e_azienda(username, password, tipo, indirizzo, secret_key):
        try:
            # Controllo lunghezza password
            if len(password) < 8:
                raise ControllerAutenticazione.PasswordTooShortError("La password deve contenere almeno 8 caratteri!")

            # Controllo complessità con regex
            if not re.search(r'[A-Z]', password):  # Almeno una lettera maiuscola
                raise ControllerAutenticazione.PasswordWeakError("La password deve contenere almeno una lettera maiuscola.")
            if not re.search(r'[a-z]', password):  # Almeno una lettera minuscola
                raise ControllerAutenticazione.PasswordWeakError("La password deve contenere almeno una lettera minuscola.")
            if not re.search(r'[0-9]', password):  # Almeno un numero
                raise ControllerAutenticazione.PasswordWeakError("La password deve contenere almeno un numero.")
            if not re.search(r'\W', password):  # Almeno un carattere speciale
                raise ControllerAutenticazione.PasswordWeakError("La password deve contenere almeno un carattere speciale (!, @, #, etc.).")

            # Avvia la transazione
            # self.cur.execute("BEGIN TRANSACTION;")

            # Inserimento delle credenziali
            try:
                CredentialRepository.insert_credential(username, password, secret_key)
            except sqlite3.IntegrityError:
                raise ControllerAutenticazione.UniqueConstraintError("Errore: Username già esistente.")

            # Recupero dell'ID delle credenziali appena inserite
            id_credenziali = DatabaseRepository.fetch_one("SELECT last_insert_rowid();")[0]

            # Inserimento dell'azienda con l'ID delle credenziali
            CompanyRepository.insert_company(id_credenziali, tipo, username, indirizzo)

            return id_credenziali  # Può essere utile restituire l'ID

        except Exception as e:
            raise Exception(f"Database error: {e}")
