from django.test import TestCase

# Create your tests here.
class ReportsTests(TestCase):
    def testSeEjecutaReporte(self):
        """
            Verificar si se esta ejecutando reporte correcto
        """
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
