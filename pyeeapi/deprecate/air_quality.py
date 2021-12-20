""" docstring """

from io import StringIO

from datetime import date, datetime
import requests
import pandas as pd

from pyeeapi import _contants as c


class AirQuality():
    """ docstring """

    @staticmethod
    def request_eea(list_params):
        """ docstring """

        eea_urls = []

        for params in list_params:
            response = requests.request("GET", url=c.url.format(**params))

            if response.ok:
                eea_urls += response.content.decode("utf-8-sig") \
                                            .split("\r\n")[:-1]

        list_data_frame = []
        for url in eea_urls:
            data = requests.request("GET", url).text

            list_data_frame.append(pd.read_csv(StringIO(data)))

        if len(list_data_frame) == 0:
            return pd.DataFrame(columns=["Countrycode",
                                         "AirQualityStationEoICode",
                                         "AirPollutant",
                                         "DatetimeBegin", "DatetimeEnd",
                                         "Concentration", "UnitOfMeasurement",
                                         "Validity", "Verification"])

        return pd.concat(list_data_frame)

    @staticmethod
    def eea_sites_info(country, station_type, station_area):
        pass

    @staticmethod
    def get_observations(country_code="", city_name="", pollutant="",
                         start="", end="", station="", eoi_code="",
                         sampling_point="", output=c.output[1], update_date="",
                         time_coverage=c.time_coverage[0]):
        """ docstring """

        year_from = start.year
        year_to = end.year

        params = {"country_code": country_code,
                  "city_name": city_name,
                  "pollutant": c.pollutants[pollutant],
                  "year_from": year_from,
                  "year_to": year_to,
                  "station": station,
                  "eoi_code": eoi_code.upper(),
                  "sampling_point": sampling_point,
                  "source": c.source[2],
                  "output": output,
                  "update_date": update_date,
                  "time_coverage": time_coverage}

        if (year_from != datetime.today().year and
                year_to == datetime.today().year):

            list_params = [params, params.copy()]

            # years before
            list_params[0]["year_to"] = year_to-1
            # year now
            list_params[1]["year_from"] = year_to
        else:
            list_params = [params]

        data = AirQuality.request_eea(list_params)
        if data.empty:
            return data

        # Datetime columns
        dt_columns = ["DatetimeBegin", "DatetimeEnd"]
        data[dt_columns] = data[dt_columns].apply(pd.to_datetime)

        # Filter dates
        data = data[data.DatetimeBegin.dt.tz_convert(None) >= start]
        data = data[data.DatetimeBegin.dt.tz_convert(None) <= end]

        return data.astype({"Concentration": "float64"})

    @staticmethod
    def clean_observations(eea_data, averaging_time="day", valid_only=True,
                           verify=False):
        """ docstring """

        clean_columns = ["Countrycode", "AirQualityStationEoICode",
                         "AirPollutant", "DatetimeBegin", "Concentration",
                         "UnitOfMeasurement", "Validity", "Verification"]
        if eea_data.empty:
            return pd.DataFrame(columns=clean_columns)

        eea_data = eea_data.iloc[clean_columns]

        if valid_only:
            eea_data = eea_data[eea_data.Validity == 1]
        if verify:
            eea_data = eea_data[eea_data.Verification == 1]

        dt_columns = ["DatetimeBegin"]
        if averaging_time == "day":
            eea_data[dt_columns] = eea_data[dt_columns].applymap(
                lambda x: date(x.year, x.month, x.day))

        clean_columns.remove("Concentration")
        return eea_data.groupby(by=clean_columns,
                                as_index=False,
                                axis=0).mean()
