from django.test import TestCase
from graphene_django.utils import GraphQLTestCase

class GraphQlUserTest(GraphQLTestCase):
    fixtures = ['users.json']

    def test_retrieve_by_id(self):
        expected = {
            "data": {
                "user": {
                    "id": "2",
                    "name": "palak",
                    "followers": [
                        {
                            "name": "shrey"
                        }
                    ]
                }
            }
        }
        res = self.query(
            """
            query {
                user(id: 2) {
                    id
                    name
                    followers {
                        name
                    }
                }
            }
            """
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(expected, res.json())
