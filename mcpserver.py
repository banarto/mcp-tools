import os
import requests 
from mcp.server import MCPServer
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
openwheathermap_api_key = os.getenv("OPENWHEATHERMAP_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

permitted_path = Path(__file__).parent / "permit_folder"

tavily_headers = {
    "Content-Type":"application/json",
    "Authorization":"Bearer " + tavily_api_key
}

mcp = MCPServer("mcp-tools")

@mcp.tool()
def clock() -> str:
    """現在時刻を取得するツール"""
    return f"現在の時刻：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@mcp.tool()
def get_wheather(zip_place: str) -> str:
    """郵便番号,国（例 100-0001,JP）から現在の天気を取得するツール"""
    url = "https://api.openweathermap.org/data/2.5/weather?zip={zip_place}&units=metric&appid={API_key}"
    url = url.format(zip_place=zip_place, API_key=openwheathermap_api_key)
    w = requests.get(url)
    if w.status_code == 200:
        return w.json()["weather"][0]["main"]
    else:
        return "天気の取得に失敗しました。"

@mcp.tool()
def read_file(path: str) -> str:
    """ファイルの中身を見るツール"""
    path = permitted_path / path
    if path.resolve().is_relative_to(permitted_path):
        try:
            with open(path, encoding="UTF-8") as f:
                s = f.read()
                return s
        except FileNotFoundError:
            return "ファイルが見つかりませんでした"
        except Exception as e:
            return f"予想外のエラーが発生しました: {e}"
    else:
        return "許可されていないファイルです"

@mcp.tool()
def web_search(word: str) -> str:
    """WEB検索するツール"""
    search_result = requests.post("https://api.tavily.com/search",headers=tavily_headers,json={"query":word})
    if search_result.status_code == 200:
        json_result = search_result.json()
        organized_result = ""
        for i in range(min(3,len(json_result["results"]))):
            organized_result += f"{i+1}件目の検索結果\nタイトル:{json_result["results"][i]["title"]}\n内容：{json_result["results"][i]["content"]}\n"
        return organized_result
    else:
        return "検索に失敗しました"

if __name__ == "__main__":
    mcp.run()