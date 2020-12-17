import pytest
import json


class TestTextInput:

    def test_nums(self, hh_api):
        text_to_search = "1"
        response = hh_api.get(path='/vacancies', params={"text":  text_to_search})
        response_data = json.loads(response.text)
        assert response.status_code == 200
        assert response_data["found"] != 0

    def test_special_chars(self, hh_api):
        text_to_search = "!."
        response = hh_api.get(path='/vacancies', params={"text":  text_to_search})
        response_data = json.loads(response.text)
        assert response.status_code == 200
        assert response_data["found"] != 0

    @pytest.mark.parametrize("input", ['', 'a', 'a'*300])
    def test_input_length(self, hh_api, input):
        response = hh_api.get(path='/vacancies', params={"text":  input})
        response_data = json.loads(response.text)
        assert response.status_code == 200
        assert response_data["found"] != 0


class TestSearchByWords:

    def test_get_all_vacancies(self, hh_api):
        response = hh_api.get(path='/vacancies')
        response_data = json.loads(response.text)
        assert response.status_code == 200
        assert response_data["found"] != 0

    def test_one_word(self, hh_api):
        text_to_search = "продавец"
        response = hh_api.get(path='/vacancies', params={"text":  text_to_search})
        response_data = json.loads(response.text)
        assert response.status_code == 200
        for item in response_data["items"]:
            assert text_to_search in item["name"].lower()

    def test_several_words(self, hh_api):
        text_to_search = "qa engineer python"
        response = hh_api.get(path='/vacancies', params={"text":  text_to_search})
        response_data = json.loads(response.text)
        assert response.status_code == 200
        assert response_data["found"] > 0

    def test_no_vacancy(self, hh_api):
        text_to_search = "sjlhfskjhdlfjkdh"
        response = hh_api.get(path='/vacancies', params={"text":  text_to_search})
        response_data = json.loads(response.text)
        assert response.status_code == 200
        assert response_data["found"] == 0


class TestPhrases:

    def test_phrase(self, hh_api):
        text_to_search = 'Продажа оборудования'
        text_to_search_phrase = '"Продажа оборудования"'
        response = hh_api.get(path='/vacancies', params={"text":  text_to_search})
        response_phrase = hh_api.get(path='/vacancies', params={"text":  text_to_search_phrase})
        response_data = json.loads(response.text)
        response_data_phrase = json.loads(response_phrase.text)
        assert response_phrase.status_code == 200
        assert response_data["found"] > response_data_phrase["found"]


class TestWordForms:

    def test_different_word_form(self, hh_api):
        text_to_search = 'продажник'
        text_to_compare = 'продаж'
        response = hh_api.get(path='/vacancies', params={"text":  text_to_search})
        response_data = json.loads(response.text)
        assert response.status_code == 200
        for item in response_data["items"]:
            assert text_to_search not in item["name"].lower() \
                and text_to_compare in item["name"].lower()

    def test_specific_word_form(self, hh_api):
        text_to_search_form = '!продажи'
        text_to_search_no_form = 'продажи'
        response_form = hh_api.get(path='/vacancies', params={"text":  text_to_search_form})
        response_no_form = hh_api.get(path='/vacancies', params={"text":  text_to_search_no_form})
        response_data_form = json.loads(response_form.text)
        response_data_no_form = json.loads(response_no_form.text)
        assert response_form.status_code == 200
        assert response_data_form["found"] < response_data_no_form["found"]

    def test_part_of_word(self, hh_api):
        text_to_search_form = 'гео*'
        text_to_search_no_form = 'гео'
        response_form = hh_api.get(path='/vacancies', params={"text":  text_to_search_form})
        response_no_form = hh_api.get(path='/vacancies', params={"text":  text_to_search_no_form})
        response_data_form = json.loads(response_form.text)
        response_data_no_form = json.loads(response_no_form.text)
        assert response_form.status_code == 200
        assert response_data_form["found"] > response_data_no_form["found"]


class TestLogicOperators:

    def test_logic_or(self, hh_api):
        text_to_search_or = 'нефть OR бензин'
        text_to_search_compare = 'нефть'
        response_or = hh_api.get(path='/vacancies', params={"text":  text_to_search_or})
        response_compare = hh_api.get(path='/vacancies', params={"text":  text_to_search_compare})
        response_data_or = json.loads(response_or.text)
        response_data_compare = json.loads(response_compare.text)
        assert response_or.status_code == 200
        assert response_data_or["found"] > response_data_compare["found"]

    def test_logic_and(self, hh_api):
        text_to_search_and = 'нефть AND бензин'
        text_to_search_compare = 'нефть'
        response_and = hh_api.get(path='/vacancies', params={"text":  text_to_search_and})
        response_compare = hh_api.get(path='/vacancies', params={"text":  text_to_search_compare})
        response_data_and = json.loads(response_and.text)
        response_data_compare = json.loads(response_compare.text)
        assert response_and.status_code == 200
        assert response_data_and["found"] < response_data_compare["found"]

    def test_logic_not(self, hh_api):
        text_to_search_not = 'нефть NOT бензин'
        text_to_search_compare = 'нефть'
        response_not = hh_api.get(path='/vacancies', params={"text":  text_to_search_not})
        response_compare = hh_api.get(path='/vacancies', params={"text":  text_to_search_compare})
        response_data_not = json.loads(response_not.text)
        response_data_compare = json.loads(response_compare.text)
        assert response_not.status_code == 200
        assert response_data_not["found"] < response_data_compare["found"]


class TestField:

    def test_field_id_valid(self, hh_api):
        v_id = '40585500'
        text_to_search = f'!ID:{v_id}'
        response = hh_api.get(path='/vacancies', params={"text":  text_to_search})
        response_data = json.loads(response.text)
        assert response.status_code == 200
        assert response_data["items"][0]["id"] == v_id

    @pytest.mark.parametrize("id_to_search", ['qw', '0'])
    def test_field_id_invalid(self, hh_api, id_to_search):
        text_to_search = f'!ID:{id_to_search}'
        response = hh_api.get(path='/vacancies', params={"text":  text_to_search})
        response_data = json.loads(response.text)
        assert response.status_code == 200
        assert response_data["found"] == 0
