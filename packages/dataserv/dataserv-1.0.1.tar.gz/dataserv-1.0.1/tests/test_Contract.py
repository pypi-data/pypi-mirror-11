import unittest
from dataserv.app import db, app
from dataserv.Contract import Contract


class ContractTest(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_new_contract(self):
        addr = '191GVvAaTRxLmz3rW3nU5jAV1rF186VxQc'
        my_contract = Contract(addr)
        my_contract.new_contract('ba17da75c580a0749b6c3d32', 1024)

        self.assertEqual(my_contract.btc_addr, addr)
        self.assertEqual(my_contract.contract_type, 0)
        self.assertEqual(my_contract.file_hash, '8366600f680255341531972a68f201c9edee89350e6d8c43c2c22a385bf02a60')
        self.assertEqual(my_contract.byte_size, 1024)
        self.assertEqual(my_contract.seed, 'ba17da75c580a0749b6c3d32')

    def test_new_contract2(self):
        addr = '191GVvAaTRxLmz3rW3nU5jAV1rF186VxQc'
        my_contract = Contract(addr)
        my_contract.new_contract()
        self.assertEqual(my_contract.btc_addr, addr)
        self.assertEqual(my_contract.contract_type, 0)
        self.assertEqual(my_contract.byte_size, app.config["BYTE_SIZE"])

    def test_new_contract_json(self):
        addr = '191GVvAaTRxLmz3rW3nU5jAV1rF186VxQc'
        my_contract = Contract(addr)
        my_contract.new_contract('ba17da75c580a0749b6c3d32', 1024)
        json_contract = my_contract.to_json()

        self.assertEqual(json_contract["btc_addr"], addr)
        self.assertEqual(json_contract["contract_type"], 0)
        self.assertEqual(json_contract["file_hash"], '8366600f680255341531972a68f201c9edee89350e6d8c43c2c22a385bf02a60')
        self.assertEqual(json_contract["byte_size"], 1024)
        self.assertEqual(json_contract["seed"], 'ba17da75c580a0749b6c3d32')

    def test_contract_limit(self):
        addr = '191GVvAaTRxLmz3rW3nU5jAV1rF186VxQc'
        con1 = Contract(addr)
        con2 = Contract(addr)
        con3 = Contract(addr)

        self.assertTrue(con1.below_limit())
        self.assertTrue(con1.below_limit(1))
        con1.new_contract('ba17da75c580a0749b6c3d32', 1024)
        self.assertFalse(con2.below_limit(1))
        con2.new_contract('ad797d10dc8e12e8553f370e', 1024)
        con3.new_contract('b780bd4852b8c8a62859a50c', 1024)
        self.assertFalse(con3.below_limit(2000))
        self.assertTrue(con3.below_limit(3073))

        # change config to break limit
        app.config["BYTE_FARMER_MAX"] = 1024
        with self.assertRaises(MemoryError):
            con3.new_contract('b780bd4852b8c8a62859a50c', 1024)

    def test_address_errors(self):
        addr1 = '191GVvAaTRxLmz3rW3nU5jAV1rF186VxQc'
        addr2 = 'notvalidaddress'

        con1 = Contract(addr1)
        con2 = Contract(addr2)

        self.assertRaises(LookupError, con1.new_contract('ba17da75c580a0749b6c3d32', 1024))
        self.assertRaises(ValueError, con2.new_contract('ad797d10dc8e12e8553f370e', 1024))
