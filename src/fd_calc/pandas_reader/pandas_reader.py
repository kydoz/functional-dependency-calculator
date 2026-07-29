import pandas
import sys
from utils import utils


def read_pandas():
    data: pandas.DataFrame
    nb_args = len(sys.argv)
    if nb_args > 1:
        file = sys.argv[1]
        if file.endswith(".csv"):
            try:
                data = pandas.read_csv(file)
            except Exception as e:
                utils.error(
                    "An error occured while reading the chosen csv file:\n" + str(e)
                )
                sys.exit(1)
        elif file.endswith(".xlsx"):
            if nb_args > 2:
                sheet = sys.argv[2]
                try:
                    data = pandas.read_excel(file, sheet_name=sheet)
                except Exception as e:
                    utils.error(
                        "An error occured while reading the chosen excel file:\n"
                        + str(e)
                    )
                    sys.exit(1)

            else:
                try:
                    xl = pandas.ExcelFile(file)
                except Exception as e:
                    utils.error(
                        "An error occured while reading the chosen excel file:\n"
                        + str(e)
                    )
                    sys.exit(1)
                for i, sheet in enumerate(xl.sheet_names):
                    print(f"{i + 1}. {sheet}")
                sheet_id = -1
                while sheet_id not in range(1, len(xl.sheet_names) + 1):
                    sheet_id = input("Choose sheet: ")
                    if sheet_id.isdigit():
                        sheet_id = int(sheet_id)
                data = pandas.read_excel(file, sheet_name=xl.sheet_names[sheet_id - 1])

        else:
            utils.error("Unsupported file type, currently supported: .csv, .xlsx")
            sys.exit(1)
    else:
        print(
            f"Usage: \n\t {sys.executable} {sys.argv[0]} <file_name>.csv \n\t {sys.executable} {sys.argv[0]} <file_name>.xlsx <sheet_name> (optional)"
        )
        sys.exit(0)
    return data
