import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class WeatherApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Text input for the city name
        self.city_input = TextInput(hint_text="Enter city name", multiline=False)
        self.layout.add_widget(self.city_input)

        # Button to fetch weather
        self.get_weather_button = Button(text="Get Weather")
        self.get_weather_button.bind(on_press=self.get_weather)
        self.layout.add_widget(self.get_weather_button)

        # Label to display the weather
        self.weather_label = Label(text="Weather info will appear here")
        self.layout.add_widget(self.weather_label)

        return self.layout

    def get_weather(self, instance):
        city_name = self.city_input.text
        api_key = "f716ec14c2a9a57fdeb2f28eeedb34d8"  # Replace with your actual API key
        base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

        # Print the URL for debugging
        print(f"Request URL: {base_url}")

        try:
            response = requests.get(base_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            data = response.json()
            if data.get('cod') == 200:  # Check if the response code is 200 (OK)
                temperature = data['main']['temp']
                description = data['weather'][0]['description']
                self.weather_label.text = f"Temperature: {temperature}°C\nDescription: {description.capitalize()}"
            else:
                # Handle API errors
                self.weather_label.text = f"Error: {data.get('message', 'Unknown error')}"
        except requests.RequestException as e:
            # Handle network errors or invalid responses
            self.weather_label.text = f"Request failed: {e}"

if __name__ == '__main__':
    WeatherApp().run()
