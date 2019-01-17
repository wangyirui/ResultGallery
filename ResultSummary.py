import os
import json
from PIL import Image
import PIL

class ResultSummary(object):
    def __init__(self):
        self.cwd = os.getcwd()
        self.result_folder = self.cwd + '/ResultSummary'
        self.img_folder = self.result_folder + '/imgs'
        self.field_names = []
        self.result_container = []

        if not os.path.exists(self.result_folder):
            os.makedirs(self.result_folder)

        if not os.path.exists(self.img_folder):
            os.makedirs(self.img_folder)

    def add_result(self, img_name, fields):
        json_dict = {img_name: fields}
        for field_name, val in fields.items():
            if isinstance(val, PIL.Image.Image):
                img_path = self.img_folder + '/' + img_name
                val.save(img_path)
                json_dict[img_name][field_name] = './imgs/' + img_name
            if field_name not in self.field_names:
                self.field_names.append(field_name)
        json_output = json.dumps(json_dict)
        self.result_container.append(json_dict)
        with open(self.result_folder + '/summary.txt', 'a') as f:
            f.write(json_output)
            f.write('\n')

    def write_html(self):
        assert self.result_container != []
        html_str = "<!DOCTYPE html>\n" \
                   "<html>\n" \
                   "<link rel=\"stylesheet\" type=\"text/css\" href=\"https://cdn.datatables.net/1.10.19/css/jquery.dataTables.css\">\n" \
                   "<head>\n" \
                   "<script type=\"text/javascript\" charset=\"utf8\" src=\"https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.3.1.min.js\"></script>\n" \
                   "<script type=\"text/javascript\" charset=\"utf8\" src=\"https://cdn.datatables.net/1.10.19/js/jquery.dataTables.js\"></script>\n" \
                   "<script>\n" \
                   "$(document).ready(function() {\n" \
                   "    $('#example').DataTable();\n" \
                   "} );\n" \
                   "</script>\n" \
                   "</head>\n" \
                   "<body>\n" \
                   "<table id = \"example\" class =\"display\" style=\"width:100%\">\n"

        html_str = self._write_table_head(html_str, self.field_names)

        html_str = self._write_table_body(html_str, self.result_container)

        html_str = self._write_table_end(html_str, self.field_names)

        with open(self.result_folder + "/result.html", 'w') as f:
            f.writelines(html_str)


    def _write_table_head(self, html_str, items):
        html_str += "\t<thead>\n"
        html_str += "\t\t<tr>\n"

        for name in items:
            html_str += f"\t\t\t<th>{name}</th>\n"

        html_str += "\t\t</tr>\n"
        html_str += "\t</thead>\n"

        return html_str

    def _write_table_body(self, html_str, result_list):
        html_str += "\t<tbody>\n"

        for record in result_list:
            html_str += "\t\t<tr>\n"
            for img_name, results in record.items():
                for field, val in results.items():
                    if os.path.isfile(self.result_folder + str(val)[1:]): # an image path
                        html_str += "\t\t\t<td>\n"
                        html_str += f"\t\t\t\t<a href=\"./imgs/{img_name}\" target=\"_blank\">\n"
                        html_str += f"\t\t\t\t\t<img style=\"display:block;\" width=\"64\" height=\"64\" src=\"./imgs/{img_name}\" align=\"center\"/>\n"
                        html_str += "\t\t\t\t</a>\n"
                        html_str += "\t\t\t</td>\n"
                    else:
                        html_str += f"\t\t\t<td>{val}</td>\n"

            html_str += "\t\t</tr>\n"

        html_str += "\t</tbody>\n"

        return html_str


    def _write_table_end(self, html_str, items):
        html_str += "\t<tfoot>\n"
        html_str += "\t\t<tr>\n"

        for name in items:
            html_str += f"\t\t<th>{name}</th>\n"

        html_str += "\t\t</tr>\n"
        html_str += "\t</tfoot>\n"

        html_str += "</table>\n\n"

        html_str += "</body>\n"
        html_str += "</html>"

        return html_str
