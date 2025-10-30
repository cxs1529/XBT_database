
from xbtutils import database
from xbtweb import xbt_html, xbtmap
from jinja2 import Environment, FileSystemLoader
import os
import datetime

dbfile = "xbtData.db"
max_profiles = 10000

# directories relative to app.py
template_dir_path = "xbtweb"
template_file_path = "index_template.html"
index_file_path = os.path.join("web","index.html")
xbtmap_file_path = os.path.join("web","static","maps")

def main():

    # get time range for the report (today-6 months)
    today = datetime.datetime.now() + datetime.timedelta(days=1) # make sure it includes today in utc
    today_string = f"{today.year}-{(today.month):02d}-{(today.day):02d}"
    six_months_ago = today - datetime.timedelta(days=6*30.5)
    six_months_ago_string = f"{six_months_ago.year}-{(six_months_ago.month):02d}-{(six_months_ago.day):02d}"
    # print(today_string, six_months_ago_string)
    # get database report for main xbt site
    report_string = database.database_summary(dbfile, start_date=six_months_ago_string, end_date=today_string, show = False, outputDir="output", fname="myreport.txt", export=False)
    html_report_table = xbt_html.to_html_table(report_string)
    # print(html_report_table)

    # query database and import list of filename, soopline, callsign, lat, lon and datetime
    profile_list = database.read_database_map_info(dbfile, limit=max_profiles)
    map_name = xbtmap.make_summary_map(profile_list, outputDir=xbtmap_file_path)
    # create path relative to index.html
    map_path_index = os.path.join("static", "maps", map_name)

    # Create html report with jinja
    template = Environment(loader=FileSystemLoader(template_dir_path) ).get_template(template_file_path)   
    html_content = {"report" : html_report_table, "map_path": map_path_index}
    renderedText = template.render(html_content)
    # print(renderedText)
    with open(index_file_path, 'w') as fout:
        fout.write(renderedText)

    # end of main

if __name__ == "__main__":
    main()