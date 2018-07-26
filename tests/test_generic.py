#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : Kyle
# @License : MIT
# @Contact : kairu_madigan@yahoo.co.jp
# @Date    : 2018/07/23 13:54

import logging
import os
import sys
import unittest

from txffpAssistant import decorators
from txffpAssistant import logger as log
from txffpAssistant.handler import generic
from txffpAssistant.handler import auth
from tests import test_data


logger = log.stream_logger(level=logging.DEBUG)
base_dir = os.path.dirname(os.path.abspath(__file__))

class ETCCardHandlerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.etc = generic.ETCCardHandler(logger=logger)
    
    def test_get_cardlist_cardinfo(self):
        with decorators.log_level(self.etc.logger, logging.INFO):
            filepath = os.path.join(base_dir, "html/card_list_company_response.html")
            with open(filepath) as f:
                html = f.read()
            
            cardinfos = self.etc._get_cardlist_cardinfo(html, "COMPANY", 1)
            card_list = [cardinfo for cardinfo in cardinfos]
            self.assertEqual(len(card_list), 16)
    
    def test_get_bind_cardinfo(self):
        filepath = os.path.join(base_dir, "html/cardBinding_company_response.html")
        with open(filepath) as f:
            html = f.read()
        
        cardinfos = self.etc._get_bind_cardinfo(html, "COMPANY", 1)
        self.assertEqual(cardinfos.__class__.__name__, "generator")
        card_list = [cardinfo for cardinfo in cardinfos]
        self.assertEqual(len(card_list), 16)
    
    def test_get_cardlist_case1(self):
        username = test_data.username
        password = test_data.password
        
        authed_session = auth.authenticated_session(username, password, logger=logger)
        etc_event = generic.ETCCardHandler(session=authed_session, logger=logger)
        cardinfos_iter = etc_event.get_cardlist(user_type="COMPANY")
        
        total = 0
        self.assertEqual(cardinfos_iter.__class__.__name__, "generator")
        for page_num, cardinfos in enumerate(cardinfos_iter):
            self.assertEqual(cardinfos.__class__.__name__, "generator")
            for _ in cardinfos:
                total += 1
        self.assertEqual(total, 34)
    
    def test_get_cardlist_case2(self):
        username = test_data.username
        password = test_data.password
        
        authed_session = auth.authenticated_session(username, password, logger=logger)
        etc_event = generic.ETCCardHandler(session=authed_session, logger=logger)
        cardinfos_iter = etc_event.get_cardlist(user_type="PERSONAL")
        
        total = 0
        self.assertEqual(cardinfos_iter.__class__.__name__, "generator")
        for page_num, cardinfos in enumerate(cardinfos_iter):
            self.assertEqual(cardinfos.__class__.__name__, "generator")
            for _ in cardinfos:
                total += 1
        self.assertEqual(total, 2)


class InvoiceRecordTestCase(unittest.TestCase):
    
    def test_get_query_apply_data(self):
        filepath = os.path.join(base_dir, "html/invoiceRecord-queryApply.html")
        with open(filepath) as f:
            html = f.read()
        
        ir = generic.InvoiceRecordHandler(logger=logger)
        record_infos = ir._get_query_apply_data(html, 1, 201805)
        
        self.assertEqual(record_infos.__class__.__name__, "generator")
        record_info_list = [record_info for record_info in record_infos]
        self.assertEqual(len(record_info_list), 3)
    
    def test_get_record_info_case1(self):
        username = test_data.username
        password = test_data.password
        
        authed_session = auth.authenticated_session(username, password, logger=logger)
        
        ir = generic.InvoiceRecordHandler(logger=logger, session=authed_session)
        record_infos = ir.get_record_info(month=201805, **test_data.redorc_data)
        
        self.assertEqual(record_infos.__class__.__name__, "generator")
        record_info_list = [info for rc_info in record_infos for info in rc_info]
        self.assertEqual(len(record_info_list), 3)


class FunctionTestCase(unittest.TestCase):
    
    def test_invpdf_cld_dl(self):
        username = test_data.username
        password = test_data.password
        
        authed_session = auth.authenticated_session(username, password, logger=logger)
        
        response = generic.invpdf_cld_dl(authed_session, **test_data.invpdf_cld_d_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content is not None)

        # with open("tests/download/pdfcld.zip", "wb") as f:
        #     f.write(response.content)
        authed_session.close()
