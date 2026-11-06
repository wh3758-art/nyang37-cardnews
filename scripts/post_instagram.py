"""images/<날짜>/*.jpg 를 인스타그램 캐러셀로 게시합니다.

필요한 GitHub Secrets
  IG_USER_ID       인스타그램 비즈니스/크리에이터 계정 ID (숫자)
  IG_ACCESS_TOKEN  게시 권한이 있는 페이스북 페이지 액세스 토큰

이미지는 공개 저장소의 raw 주소에서 인스타그램이 직접 가져갑니다.
사용법: python scripts/post_instagram.py 2026-11-06 <커밋 SHA>
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH = f"https://graph.facebook.com/{os.environ.get('GRAPH_VERSION', 'v27.0')}"


def call(method: str, path: str, **params) -> dict:
    params["access_token"] = os.environ["IG_ACCESS_TOKEN"]
    data = urllib.parse.urlencode(params).encode()
    if method == "GET":
        req = urllib.request.Request(f"{GRAPH}/{path}?{data.decode()}")
    else:
        req = urllib.request.Request(f"{GRAPH}/{path}", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"인스타그램 API 오류 ({path}): {e.read().decode()}")


def wait_ready(container_id: str) -> None:
    for _ in range(30):
        status = call("GET", container_id, fields="status_code").get("status_code")
        if status == "FINISHED":
            return
        if status in ("ERROR", "EXPIRED"):
            sys.exit(f"컨테이너 {container_id} 처리 실패: {status}")
        time.sleep(5)
    sys.exit(f"컨테이너 {container_id} 처리 시간이 초과됐습니다.")


def main() -> None:
    date, sha = sys.argv[1], sys.argv[2]
    repo = os.environ["GITHUB_REPOSITORY"]  # 예: wh3758-art/nyang37-cardnews
    ig = os.environ["IG_USER_ID"]

    images = sorted((ROOT / "images" / date).glob("*.jpg"))
    if not 2 <= len(images) <= 10:
        sys.exit(f"images/{date} 에 이미지가 {len(images)}장 있습니다.")
    caption_file = ROOT / "cards" / date / "caption.txt"
    caption = caption_file.read_text(encoding="utf-8").strip() if caption_file.exists() else ""

    children = []
    for img in images:
        url = f"https://raw.githubusercontent.com/{repo}/{sha}/images/{date}/{img.name}"
        item = call("POST", f"{ig}/media", image_url=url, is_carousel_item="true")
        print("이미지 등록:", img.name, item["id"])
        children.append(item["id"])
    for cid in children:
        wait_ready(cid)

    carousel = call("POST", f"{ig}/media", media_type="CAROUSEL",
                    children=",".join(children), caption=caption)
    wait_ready(carousel["id"])
    published = call("POST", f"{ig}/media_publish", creation_id=carousel["id"])
    print("게시 완료! 미디어 ID:", published["id"])


if __name__ == "__main__":
    main()
