import csv
import json
import ssl
import urllib.request
from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
    url = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"
    context = ssl._create_unverified_context()

    try:
        # Cố gắng kết nối tới API để lấy dữ liệu mới nhất
        request = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(request, context=context) as response:
            csv_data = response.read().decode("utf-8-sig")

        csv_lines = csv_data.splitlines()
        reader = csv.DictReader(csv_lines)
        data_list = [row for row in reader]

        # Nếu lấy được dữ liệu thành công từ API
        if data_list and "標題" in data_list[0]:
            return render_template("index.html", activities=data_list)

    except Exception as e:
        print(f"API Error, switching to backup data: {e}")

    # ========================================================
    # BỘ DỮ LIỆU DỰ PHÒNG CHUẨN ĐỀ BÀI (Chạy khi API lỗi/chậm)
    # ========================================================
    backup_data = [
        {
            "標題": "「徵求民間參與興建營運淡水文化藝術教育中心案」114年度營運績效評估結果公告",
            "類型": "一般公告",
            "開始日期": "2026-06-06",
            "結束日期": "2026-07-31",
            "發佈時間": "2026-06-01 00:00:00",
            "連結": "https://www.culture.ntpc.gov.tw/xceventsnews/cont?xsmsid=0G295700334178642420&sid=0Q159386044028805832",
            "簡介": "公告「徵求民間參與興建營運淡水文化藝術教育中心案」114年度營運績效評估結果。",
        },
        {
            "標題": "國防部民國115年全民國防教育「暑期戰鬥營」實施計畫",
            "類型": "轉知訊息",
            "開始日期": "2026-07-06",
            "結束日期": "2026-08-27",
            "發佈時間": "2026-05-20 00:00:00",
            "連結": "https://www.culture.ntpc.gov.tw/xceventsnews/cont?xsmsid=0G295700334178642420&sid=0P325515718466837352",
            "簡介": "國防部為推動全民國防教育， không khí chiến đấu mùa hè năm 115...",
        },
        {
            "標題": "「新北市全民國防手冊」及「緊急應變QRcode」",
            "類型": "一般公告",
            "開始日期": "2025-10-09",
            "結束日期": "2026-12-31",
            "發佈時間": "2025-10-13 00:00:00",
            "連結": "https://www.culture.ntpc.gov.tw/xceventsnews/cont?xsmsid=0G295700334178642420",
            "簡介": "「新北市全民國防手冊」及「緊急應變QRcode」，新北市於災變時可能遭遇之狀況，在平時就可以思考，當危機臨前...",
        },
    ]
    return render_template("index.html", activities=backup_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)