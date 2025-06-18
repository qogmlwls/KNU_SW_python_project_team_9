chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "CHECK_AD") {
    
    console.log("message.url : " + message.url);

    fetch(`http://49.247.175.145/check_blog?url=${message.url}`)
      .then(res => res.text())
      .then(text => {
        console.log("결과값 : " + text);
        const cleanArray = JSON.parse(text);
        const cleanLabel = cleanArray[0];
        console.log("cleanLabel : " + cleanLabel);
        sendResponse({ label: cleanLabel });
        console.log("sendResponse 전송함");
      })
      .catch(err => {
        console.error("API 호출 실패:", err);
        sendResponse({ label: err.message + ' url: ' + message.url, error: true });
      });

     // sendResponse({ label: "일반" });

    // (async () => {

    //   console.log("?");

    //   try {
    //     console.log("매개변수값 : "+message.url);

    //     const res = await fetch(`http://49.247.175.145/check_blog?url=${message.url}`);
        
    //     console.log("fetch 실행");
    //     const text = await res.text();
    //     console.log("결과값 : " + text);

    //      const cleanArray = JSON.parse(text);  // ["일반"]
    //     const cleanLabel = cleanArray[0];     // "일반"
    //     console.log("cleanLabel : " + cleanLabel);

    //    // const cleanLabel = text.replace(/[{}]/g, '').trim();  // → "광고" 또는 "일반"
    //     sendResponse({ label: cleanLabel });
      

    //   } catch (err) {
    //     console.error("API 호출 실패:", err);
    //     sendResponse({ label: err.message + 'url'+message.url, error: true });
    //   }
    // })();

    // ✅ 비동기 응답 유지
    return true;
  }
});
