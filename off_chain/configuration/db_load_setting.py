import os
import yaml


class BbYamlLoadSetting:
    """
    Handles loading configurations from 'db_setting.yaml' and 'log_load_setting.yaml'.
    Ensures proper path resolution for cross-platform compatibility.
    """

    # Define the absolute path to the setting files
    DATABASE_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "db_setting.yaml")

    @staticmethod
    def load_config():
        """
        Reads and loads a YAML configuration file.
        """
        with open(BbYamlLoadSetting.DATABASE_CONFIG_PATH, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)


# ===================== DATABASE CONFIGURATION =====================

# Load database configuration
configDatabase = BbYamlLoadSetting.load_config()

# Define the absolute base directory for the database
BASE_DIR_DB = os.path.abspath(os.path.join(os.path.dirname(__file__), configDatabase["database"]["base_dir"]))
# Construct database file paths
DATABASE_PATH = os.path.normpath(os.path.join(BASE_DIR_DB, configDatabase["database"]["path_database"]))
SQL_FILE_PATH = os.path.normpath(os.path.join(BASE_DIR_DB, configDatabase["database"]["path_sql_file"]))
