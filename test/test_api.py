from app.api import AQIapi


class TestCase:
    def __init__(self) -> None:
        self.api_aqi = AQIapi(False)
        self.api_aqi.key = '2af1dc58-ca93-4dee-980e-58193818cfca'

    def test_get_countries(self) -> None:
        result = self.api_aqi.request_countries()
        print('countries')
        print(result)
        print('_____')

    def test_get_states(self) -> None:
        country = 'China'
        result = self.api_aqi.request_states(country)
        print('state')
        print(result)
        print('____')

    def test_get_cities(self) -> None:
        country = 'China'
        state = 'Jiangxi'
        result = self.api_aqi.request_cities(country, state)
        print('state')
        print(result)
        print('____')

    def test_get_city_data(self) -> None:
        country = 'China'
        state = 'Jiangxi'
        city = 'Ganzhou'
        result = self.api_aqi.request_city_data(country, state, city)
        print('city data')
        print(result)
        print('____')
        return

    def run_test(self) -> None:
        self.test_get_countries()
        self.test_get_states()
        self.test_get_cities()
        self.test_get_city_data()


def main() -> None:
    t = TestCase()
    t.run_test()
