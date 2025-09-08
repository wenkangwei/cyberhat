import asyncio
from playwright.async_api import async_playwright
import json




async def scrape_with_playwright(wechat_url, output_file):
    """使用Playwright直接爬取"""
    try:
        print("启动Playwright...")
        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
            
            # 创建页面
            page = await browser.new_page()
            
            # 设置用户代理
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            # 导航到页面
            # wechat_url = "https://mp.weixin.qq.com/s/OMtb1DL_ik2TvENzWHWGsg"
            # wechat_url= "https://zhuanlan.zhihu.com/p/1901422655787230018"
            print(f"导航到: {wechat_url}")
            await page.goto(wechat_url, wait_until='networkidle')
            
            # 等待页面加载
            await page.wait_for_timeout(5000)
            
            # 提取文章内容
            print("提取内容...")
            article_data = await page.evaluate("""() => {
                const selectors = [
                    '#js_content',
                    '.rich_media_content', 
                    '.article-content',
                    'article'
                ];
                
                let contentElement = null;
                for (const selector of selectors) {
                    contentElement = document.querySelector(selector);
                    if (contentElement) break;
                }
                
                if (!contentElement) {
                    contentElement = document.body;
                }
                
                return {
                    title: document.title,
                    url: window.location.href,
                    content: contentElement.innerText.trim(),
                    html: contentElement.innerHTML,
                    success: true
                };
            }""")
            
            print("关闭浏览器...")
            await browser.close()
            
            print("抓取成功!")
            print(f"标题: {article_data['title']}")
            print(f"内容长度: {len(article_data['content'])} 字符")
            print(f"内容预览: {article_data['content'][:]}...")
            
            # 保存结果
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(article_data, f, ensure_ascii=False, indent=2)
            
            return article_data
            
    except Exception as e:
        print(f"Playwright错误: {e}")
        return None


async def webpage_crawler(url, output_file="", mode="wechat"):
    res = None
    if mode == "wechat":
        # res = asyncio.run(scrape_with_playwright(url, output_file))
         res = await scrape_with_playwright(url, output_file)
    else:
        raise ValueError(f"mode={mode} is not supported yet.")
    return res



# def webpage_crawler(url, output_file="", mode="wechat"):
#     """网页爬取函数 - 修复版本"""
#     res = None
#     try:
#         if mode == "wechat":
#             # 安全地运行异步函数
#             res = run_async_safely(scrape_with_playwright, url, output_file)
#         else:
#             raise ValueError(f"mode={mode} is not supported yet.")
#         return res
#     except Exception as e:
#         print(f"爬取过程中出错: {e}")
#         return None

def run_async_safely(async_func, *args, **kwargs):
    """
    安全地运行异步函数，避免事件循环冲突
    
    Args:
        async_func: 异步函数
        *args: 位置参数
        **kwargs: 关键字参数
        
    Returns:
        异步函数的结果
    """
    try:
        # 尝试获取当前事件循环
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # 没有事件循环，创建新的并运行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(async_func(*args, **kwargs))
        finally:
            loop.close()
    else:
        # 检查事件循环是否已经在运行
        if loop.is_running():
            # 如果已经在运行，我们需要特殊处理
            # 这里我们创建一个新的事件循环来运行
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                return new_loop.run_until_complete(async_func(*args, **kwargs))
            finally:
                new_loop.close()
        else:
            # 事件循环存在但没有运行，直接运行
            return loop.run_until_complete(async_func(*args, **kwargs))


# 安装Playwright: pip install playwright && playwright install chromium
if __name__ == "__main__":
    asyncio.run(scrape_with_playwright("https://mp.weixin.qq.com/s/OMtb1DL_ik2TvENzWHWGsg", 'wechat_article_playwright.json'))