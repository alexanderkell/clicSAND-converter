import pandas as pd
import numpy as np
from tkinter import *
import tkinter.filedialog


def osemosys_to_csv(input, output):
    label = Label(text="Loading...").pack()

    columns = [
        "index",
        "Variable",
        "Dim1",
        "Dim2",
        "Dim3",
        "Dim4",
        "Dim5",
        "Dim6",
        "Dim7",
        "Dim8",
        "Dim9",
        "Dim10",
        "ResultValue",
    ]
    osemosys_output = pd.read_csv(
        input, names=columns, sep="\(|,|\)|[ \t]{1,}", engine="python"
    )

    def check_for_all_zeros(df):
        df.loc[:, (df == 0).all(axis=0)] = np.nan
        return df

    osemosys_clean = osemosys_output.groupby("Variable").apply(
        lambda x: check_for_all_zeros(x)
    )

    osemosys_clean["ResultValue"] = osemosys_clean.ffill(axis=1).iloc[:, -1]

    def replace_result_value(df):
        df[df.loc[:, ~df.isnull().all()].iloc[:, -2].name] = np.nan
        return df

    osemosys_cleaned = osemosys_clean.groupby("Variable").apply(
        lambda x: replace_result_value(x)
    )

    osemosys_cleaned = osemosys_cleaned.drop("index", axis=1)

    output_directory = "{}/final_output.csv".format(output)
    osemosys_cleaned.to_csv(
        output_directory,
        index=False,
    )
    label = Label(
        text="Conversion successfully run, check your output directory for the file."
    ).pack()


if __name__ == "__main__":
    global a
    a = Tk()
    a.title("OSeMOSYS Output Converter")

    def file_open():
        input_file = tkinter.filedialog.askopenfilename()
        label = Label(text="Input file\n {}".format(input_file)).pack()
        global input
        input = input_file
        return input

    def directory_open():
        output_file = tkinter.filedialog.askdirectory()
        label = Label(text="Output directory\n {}".format(output_file)).pack()
        global output
        output = output_file
        return output_file

    input = Button(text="Input file", width=30, command=file_open).pack()
    output = Button(text="Output directory", width=30, command=directory_open).pack()
    run = Button(
        text="Run", width=30, command=lambda: osemosys_to_csv(input, output)
    ).pack()

    a.mainloop()