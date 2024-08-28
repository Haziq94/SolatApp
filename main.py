from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import requests
from requests.exceptions import RequestException

class PrayerTimesApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Button to fetch data
        fetch_button = Button(text='Fetch Prayer Times', size_hint_y=None, height=40)
        fetch_button.bind(on_press=self.fetch_prayer_times)
        layout.add_widget(fetch_button)

        # ScrollView to display the fetched data
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.grid_layout = GridLayout(cols=1, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)
        layout.add_widget(self.scroll_view)
        
        return layout

    def fetch_prayer_times(self, instance):
        url = 'http://www.e-solat.gov.my/index.php?r=esolatApi/TakwimSolat&period=today&zone=JHR02'
        try:
            # Disabling SSL certificate verification (not recommended for production)
            response = requests.get(url, verify=False)
            data = response.json()

            # Clear previous widgets
            self.grid_layout.clear_widgets()

            # Check if the response is successful
            if data['status'] == 'success':
                prayer_times = data['data']
                for prayer, time in prayer_times.items():
                    self.grid_layout.add_widget(Label(text=f"{prayer}: {time}", size_hint_y=None, height=40))
            else:
                self.grid_layout.add_widget(Label(text='Failed to fetch prayer times.', size_hint_y=None, height=40))

        except RequestException as e:
            self.grid_layout.clear_widgets()
            self.grid_layout.add_widget(Label(text=f'Error: {str(e)}', size_hint_y=None, height=40))


if __name__ == '__main__':
    PrayerTimesApp().run()
