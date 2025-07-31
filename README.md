# PV-Production-Estimator
PV Production Estimator using basic input data, PVGIS API and returns map, production estimate per array, month and grand total. 
This tool is developed for streamlit and accessible at https://pv-estimator.streamlit.app

### The tool asks for the following inputs:
    1. Geographical Address (This has to be a proper street name, number, and pin/zip code. City name is optional)
    2. The WattPeak size of a single panel. Presently, the system assumes only one type of panel across all arrays.
    3. The details of a PV array:
        a. The following details are asked - Pitch (the inclination of the roof/system), Azimuth (the orientaiton of the roof with reference to south, THIS TOOL NEEDS INPUT IN PVGIS formato of azimuth), number of panels.
        b. For each array, a shading level is also asked, which is categorised as Low/Moderate/High/Extreme. These correspond to additional losses of 6%/12%/18%/30%.
        c. The details can be entered for a maximum of four arrays.
        d. If a back-to-back layout is used, the user has the option of adding their second array with the opposite azimuth. Presently this is manually done.

The tool operates with Open Street Map and PVGIS APIs for a basic retrieval of coordinates and estimated production of solar power in that area.

### The tool has following outputs:
    1. A map marking the coordinates to cross-verify address.
    2. A bar chart with monthly production across all arrays.
    3. A tabular display of production across each array per month. The row and column subtotals correspond to per-month and per-array productions respectively.
    4. A total that is the sum of all production.

### Financial Analysis (IRR)
This tool includes a simple internal rate of return (IRR) calculator. The default cost per kWp is set to **1000 USD**, which reflects the market average for small PV systems according to IRENA's *Renewable Power Generation Costs in 2022*. The default electricity price is **0.15 USD/kWh** and the lifetime is assumed to be 25 years. These values can be adjusted in the app before computing the IRR.

### Known limitations of the tool. At least some of these can be fixed within the parameters of open-source software and information:
    1. The PVGIS API can show an error 400, which means the coordinates are in the sea. This is a limitation at the level of PVGIS.
    2. Back-to-back modules are manually entered as individual arrays.
    3. The tool provides a quick estimation for an initial year - It is not presently capable of long-term calculations.
    4. Shading is a subjective phenomenon.
    5. The tool does not calculate or account for the type of inverter(s) used in the system.
    6. The accuracy of location identification is dependent on the OpenStreetMap Nominatim API. In some cases, particularly with less specific addresses or newly developed areas, the geocoding might not accurately reflect the actual location.
    7. The tool relies on external APIs for solar irradiation data, which may not fully capture local microclimates or shading from surrounding structures not accounted for in broad datasets.
    8. While the tool provides a basic IRR calculator, it does not perform detailed financial analyses such as calculating tax benefits, depreciation, or varying electricity rates over time. These factors can significantly affect the financial return of solar investments.
    9. The tool assumes a fixed orientation and tilt for solar panels. In reality, adjustable mounting systems can optimize panel angles seasonally, potentially enhancing production.
    10. Long-term maintenance, operational costs, and potential system downtime are not considered in the production estimates.
    11. The tool does not take into account local building codes, regulations, or grid connection policies that might impact the feasibility or cost of solar installations.
    12. It does not directly compare generated solar energy with the user’s energy consumption profile to calculate excess production or shortfall.
    13. The tool does not account for the gradual degradation of solar panel efficiency over time, which can affect long-term energy production.
    14. The tool lacks integration with real-time data for weather conditions and solar irradiation, which could provide more accurate, up-to-date estimations.
    15. The tool has limited capabilities in allowing users to specify detailed characteristics of solar panels and inverters, such as brand-specific efficiency, warranty conditions, or technological type.
    16.  It does not include an analysis of the environmental impacts or carbon footprint reduction associated with installing the solar PV system.

### Credits:
The PV Estimator was built using a variety of open-source tools, including Python, Streamlit, OpenStreetMap (OSM), and the Photovoltaic Geographical Information System (PVGIS), all of which remain the property of their respective owners. The code for PV Estimator is hosted on GitHub in a public repository. While the tool and its future iterations are considered the author's intellectual product, the use of these open-source resources is gratefully acknowledged.

As a master's graduate in sustainable energy, my technical knowledge has significantly contributed to this project. However, I am not a programming expert and have utilized artificial intelligence, particularly ChatGPT, in the development of this tool. I welcome contributions, feedback, and suggestions for improvement from the community. If you're interested in contributing or have feedback, please feel free to submit issues or pull requests on GitHub or contact me directly at aswath.subramanian@outlook.com

When using or referencing the PV Estimator, attribution to the original work is appreciated.

This project is licensed under the Apache License 2.0, allowing for its use and modification under the terms outlined therein.
