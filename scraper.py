from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def fetch_price(url: str, timeout_ms: int = 15000, retries: int = 2) -> int | None:
    for attempt in range(retries + 1):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
                context = browser.new_context(user_agent="Mozilla/5.0 (compatible; PriceWatcher/1.0)")
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
                # ページ安定待ち（軽め）
                page.wait_for_load_state("networkidle", timeout=timeout_ms)
                # 価格要素（CSSセレクタは予備も用意）
                selector_candidates = [".price__current", "[data-test=price-current]", ".product-price"]
                price_text = None
                for sel in selector_candidates:
                    el = page.query_selector(sel)
                    if el:
                        price_text = el.inner_text().strip()
                        break
                browser.close()

                if not price_text:
                    return None
                digits = "".join(ch for ch in price_text if ch.isdigit())
                return int(digits) if digits else None

        except PlaywrightTimeoutError:
            if attempt == retries:
                return None
        except Exception:
            if attempt == retries:
                return None
    return None
