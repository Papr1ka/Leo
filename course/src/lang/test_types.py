import unittest

from lang_base_types import Boolean, Float, Integer


class TypesTest(unittest.TestCase):
    def test_types(self):
        self.assertEqual(Integer.from_string("0110b").value, 6)
        self.assertEqual(Integer.from_string("1110B").value, 14)

        self.assertEqual(Integer.from_string("1710o").value, 968)
        self.assertEqual(Integer.from_string("171O").value, 121)

        self.assertEqual(Integer.from_string("9DEBAh").value, 646842)
        self.assertEqual(Integer.from_string("1ABH").value, 427)

        self.assertEqual(Integer.from_string("321d").value, 321)
        self.assertEqual(Integer.from_string("123D").value, 123)
        self.assertEqual(Integer.from_string("123213").value, 123213)

        self.assertEqual(Float.from_string("10.5").value, 10.5)
        self.assertEqual(Float.from_string(".5").value, 0.5)
        self.assertEqual(Float.from_string("1.5e2").value, 150)
        self.assertEqual(Float.from_string("1.5e+2").value, 150)
        self.assertEqual(Float.from_string("1.5e-2").value, 0.015)
        self.assertEqual(Float.from_string("1.5E2").value, 150)
        self.assertEqual(Float.from_string("1.5E+2").value, 150)
        self.assertEqual(Float.from_string("1.5E-2").value, 0.015)

        self.assertEqual(Float.from_string(".5e2").value, 50)
        self.assertEqual(Float.from_string(".5e+2").value, 50)
        self.assertEqual(Float.from_string(".5e-2").value, 0.005)
        self.assertEqual(Float.from_string(".5E2").value, 50)
        self.assertEqual(Float.from_string(".5E+2").value, 50)
        self.assertEqual(Float.from_string(".5E-2").value, 0.005)

        self.assertEqual(Integer(1).add(Integer(11)).value, Integer(12).value)
        self.assertEqual(Integer(1).sub(Integer(10)).value, Integer(-9).value)
        self.assertEqual(Integer(5).mul(Integer(10)).value, Integer(50).value)
        self.assertEqual(Integer(5).div(Integer(10)).value, Integer(0).value)

        self.assertEqual(Float(1.5).add(Float(11.5)).value, Float(13.).value)
        self.assertEqual(Float(1.5).sub(Float(10.)).value, Float(-8.5).value)
        self.assertEqual(Float(1.2).mul(Float(5.)).value, Float(6.).value)
        self.assertEqual(Float(5.).div(Float(10.)).value, Float(0.5).value)

        self.assertEqual(Integer(10).or_(Integer(10)).value, True)
        self.assertEqual(Integer(10).or_(Integer(0)).value, True)
        self.assertEqual(Integer(0).or_(Integer(10)).value, True)
        self.assertEqual(Integer(0).or_(Integer(0)).value, False)

        self.assertEqual(Integer(10).and_(Integer(10)).value, True)
        self.assertEqual(Integer(10).and_(Integer(0)).value, False)
        self.assertEqual(Integer(0).and_(Integer(10)).value, False)
        self.assertEqual(Integer(0).and_(Integer(0)).value, False)

        self.assertEqual(Integer(10).not_().value, False)
        self.assertEqual(Integer(0).not_().value, True)

        self.assertEqual(Float(10.).or_(Float(10.)).value, True)
        self.assertEqual(Float(10.).or_(Float(0.)).value, True)
        self.assertEqual(Float(0.).or_(Float(10.)).value, True)
        self.assertEqual(Float(0.).or_(Float(0.)).value, False)

        self.assertEqual(Float(10.).and_(Float(10.)).value, True)
        self.assertEqual(Float(10.).and_(Float(0.)).value, False)
        self.assertEqual(Float(0.).and_(Float(10.)).value, False)
        self.assertEqual(Float(0.).and_(Float(0.)).value, False)

        self.assertEqual(Float(10.).not_().value, False)
        self.assertEqual(Float(0.).not_().value, True)

        self.assertEqual(Integer(10).or_(Boolean(True)).value, True)
        self.assertEqual(Integer(10).or_(Boolean(False)).value, True)
        self.assertEqual(Integer(0).or_(Boolean(True)).value, True)
        self.assertEqual(Integer(0).or_(Boolean(False)).value, False)

        self.assertEqual(Integer(10).and_(Boolean(True)).value, True)
        self.assertEqual(Integer(10).and_(Boolean(False)).value, False)
        self.assertEqual(Integer(0).and_(Boolean(True)).value, False)
        self.assertEqual(Integer(0).and_(Boolean(False)).value, False)

        self.assertEqual(Float(10.).or_(Boolean(True)).value, True)
        self.assertEqual(Float(10.).or_(Boolean(False)).value, True)
        self.assertEqual(Float(0.).or_(Boolean(True)).value, True)
        self.assertEqual(Float(0.).or_(Boolean(False)).value, False)

        self.assertEqual(Float(10.).and_(Boolean(True)).value, True)
        self.assertEqual(Float(10.).and_(Boolean(False)).value, False)
        self.assertEqual(Float(0.).and_(Boolean(True)).value, False)
        self.assertEqual(Float(0.).and_(Boolean(False)).value, False)

        self.assertEqual(Boolean(True).or_(Boolean(True)).value, True)
        self.assertEqual(Boolean(True).or_(Boolean(False)).value, True)
        self.assertEqual(Boolean(False).or_(Boolean(True)).value, True)
        self.assertEqual(Boolean(False).or_(Boolean(False)).value, False)

        self.assertEqual(Boolean(True).and_(Boolean(True)).value, True)
        self.assertEqual(Boolean(True).and_(Boolean(False)).value, False)
        self.assertEqual(Boolean(False).and_(Boolean(True)).value, False)
        self.assertEqual(Boolean(False).and_(Boolean(False)).value, False)

        self.assertEqual(Integer(10).neq(Integer(11)).value, True)
        self.assertEqual(Float(10.).neq(Float(11.)).value, True)
        self.assertEqual(Boolean(True).neq(Boolean(False)).value, True)
        self.assertEqual(Integer(10).neq(Integer(10)).value, False)
        self.assertEqual(Float(10.).neq(Float(10.)).value, False)
        self.assertEqual(Boolean(True).neq(Boolean(True)).value, False)

        self.assertEqual(Integer(10).eq(Integer(11)).value, False)
        self.assertEqual(Float(10.).eq(Float(11.)).value, False)
        self.assertEqual(Boolean(True).eq(Boolean(False)).value, False)
        self.assertEqual(Integer(10).eq(Integer(10)).value, True)
        self.assertEqual(Float(10.).eq(Float(10.)).value, True)
        self.assertEqual(Boolean(True).eq(Boolean(True)).value, True)

        self.assertEqual(Integer(10).lt(Integer(11)).value, True)
        self.assertEqual(Float(10.).lt(Float(11.)).value, True)
        self.assertEqual(Boolean(False).lt(Boolean(True)).value, True)
        self.assertEqual(Integer(10).lt(Integer(10)).value, False)
        self.assertEqual(Float(10.).lt(Float(10.)).value, False)
        self.assertEqual(Boolean(True).lt(Boolean(True)).value, False)
        self.assertEqual(Integer(10).lt(Integer(9)).value, False)
        self.assertEqual(Float(10.).lt(Float(9.)).value, False)
        self.assertEqual(Boolean(True).lt(Boolean(False)).value, False)

        self.assertEqual(Integer(10).gt(Integer(11)).value, False)
        self.assertEqual(Float(10.).gt(Float(11.)).value, False)
        self.assertEqual(Boolean(False).gt(Boolean(True)).value, False)
        self.assertEqual(Integer(10).gt(Integer(10)).value, False)
        self.assertEqual(Float(10.).gt(Float(10.)).value, False)
        self.assertEqual(Boolean(True).gt(Boolean(True)).value, False)
        self.assertEqual(Integer(11).gt(Integer(10)).value, True)
        self.assertEqual(Float(11.).gt(Float(10.)).value, True)
        self.assertEqual(Boolean(True).gt(Boolean(False)).value, True)

        self.assertEqual(Integer(10).lte(Integer(11)).value, True)
        self.assertEqual(Float(10.).lte(Float(11.)).value, True)
        self.assertEqual(Boolean(False).lte(Boolean(True)).value, True)
        self.assertEqual(Integer(10).lte(Integer(10)).value, True)
        self.assertEqual(Float(10.).lte(Float(10.)).value, True)
        self.assertEqual(Boolean(True).lte(Boolean(True)).value, True)
        self.assertEqual(Integer(11).lte(Integer(10)).value, False)
        self.assertEqual(Float(11.).lte(Float(10.)).value, False)
        self.assertEqual(Boolean(True).lte(Boolean(False)).value, False)

        self.assertEqual(Integer(10).gte(Integer(11)).value, False)
        self.assertEqual(Float(10.).gte(Float(11.)).value, False)
        self.assertEqual(Boolean(False).gte(Boolean(True)).value, False)
        self.assertEqual(Integer(10).gte(Integer(10)).value, True)
        self.assertEqual(Float(10.).gte(Float(10.)).value, True)
        self.assertEqual(Boolean(True).gte(Boolean(True)).value, True)
        self.assertEqual(Integer(11).gte(Integer(10)).value, True)
        self.assertEqual(Float(11.).gte(Float(10.)).value, True)
        self.assertEqual(Boolean(True).gte(Boolean(False)).value, True)


if __name__ == '__main__':
    unittest.main()
