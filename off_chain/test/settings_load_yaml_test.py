import os
import pytest
import yaml
import logging
from off_chain.configuration.log_setting import LogConfig, logger

# ===================== TEST SETUP =====================

def test_log_yaml_exists():
    """Verifica que el archivo logging.yaml exista."""
    assert os.path.exists(LogConfig.LOGGING_CONFIG_PATH), f"Archivo YAML no encontrado: {LogConfig.LOGGING_CONFIG_PATH}"
    logger.info("Archivo logging.yaml encontrado.")

def test_load_yaml_config():
    """Verifica que logging.yaml se cargue correctamente."""
    try:
        with open(LogConfig.LOGGING_CONFIG_PATH, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            assert config, "El archivo logging.yaml está vacío"
            assert "logging" in config, "La clave 'logging' no está en logging.yaml"
            logger.info("Archivo logging.yaml cargado correctamente.")
    except yaml.YAMLError as e:
        logger.error(f"Error al cargar YAML: {str(e)}")
        pytest.fail(f"Error al cargar YAML: {str(e)}")

def test_setup_logger():
    """Verifica que el logger se configure sin errores."""
    try:
        test_logger = LogConfig.setup_logger()
        assert isinstance(test_logger, logging.Logger), "El objeto devuelto no es un logger válido"
        logger.info("Logger configurado correctamente.")
    except Exception as e:
        logger.error(f"Error al configurar logger: {str(e)}")
        pytest.fail(f"Error al configurar logger: {str(e)}")

def test_logger_output(caplog):
    """Verifica que el logger registre un mensaje y contenga className y relativePath."""
    with caplog.at_level(logging.INFO):
        test_logger = LogConfig.setup_logger()
        test_logger.info("Mensaje de prueba")

    log_output = caplog.text
    assert "Mensaje de prueba" in log_output, "El mensaje de prueba no se registró en los logs"
    assert "relativePath" in log_output, "El campo 'relativePath' no aparece en los logs"
    assert "className" in log_output, "El campo 'className' no aparece en los logs"
    logger.info("El mensaje de prueba se registró correctamente en los logs.")

# ===================== RUN TESTS =====================
if __name__ == "__main__":
    pytest.main()
