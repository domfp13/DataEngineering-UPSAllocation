# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Luis Fuentes

from __future__ import annotations
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pyodbc
import urllib
import cx_Oracle

class SQLServerConn():
    """This class returns a SQL Server connection"""
    
    def __init__(self):
        self.server: str = "SPW099SQL12VA\\NODE_A" 
        self.data_base: str = "service"
        self.user_name: str = "web"
        self.password: str = "web00"
        quoted = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER="+self.server+";DATABASE="+self.data_base+";UID="+self.user_name+";PWD="+self.password)
        self.db_instance = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
            
    def sql_to_data(self, sqlText, waybill: str = None, user1: str = None, user2: str = None, carrier: str = None, acct_nbr: str = None) -> list:
        """This method returns a list of dictionaries for a specific sql passover parameter"""
        result = []
        try:
            with self.db_instance.begin() as connection:
                rows = connection.execute(sqlText, waybill = waybill, user1 = user1, user2 = user2, carrier = carrier, acct_nbr = acct_nbr).fetchall()
                for row in rows:
                    result_row = {}
                    for col in row.keys():
                        result_row[str(col)] = str(row[col])
                    result.append(result_row)
        except Exception as e:
            print(e)
        finally: 
            return result

    def __del__(self):
        print("Connection Deleted")

class OracleConnection():
    """This class returns a Oracle Connection"""

    def __init__(self):
        self.server: str = "DW.WORLD"
        self.user_name: str = "SVCCAN_BCH"
        self.password: str = "B67YBCH"
        self.db_instance = cx_Oracle.connect(self.user_name, self.password, self.server)

    def sql_to_data(self, sqlText, dict_values: dict):
        """This method returns a list of tuples for a specific sql passover parameter"""
        result = []
        try:
            cursor = self.db_instance.cursor()
            rows = cursor.execute(sqlText, dict_values).fetchall()
            for row in rows:
                result.append(row)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            return result
    
    def __del__(self):
        print("Connection Deleted")
        self.db_instance.close()


    
    