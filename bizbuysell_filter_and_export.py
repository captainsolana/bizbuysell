import argparse
from datetime import date
import pandas as pd
import pdb
import sys


class Serp():
    def __init__(self, *, url, name, formdata):
        self.name = name
        self.firstpage_url = url
        self.formdata = formdata
        self.response_text = ""

    def __repr__(self):
        return self.name


class Listing():
    def __init__(self, custom_name, **entries):
        self.__dict__.update(entries)
        self.custom_name = custom_name
        self.date_accessed = date.today()

    def __hash__(self):
        return hash(self.custom_name)

    def __eq__(self, other):
        return self.custom_name == other.custom_name

    def __repr__(self):
        return self.custom_name


def filter_objects_and_write_to_csv(object_list, outfile):
    dicts_list = []
    for obj in object_list:
        if hasattr(obj, "financials") and hasattr(obj, "address"):
            obj.financials["url"] = obj.url
            obj.financials["parent_category"] = obj.category["parent_category"]
            obj.financials["sub_category"] = obj.category["sub_category"]
            obj.financials["state"] = obj.address["addressRegion"]
            if hasattr(obj, "details"):
                employees_present = "Employees" in obj.details
                if employees_present:
                    obj.financials["Employees"] = obj.details["Employees"]
                else:
                    obj.financials["Employees"] = "Not Present"
            dicts_list.append(obj.financials)

    df_init = pd.DataFrame(dicts_list)
    df_init.sort_values("url")

    df = df_init.drop_duplicates(
        subset=[
            "Asking Price", "Cash Flow", "EBITDA", "Employees", "Established", "FF&E",
            "Gross Revenue", "Inventory"
        ]
    )

    df_ints = df[(df["Multiple"].apply(lambda x: type(x) == float)) & df["Cash Flow"].apply(lambda x: type(x) == int)]
    states = ["Illinois", "Indiana", "Michigan", "Minnesota",
              "Missouri", "Ohio", "Pennsylvania", "Virginia"]
    df_filtered = df_ints[
        (df_ints["Multiple"].between(0.75, 5)) & (df_ints["Cash Flow"] > 500000) & df_ints.state.isin(states)]

    # When writing a new CSV
    # df_filtered.to_csv(outfile)

    # When appending
    df_filtered.to_csv(outfile, mode="a", header=False)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "-F", "--infile", required=True, help="Path to a PKL file of parsed listings"
    )
    p.add_argument(
        "--outfile",
        default="out.csv",
        help="Path to write the output to (default: %(default)s)",
    )

    args = p.parse_args(sys.argv[1:])

    infile = args.infile
    outfile = args.outfile
    # /Users/work/Dropbox/Projects/Working Data/bizbuysell/listings20191231_parsed.pkl

    object_list = pd.read_pickle(infile)
    filter_objects_and_write_to_csv(object_list, outfile)
    pdb.set_trace()
