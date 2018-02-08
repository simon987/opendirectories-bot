from flask import Flask, render_template, abort
import os
import ssl

app = Flask(__name__)


@app.route('/report/<report_id>/')
def report(report_id):
    if is_valid_id(report_id):
        return render_template("report.html", report_id=report_id)
    else:
        abort(400)


@app.route('/report/<report_id>/json_chart')
def report_json_chart(report_id):

    if is_valid_id(report_id):

        report_path = os.path.join("reports/", report_id + "_chart.json")
        return app.send_static_file(report_path)  # Todo: check for security issues

    else:
        abort(400)


@app.route('/report/<report_id>/json')
def report_json(report_id):

    if is_valid_id(report_id):

        report_path = os.path.join("reports/", report_id + ".json")
        return app.send_static_file(report_path)  # Todo: check for security issues

    else:
        abort(400)


@app.route('/report/<report_id>/links')
def report_links(report_id):

    if is_valid_id(report_id):

        report_path = os.path.join("reports/", report_id + ".txt")
        return app.send_static_file(report_path)  # Todo: check for security issues

    else:
        abort(400)


def is_valid_id(report_id: str):

    return report_id.isalnum() and len(report_id) == 6


if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.load_cert_chain('certificates/cert.crt', 'certificates/privkey.pem')
    app.run("0.0.0.0", ssl_context=context)