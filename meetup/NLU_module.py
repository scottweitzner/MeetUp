import constants
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features
from watson_developer_cloud import WatsonException
import shelve


def get_watson_keywords(text):
    watson_shelve = shelve.open(constants.SHELVE_FILE_PATH, writeback=False)

    try:
        if str(text) in watson_shelve:
            response = watson_shelve[str(text)]
        else:
            response = _execute_request(text)
            watson_shelve[str(text)] = response
    except WatsonException:
        return None  # TODO: create better error handling than just returning empty list
    finally:
        watson_shelve.close()

    return response['keywords']


##########################################################################
# Executes request to watson NLU unit and returns raw response
##########################################################################
def _execute_request(text):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        username=constants.WATSON_USER,
        password=constants.WATSON_PASS,
        version="2017-02-27"
    )

    response = natural_language_understanding.analyze(
        text=text,
        features=[
            features.Keywords()
        ]
    )

    return response


