chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "CHECK_AD") {
    (async () => {
      try {
        const res = await fetch(`http://49.247.175.145/check_blog?url=${message.url}`);
       const text = await res.text();
        const cleanLabel = text.replace(/[{}]/g, '').trim();  // → "광고" 또는 "일반"
        sendResponse({ label: cleanLabel });

      } catch (err) {
        console.error("API 호출 실패:", err);
        sendResponse({ label: err.message + 'url'+message.url, error: true });
      }
    })();

    // ✅ 비동기 응답 유지
    return true;
  }
});
