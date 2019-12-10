import unittest
from db_facts.db_facts import DbFacts
from unittest.mock import patch, MagicMock
import pandas as pd


class TestDbFacts(unittest.TestCase):
    @patch('db_facts.db_facts.util')
    @patch('db_facts.db_facts.sql')
    def test_run(self, mock_sql, mock_util):
        # the unaltered, original dataframe for testing
        test_input = pd.DataFrame.from_dict({
            'id': [0],
            'score': [1]
            })

        # the expected dataframe after transformation
        test_output = pd.DataFrame.from_dict({
            'id': [0],
            'score': [2]
            })

        job_context = MagicMock()
        mock_engine = MagicMock()

        job_context.get_default_db_engine.return_value = mock_engine
        mock_sql.read_sql.return_value = test_input

        job = DbFacts(job_context)
        mock_write = mock_util.write_to_table

        job.run()

        # verify that the transformation was succesful
        assert test_output.equals(mock_write.call_args[0][0])
