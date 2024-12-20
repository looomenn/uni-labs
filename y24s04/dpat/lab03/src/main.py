"""
Course: DPAT
Lab: 03
"""

import vhi  # овоʼязковий імпорт для отримання даних з NOAA
import pandas as pd

from spyre import server
import matplotlib.pyplot as plt

# True - буде закачувати файли з NOAA при кожному запуску.
# Обовʼязково при першому запуску.
FETCH: bool = False

if FETCH: vhi.fetch_bulk(1, 27, 1982, 2023)
DATAFRAME = vhi.get_dataframe(vhi.DUMP_FOLDER)


def error_plot(
        text: str,
        ax: plt.Axes
) -> None:
    """
    Функція, яка додає на графік вказаний текст.
    :param text: Текст, який треба відобразити
    :param ax: Осі з ініціалізованого plt.subplots()
    :return: None
    """
    ax.text(0.5, 0.5, text,
            fontsize=15, ha='center', va='center', wrap=True)
    ax.set_axis_off()


class VhiVisualizer(server.App):
    title = "NOAA Visualisation"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'NOAA data',
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}],
            "value": 'VHI',
            "key": 'index',
            "action_id": "update_data"
        },
        {
            "type": "dropdown",
            "label": "Region",
            "options": [
                {"label": vhi.get_province(region), "value": region} for region in DATAFRAME['PID'].unique()
            ],
            "key": "region",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "label": "Months Interval (e.g. 1-3)",
            "value": "1-3",
            "key": "months",
            "action_id": "update_data"
        },
        {
            "type": "dropdown",
            "label": "Start Year",
            "options": [
                {"label": str(year), "value": str(year)} for year in DATAFRAME['Year'].unique()
            ],
            "key": "start_year",
            "action_id": "update_data"
        },
        {
            "type": "dropdown",
            "label": "End Year",
            "options": [
                {"label": str(year), "value": str(year)} for year in DATAFRAME['Year'].unique()
            ],
            "key": "end_year",
            "action_id": "update_data"
        }
    ]

    tabs = ["Data", "Plot"]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Fetch"
    }]

    outputs = [
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Data",
            "on_page_load": True
        },
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        }
    ]

    @staticmethod  # заглушка для PEP8 :/
    def getData(params, **kwargs):

        # отримуємо з params усе необхідне
        index = params.get('index', 'VHI')
        region_id = int(params.get('region', DATAFRAME['PID'].iloc[0]))
        months = params.get('months', '1-3')
        start_year, end_year = int(params.get('start_year', '2000')), int(params.get('end_year', '2013'))
        start_month, end_month = map(int, months.split('-'))

        # перераховуємо місяці в тижні
        start_week = round((start_month - 1) * 4.33 + 1)
        end_week = round(end_month * 4.33)

        # перевіряємо, щоб ми не поїхали у віʼдємне майбунє
        if start_week > end_week:
            return pd.DataFrame(
                {
                    "Error": [f"The start month ({start_month}) cannot be larger than the end month ({end_month})"]
                }
            )

        # аналогічна перевірка тільки для роцьків
        if start_year > end_year:
            return pd.DataFrame(
                {
                    "Error": [f"The start year ({start_year}) cannot be larger than the end year ({end_year})"]
                }
            )

        # формуємо фільтрований датафрейм
        filtered_df = DATAFRAME[(DATAFRAME['PID'] == region_id) &
                                (DATAFRAME['Year'] >= start_year) &
                                (DATAFRAME['Year'] <= end_year) &
                                (DATAFRAME['Week'] >= start_week) &
                                (DATAFRAME['Week'] <= end_week)].copy()

        # магічний синтаксис бо ✨дейта клінінг✨від чату гепете (бо шось цього не було реалізовано в першій лабі лол)
        filtered_df = filtered_df[~filtered_df.isin([-1]).any(axis=1)]

        # міняємо айдішнік обласного центру на відповідну назву
        province_name = vhi.get_province(region_id)
        filtered_df.loc[:, 'Province'] = province_name

        # повертаємо фінальний датафрейм з відповідними стовпчиками
        return filtered_df[['Province', 'Year', 'Week', index]]

    def getPlot(self, params):
        """ функція для створення графіку """

        # отримуємо шо на треба для попередньої валідації
        start_year, end_year = int(params.get('start_year', '2023')), int(params.get('end_year', '2023'))
        start_month, end_month = map(int, params.get('months', '1-3').split('-'))
        index = params.get('index', 'VHI')

        # ініціалізація полотна
        fig, ax = plt.subplots()

        # валідація відʼємного майбунього
        if start_month > end_month:
            error_plot(f'The start month ({start_month}) cannot be larger than the end month ({end_month})', ax)
            return fig

        # валідація для можливості хоч шось там прочитати
        if end_year - start_year > 5:
            error_plot(f'For the plot, the difference between'
                       f' the start ({start_year}) and end ({end_year}) years can\'t be larger than 5.', ax)
            return fig

        # валідація відʼємного майбунього номер два
        if start_year > end_year:
            error_plot(f'Start year ({start_year}) cannot be larger that end year ({end_year}) ', ax)
            return fig

        # отримуємо датафрейм з попередньої функції
        filtered_df = self.getData(params)

        # робимо список з кольорами, для візуального розділення кожного року
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']

        # малюємо графікі
        for i, year in enumerate(filtered_df['Year'].unique()):
            year_data = filtered_df[filtered_df['Year'] == year].set_index('Week')
            ax.plot(year_data.index, year_data[index], color=colors[i % len(colors)], marker='o', label=f"Year {year}")

        ax.set_ylabel(index)
        ax.set_title(f"{index} over Weeks for Multiple Years")
        ax.set_xlabel("Week")
        ax.legend()

        return fig

    @staticmethod
    def getCustomCSS(**kwargs):
        css = """
        h1 {
            border-bottom: 0px;
            text-transform: none !important;
        }
        
        .spyrePad--vertS{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        li.active a, li.active a:hover{
            border: 1px solid #D7DBE1;
            -webkit-box-shadow: 0px 1px 3px 0px rgba(0,0,0,0.1);
            -moz-box-shadow: 0px 1px 3px 0px rgba(0,0,0,0.1);
            box-shadow: 0px 1px 3px 0px rgba(0,0,0,0.1);
        }
        
        .tab-links a {
            background: white;
            border-radius: 8px;
            color: #47536;
            border: 1px solid white;
        }
        
        .content > img[scr=""] { display: none }
        .tab-links { padding-inline-start: 15px !important}
        .tab-links li { margin: 0px 4px }
        .tab-links a:hover { background: #EFF4FE; color: black; }
        
        .menu {
            padding: 16px;
            height: auto;
            display: flex;
            flex-direction: column;
            border-radius: 6px;
            overflow: hidden;
        }
        
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            min-height: 648px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 12px;
        }
        p {
            color: #333;
        }
        input[type="text"], select {
            padding: 10px;
            width: 100%;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .button {
            background: #266EF1;
        }
        .button:hover {
            background-color: #175BCC;
        }
        .tabbable .nav-tabs {
            margin-bottom: 20px;
            background-color: #eee;
            border-bottom: 1px solid #ddd;
        }
        .tabbable .nav-tabs li.active a {
            background-color: #fff;
            border-color: #ddd #ddd #fff;
        }
        .tabbable .nav-tabs li a {
            border: 1px solid transparent;
            border-radius: 4px 4px 0 0;
        }
        .tabbable .tab-content {
            padding: 20px;
            border: 1px solid #ddd;
            border-top: none;
            background-color: #fff;
            border-radius: 0 4px 4px 4px;
        }
        """
        return css


def main():
    if FETCH: vhi.clear_dump_folder(vhi.DUMP_FOLDER)

    app = VhiVisualizer()
    app.launch()


if __name__ == "__main__":
    main()
