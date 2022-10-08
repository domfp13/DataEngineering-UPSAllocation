from __future__ import annotations
from src.DBConn import SQLServerConn, OracleConnection
from sqlalchemy.sql import text


if __name__ == "__main__":

    sql_s = SQLServerConn()
    sql_o = OracleConnection()
    carrier_code = "PURCO"
    acct_nbr = '8557975'
    s = text("""
                SELECT TOP 100 *
                FROM xref_table
                """)
    result = sql_s.sql_to_data(sqlText=s)  # -> [{'xref_value': 'DEPOT'}]

    print(result)