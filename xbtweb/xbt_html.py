

def to_html_table(csv_string):
    print("Converting report to html table")
    # split cvs lines into list
    lines = csv_string.splitlines()
    print(lines)

    # Check that the report has results
    if lines[0].startswith("WARNING") == False:
        # html_header = ""
        # html_data = ""
        html_table = ""
        for row,line in enumerate(lines):
            if row == 0:
                html_header = "<tr>\n\t"
                line_headers = line.split(",")
                for header in line_headers:
                    html_header = html_header + "\t<th>" + header + "</hr>\n\t"
                html_header = html_header + "</tr>\n\t"   
                html_table = html_table + html_header
            else:
                html_data = "<tr>\n\t"
                line_values = line.split(",")
                for value in line_values:
                    html_data = html_data + "\t<td>" + value + "</td>\n\t"
                html_data = html_data + "</tr>\n\t"
                html_table = html_table + html_data
        html_string = "<table>\n\t" + html_table + "</table>\n"
    else:
        html_string = "<p>No results</p>"    
    # for line in lines:
    #     print(line)


    return html_string