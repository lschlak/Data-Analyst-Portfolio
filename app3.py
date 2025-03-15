import pandas as pd

from pathlib import Path

from USAggregate import usaggregate

import os

 

from shiny.express import input, render, ui, expressify

from shiny import reactive

from shinyswatch import theme

import datetime

 

#USAggregate currently REQUIRES you to have a time period...this seems not useful

#Needs to be np.nan in the example dataframe on github

 

#Add Shinyswatch to the requirements file!!!

 

MAX_SIZE = 50000

 

with ui.div(class_="col-md-10 col-lg-8 py-5 mx-auto text-lg-center text-left"):

    ui.h1("USAggregate"),

    ui.h3("Harmonize Multi-Level Geographical Data"),

    style ="text-align: center;"

 

ui.page_opts(title="USAggregate", theme=theme.cerulean)

 

names = ["CSV Upload", "Aggregation"]

 

#Remove tract from the options

#check what the lowest level of detail is for each csv

 

@expressify

def my_accordion(multiple=True, id="acc_multiple"):

    with ui.accordion():

        with ui.accordion_panel("Instructions"):

            ui.input_action_button("show76", "Click Here")

            @reactive.effect

            @reactive.event(input.show76)

            def _():

                            q = ui.modal(

                                    "Welcome to USAggregate, a Python-based webapp designed to allow simple and quick geographic harmonization of multiple csv files. Please click the button below for deatiled instructions:To use USAggregate, be sure your geographic variables are named TRACT, zip, county, city, or state and your time variable is labeled year (for four digit year values) or date (for date formatted values). If your csv file uses FIPS codes instead of geographic names, ensure column names are STATEFP, COUNTYFP, or STATECOUNTYFP (combined state and county code). USAggregate can only aggregate data to lowest level of granularity in your least granular csv. For example, if one csv only contains data at the state level, the data cannot be aggregated to the county or city level. To begin, select your desired level of geographic detail and your aggregation methods using the panel on the left. Then, upload your csv files and let USAggregate do the rest!",

                                    title="Instructions",

                                    easy_close=True,

                                    footer=None,

                                )

                            ui.modal_show(q)

        #    @render.text

        #    def text():

        #        return "Instructions"

        #with ui.accordion_panel("CSV Upload"):

         #    ui.input_file("file1", "Choose your 1st CSV to upload:", multiple=True),

          #   ui.input_file("file2", "Choose your 2nd CSV to upload:", multiple=True),

           #  ui.input_file("file3", "Choose your 3rd CSV to upload:", multiple=True)

       

        with ui.accordion_panel("Aggregation Method"):

            ui.input_selectize("geo_level", "Select geographic level of detail", choices=['tract', 'zip', 'city', 'county', 'state'])

            ui.input_selectize("aggregation", "Select your aggregation method", choices=["sum", "mean", "median"])

            ui.input_selectize("str_aggregation", "Select your string aggregation method", choices=["first", "last", "mode"])

            ui.input_selectize("time", "Select your time group", choices=['year','day', 'week', 'month', 'quarter', 'year'])

 

        with ui.accordion_panel("Local Specifications"):

               

                ui.input_action_button("show8", "Click Here")

 

                #This will probably be moved to a cell below the Data Upload + Data Downloard tables. Currently, clicking on the button clears previous inputs. Bit too fickle.

                @reactive.effect

                @reactive.event(input.show8)

                def _():

                    m = ui.modal(

                        ui.p("To indicate the aggregation method for one specific column, use the local column specification option."),

                        ui.p("First select 'Add Numeric Column' or 'Add String Column'. Then type a column name and a specified aggregation method."),

                        ui.p("Use local column specifications with care!"),

                        title="Local Column Specifications",

                        easy_close=True,

                        footer=None,

                    )

                    ui.modal_show(m)

                ui.p(" ")

 

                ui.input_checkbox("show1", "Add Numeric Column", False)

                with ui.panel_conditional("input.show1"):

                        ui.input_text("local_col1", "Column Name","")

                        ui.input_select("local_agg1", "Aggregation Method", ["","sum", "mean", "median"])

 

                ui.input_checkbox("show2", "Add Numeric Column", False)

                with ui.panel_conditional("input.show2"):

                        ui.input_text("local_col2", "Column Name", "")

                        ui.input_select("local_agg2", "Aggregation Method", ["","sum", "mean", "median"])

                   

                ui.input_checkbox("show3", "Add Numeric Column", False)

                with ui.panel_conditional("input.show3"):

                        ui.input_text("local_col3", "Column Name", "")

                        ui.input_select("local_agg3", "Aggregation Method ", ["","sum", "mean", "median"])

               

                ui.input_checkbox("show4", "Add String Column", False)

                with ui.panel_conditional("input.show4"):

                        ui.input_text("local_col4", "Column Name", "")

                        ui.input_select("local_agg4", "Aggregation Method ", ["","first", "last", "mode"])

 

                ui.input_checkbox("show5", "Add String Column", False)

                with ui.panel_conditional("input.show5"):

                        ui.input_text("local_col5", "Column Name", "")

                        ui.input_select("local_agg5", "Aggregation Method ", ["","first", "last", "mode"])

                       

                ui.input_checkbox("show6", "Add String Column", False)

                with ui.panel_conditional("input.show6"):

                        ui.input_text("local_col6", "Column Name", "")

                        ui.input_select("local_agg6", "Aggregation Method ", ["","first", "last", "mode"])

 

        with ui.accordion_panel("Troubleshooting"):  

                ui.input_action_button("show", "Click Here")

 

                @reactive.effect

                @reactive.event(input.show)

                def _():

                    m = ui.modal(

                        ui.p("Most errors thrown by USAggregate can be solved by simply adjusting your aggregation methods or local column specifications. Below are a handful of common errors and their resolutions:"),

                        ui.p("Error #1: You are trying to merge on datetime64[ns] and int64 columns. If you wish to proceed you should use pd.concat"),

                        ui.p("Solution #!: Ajust the time aggregation selection to an appropriate level of detail"),

                        ui.p(""),
                        ui.p(""),

                        ui.p("Error #2: To aggregate by 'tract', the DataFrame must have the 'tract' column."),

                        ui.p("Solution #2: Adjust the geographic aggregation selection to an appropriate level of detail. Tract is too low a level of detail based on the data provided (note: this could occur with any level of geographic that is more granular than the uploaded datasets)"),

                        ui.p(""),

                        ui.p(""),
                        ui.p("Error #3: 'GEO_ID' "),

                        ui.p("Solution #3: Adjust the geographic aggregate var"),

                        ui.p(""),
                        ui.p(""),

                        title="Troubleshooting",

                        easy_close=True,

                        footer=None,

                    )

                    ui.modal_show(m)

                                   

with ui.sidebar():

    my_accordion()

 

with ui.layout_columns(col_widths=[6,6], height="280px",fill=True):

    with ui.panel_well():

                ui.h2("Data Upload")

                with ui.layout_columns(height="500px",fill=True):              

                    with ui.navset_card_underline(id="selected_navset_card_underline"):

                                with ui.nav_panel("CSV #1"):

                                    ui.input_file("file1", "", multiple=True)

                                    @render.code

                                    def preview_df1():

                                                        # First file

                                                        file1 = input.file1()

                                                        if not file1:

                                                            return

                                                        file_name = str(file1[0]["name"])

 

                                                        with open(file1[0]["datapath"], "r", encoding='utf-8-sig') as f:

                                                            dataframe1 = pd.read_csv(f)

                                                           

                                                        return dataframe1

                                        #with ui.card():

                                        #    ui.card_header("Local Specifications")

                                        #    ui.input_selectize("geo_level5", "Column Name", choices=["county", "state", "city", "zip"])

                                        #    ui.input_selectize("geo_level2", "Geo Level", choices=["county", "state", "city", "zip"])

                                        #    ui.input_selectize("geo_level3", "Numerical Agg", choices=["county", "state", "city", "zip"])

                                        #    ui.input_selectize("geo_level4", "String Agg", choices=["county", "state", "city", "zip"])

                                           

                                           

                                with ui.nav_panel("CSV #2"):

                                    ui.input_file("file2", "", multiple=True)

                                    @render.code

                                    def preview_df2():

                                            file2 = input.file2()

                                            if not file2:

                                                return

                                            file_name = str(file2[0]["name"])

                                            # infile = Path(__file__).parent / file_name

 

                                            with open(file2[0]["datapath"], "r", encoding='utf-8-sig') as f:

                                                dataframe2 = pd.read_csv(f)

 

                                            return dataframe2

 

                                with ui.nav_panel("CSV #3"):

                                    ui.input_file("file3", "", multiple=True)

                                    @render.code

                                    def preview_df3():

                                            file3 = input.file3()

                                            if not file3:

                                                return

                                            file_name = str(file3[0]["name"])

                                            # infile = Path(__file__).parent / file_name

 

                                            with open(file3[0]["datapath"], "r", encoding='utf-8-sig') as f:

                                                dataframe3 = pd.read_csv(f)

 

                                            return dataframe3

                                   

                                with ui.nav_panel("CSV #4"):

                                    ui.input_file("file4", "", multiple=True)

                                    @render.code

                                    def preview_df4():

                                            file4 = input.file4()

                                            if not file4:

                                                return

                                            file_name = str(file4[0]["name"])

                                            # infile = Path(__file__).parent / file_name

 

                                            with open(file4[0]["datapath"], "r", encoding='utf-8-sig') as f:

                                                dataframe4 = pd.read_csv(f)

 

                                            return dataframe4

                               

                           

 

                            #return result

                        #f"{names}"

 

                #return file_name

 

    with ui.panel_well():

            ui.h2("Data Download")  

            @render.text

            def value():

                            text = "The dataframes were aggregated up to the " + input.geo_level() + " level. To download the aggregated csv, click here:"

                            return text

            ui.p(" ")

            @render.download(label="Download Aggregated Data", filename="USAggregate.csv")

            def download1():

                                       

                                                # First file

                                                counter1=0

                                                file1 = input.file1()

                                                if file1 is None:

                                                    counter1=1

                                                else:

                                                    file_name = str(file1[0]["name"])

 

                                                    with open(file1[0]["datapath"], "r", encoding='utf-8-sig') as f:

                                                        dataframe1 = pd.read_csv(f)

                                                   

 

                                                ########################################################

 

                                                # Second file

                                                counter2=0

                                                file2 = input.file2()

                                                if file2 is None:

                                                    counter2=1

                                                else:

                                                    file_name = str(file2[0]["name"])

                                                # infile = Path(__file__).parent / file_name

 

                                                    with open(file2[0]["datapath"], "r", encoding='utf-8-sig') as f:

                                                        dataframe2 = pd.read_csv(f)

 

                                                ########################################################

 

                                                # Third file

                                               

                                                counter3=0

                                                file3 = input.file3()

                                                if file3 is None:

                                                        counter3=1

                                                else:

                                                    file_name = str(file3[0]["name"])

                                                    # infile = Path(__file__).parent / file_name

 

                                                    with open(file3[0]["datapath"], "r", encoding='utf-8-sig') as f:

                                                        dataframe3 = pd.read_csv(f)

 

                                                counter4=0

                                                file4 = input.file4()

 

                                                if file4 is None:

                                                        counter4=1

                                                else:

                                                    file_name = str(file4[0]["name"])

                                                    # infile = Path(__file__).parent / file_name

 

                                                    with open(file4[0]["datapath"], "r", encoding='utf-8-sig') as f:

                                                            dataframe4 = pd.read_csv(f)

 

                                                   

                                               

                                                #return file1[0]['name'], file2[0]['name'],file3[0]['name']

                                                ########################################################

                                                data_list=[]

 

                                                if counter1==0:

                                                        data_list.append(dataframe1)

 

                                                if counter2==0:

                                                        data_list.append(dataframe2)

 

                                                if counter3==0:

                                                        data_list.append(dataframe3)

                                                   

                                                if counter4==0:

                                                        data_list.append(dataframe4)

 

                                                dictionary_numeric_locals={input.local_col1(): input.local_agg1(),

                                                                          input.local_col2(): input.local_agg2(),

                                                                          input.local_col3(): input.local_agg3()}

                                               

                                                dictionary_string_locals = {input.local_col4(): input.local_agg4(),

                                                                          input.local_col5(): input.local_agg5(),

                                                                          input.local_col6(): input.local_agg6()}

 

                                           

                                                df= usaggregate(data=data_list,

                                                                                level=input.geo_level(),

                                                                                agg_numeric_geo=input.aggregation(),

                                                                                agg_character_geo=input.str_aggregation(),

                                                                                col_specific_agg_num_geo=dictionary_numeric_locals,

                                                                                col_specific_agg_chr_geo=dictionary_string_locals,

                                                                                time_period=input.time())

 

                                            #yield buf.getvalue()

                                                yield df.to_csv(index=False)

 

            @render.download(label="Download Change Log", filename="USAggregate_Log.txt")

            def download4():

 

                f = lambda x:" " if x is None else x[0]["name"]

                f1 = f(input.file1())

                f2 = f(input.file2())

                f3 = f(input.file3())

                f4 = f(input.file4())

               

                text = f"""

                USAggregate Output

                -------------------------------------------------------------

                The date and time is:                     {datetime.datetime.now()}
                The aggregated file names were:           {f1,f2,f3,f4}  
                The geographic level of aggregation was:  {input.geo_level()}
                The numeric aggregation method was:       {input.aggregation()}
                The string aggregation method was:        {input.str_aggregation()}
                The time aggregation method was:          {input.time()}
                Local numeric specifications were:        {input.local_col1()}:{input.local_agg1()},{input.local_col2()}:{input.local_agg2()},{input.local_col3()}:{input.local_agg3()}
                Local string specifications were:         {input.local_col4()}:{input.local_agg4()},{input.local_col5()}:{input.local_agg5()},{input.local_col6()}:{input.local_agg6()}

                ---------------------------------------------------------------

                For more details on the USAggregate python package, visit: https://github.com/ethand05hi/USAggregate/tree/main

 
                **Designed by Ethan Doshi & Luke Schlake**

                """

 

                yield text

 

            ui.p(" ")

            with ui.card():

                                            @render.code

                                            def output():

                                        # First file

                                                 # First file

                                                counter1=0

                                                file1 = input.file1()

                                                if file1 is None:

                                                    counter1=1

                                                else:

                                                    file_name = str(file1[0]["name"])

 

                                                    with open(file1[0]["datapath"], "r", encoding='utf-8-sig') as f:

                                                        dataframe1 = pd.read_csv(f)

                                                       

 

                                                ########################################################

 

                                                # Second file

                                                counter2=0

                                                file2 = input.file2()

                                                if file2 is None:

                                                    counter2=1

                                                else:

                                                    file_name = str(file2[0]["name"])

                                                # infile = Path(__file__).parent / file_name

 

                                                    with open(file2[0]["datapath"], "r", encoding='utf-8-sig') as f:

                                                        dataframe2 = pd.read_csv(f)

 

                                                ########################################################

 

                                                # Third file

                                               

                                                counter3=0

                                                file3 = input.file3()

                                                if file3 is None:

                                                        counter3=1

                                                else:

                                                    file_name = str(file3[0]["name"])

                                                    # infile = Path(__file__).parent / file_name

 

                                                    with open(file3[0]["datapath"], "r", encoding='utf-8-sig') as f:

                                                        dataframe3 = pd.read_csv(f)

 

                                                counter4=0

                                                file4 = input.file4()

                                                if file4 is None:

                                                        counter4=1

                                                else:

                                                    file_name = str(file4[0]["name"])

                                                    # infile = Path(__file__).parent / file_name

 

                                                    with open(file4[0]["datapath"], "r", encoding='utf-8-sig') as f:

                                                            dataframe4 = pd.read_csv(f)

                                               

                                                #return file1[0]['name'], file2[0]['name'],file3[0]['name']

                                                ########################################################

                                                try:

                                                    data_list=[]

 

                                                    if counter1==0:

                                                                data_list.append(dataframe1)

 

                                                    if counter2==0:

                                                                data_list.append(dataframe2)

 

                                                    if counter3==0:

                                                                data_list.append(dataframe3)

                                                           

                                                    if counter4==0:

                                                                data_list.append(dataframe4)

 

                                                    dictionary_numeric_locals={input.local_col1(): input.local_agg1(),

                                                                          input.local_col2(): input.local_agg2(),

                                                                          input.local_col3(): input.local_agg3()}

                                               

                                                    dictionary_string_locals = {input.local_col4(): input.local_agg4(),

                                                                          input.local_col5(): input.local_agg5(),

                                                                          input.local_col6(): input.local_agg6()}

                                                   

   

                                                    df= usaggregate(data=data_list,

                                                                                    level=input.geo_level(),

                                                                                    agg_numeric_geo=input.aggregation(),

                                                                                    agg_character_geo=input.str_aggregation(),

                                                                                    col_specific_agg_num_geo=dictionary_numeric_locals,

                                                                                    col_specific_agg_chr_geo=dictionary_string_locals,

                                                                                    time_period=input.time())

                                                    return df

                                                except IndexError:

                                                        print("")

 
