import json
from pathlib import Path
import re
from os import makedirs


START_INDEX = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px 12px;
            border: 1px solid #ccc;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
        .pass {
            background-color: #d4edda;
        }
        .fail {
            background-color: #f8d7da;
        }
        .skip {
            background-color: #fff3cd;
        }
        #all:checked ~ table tr {
            display: table-row;
        }
        #pass:checked ~ table tr.fail, #pass:checked ~ table tr.skip {
            display: none;
        }
        #fail:checked ~ table tr.pass, #fail:checked ~ table tr.skip {
            display: none;
        }
        #skip:checked ~ table tr.pass, #skip:checked ~ table tr.fail {
            display: none;
        }
        pre{
            background-color: lightgray;
            padding: 10px;
            overflow: auto;
        }
    </style>
</head>
<body>
"""

END_INDEX = """
</body>
</html>
"""

# Function to generate the HTML content
def generate_html(data):
    html_content = f"""
    {START_INDEX}
    <h1>Test Results</h1>
    <input type="radio" id="all" name="show" checked/>
    <label for="all">All</label>
    <input type="radio" id="pass" name="show" />
    <label for="pass">Pass</label>
    <input type="radio" id="fail" name="show" />
    <label for="fail">Fail</label>
    <input type="radio" id="skip" name="show" />
    <label for="skip">Skip</label>
    <table>
        <thead>
            <tr>
                <th>Category</th>
                <th>Log File</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
"""

    for category, logs in data.items():
        for log_file, status in logs.items():
            status_class = status.lower()  # use status as class for styling
            name = f"<a href='{log_file}.html'>{log_file}</a>" if status != "PASS" else log_file
            html_content += f"""
            <tr class="{status_class}">
                <td>{category}</td>
                <td>
                    {name}
                </td>
                <td>{status}</td>
            </tr>
"""
    html_content += f"""
        </tbody>
    </table>
{END_INDEX}
"""
    return html_content


def decode_logs_file():
    results = {}
    for one_file in ["test-suite.log", "test-suite-root.log"]:
        with open(one_file, "rb") as f:
            lines = f.read()

        lines = lines.decode("utf-8", "ignore")
        for regex in [r"^SKIP: .*\n=*(.|\n)*?SKIP .*", r"^FAIL: .*\n=*(.|\n)*?FAIL .*"]:
            matches = re.finditer(regex, lines, re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                one_res = match.group()
                res = one_res.split("\n")
                test_file = res[-1].split(" ")[1]
                test_name = res[0].split("/")[-1]
                text = "\n".join(res)
                num = re.findall(r"failed:", text)
                results[f"{test_name}.log"] = (text, test_file, len(num))

    return results


def html_test_output(name, one_output):
    text_out, test_file, res = one_output
    res_print = res if res != 0 else ""
    txt = START_INDEX
    txt += f"<h2>{name} ({res_print} failed)</h2>\n"
    link = f"https://github.com/coreutils/coreutils/blob/master/{test_file}"
    txt += f"<a href='{link}' target='_blank'>test link: {test_file}</a>"
    txt += f"<pre>{text_out}</pre>"
    txt += END_INDEX
    output_path = Path(f"dist/{test_name}.html")
    output_path.write_text(txt)


if __name__ == "__main__":
    makedirs("dist", exist_ok=True)
    json_data = json.loads(Path("gnu-full-result.json").read_text())
    html_content = generate_html(json_data)

    # Write the HTML content to an index.html file
    output_path = Path("dist").joinpath("index.html")
    output_path.write_text(html_content)
    tables = decode_logs_file()
    for test_name, logs in tables.items():
        html_test_output(test_name, logs)
