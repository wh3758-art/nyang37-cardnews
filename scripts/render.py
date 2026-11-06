"""cards/<날짜>/01.html ~ 06.html 을 1080x1350 JPG 로 바꿔 images/<날짜>/ 에 저장합니다.

사용법: python scripts/render.py 2026-11-06
(날짜를 빼면 cards/ 안에서 가장 최근 날짜를 씁니다)
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
W, H = 1080, 1350


def latest_date() -> str:
    dates = sorted(p.name for p in (ROOT / "cards").iterdir() if p.is_dir())
    if not dates:
        sys.exit("cards/ 폴더에 날짜 폴더가 없습니다.")
    return dates[-1]


def main() -> None:
    date = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else latest_date()
    src = ROOT / "cards" / date
    out = ROOT / "images" / date
    pages = sorted(src.glob("[0-9][0-9].html"))
    if not 2 <= len(pages) <= 10:
        sys.exit(f"{src} 에 카드가 {len(pages)}장 있습니다. 캐러셀은 2~10장이어야 합니다.")
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for html in pages:
            page.goto(html.resolve().as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            target = out / (html.stem + ".jpg")
            # 인스타그램 게시 API 는 JPEG 만 받습니다.
            page.screenshot(path=str(target), type="jpeg", quality=92,
                            clip={"x": 0, "y": 0, "width": W, "height": H})
            print("저장:", target.relative_to(ROOT))
        browser.close()

    print(f"DATE={date}")


if __name__ == "__main__":
    main()
