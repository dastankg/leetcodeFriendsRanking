from config.config_file import load_config, Config
import psycopg2

config: Config = load_config()
conn_string = (f"host={config.db.db_host} dbname={config.db.database} user={config.db.db_username} "
               f"password={config.db.db_password}")


conn = psycopg2.connect(conn_string)



