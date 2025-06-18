console.log("content.js");

const elements = document.querySelectorAll(
  '#main_pack > section > div.api_subject_bx > ul > li > div > div.detail_box > div.dsc_area > a'
);

elements.forEach((element) => {
  const rawHref = element.getAttribute('href');

  chrome.runtime.sendMessage({ type: "CHECK_AD", url: rawHref }, (result) => {
    console.log("response");

    if (!result || result.error) return;

    console.log("keyword list : ", result.keywordlist);

    const target = element.parentElement?.parentElement?.parentElement;
    if (target) {
      target.style.backgroundColor = result.label === '광고' ? 'yellow' : 'blue';
    }

    // 팝업용 div 생성
    const popup = document.createElement('div');
    popup.style.position = 'fixed'; // <- fixed로 설정
    popup.style.backgroundColor = 'white';
    popup.style.border = '1px solid gray';
    popup.style.padding = '5px';
    popup.style.fontSize = '12px';
    popup.style.zIndex = '1000';
    popup.style.display = 'none';
    popup.style.whiteSpace = 'pre-line';

    popup.textContent = `키워드 포함:\n${result.keywordlist.join('\n')}`;
    document.body.appendChild(popup);

    let popupTimeout;

    element.addEventListener('mouseenter', (e) => {
      popup.style.left = e.clientX + 10 + 'px';
      popup.style.top = e.clientY + 10 + 'px';
      popup.style.display = 'block';
    });

    element.addEventListener('mouseleave', () => {
      popupTimeout = setTimeout(() => {
        popup.style.display = 'none';
      }, 100); // 살짝 지연시켜 팝업 내부 진입 허용
    });

    popup.addEventListener('mouseenter', () => {
      clearTimeout(popupTimeout); // 팝업 안에 있을 땐 안 사라짐
    });

    popup.addEventListener('mouseleave', () => {
      popup.style.display = 'none';
    });
  });
});


// console.log("content.js");
// const elements = document.querySelectorAll(
//   '#main_pack > section > div.api_subject_bx > ul > li > div > div.detail_box > div.dsc_area > a'
// );

// elements.forEach((element) => {

//   const rawHref = element.getAttribute('href');
//   chrome.runtime.sendMessage({ type: "CHECK_AD", url:rawHref }, (result) => {
//     // 문제는 응답이 content.js에 도달하지 못하는 것
//     console.log("response");
//     //alert('결과값 : '+result.label);
//     // let keyword_list = ['협찬','협찬을 제공받아','원고료'];
//     console.log("keyword list : "+result.keywordlist);
//     if (result && result.label === '광고') {//
//       const target = element.parentElement?.parentElement?.parentElement;
//       if (target) {
//         target.style.backgroundColor = 'yellow';
//       }
//     }
//     else{
//       const target = element.parentElement?.parentElement?.parentElement;
//       if (target) {
//         target.style.backgroundColor = 'blue';
//       }
    
//     }
//   });

// });

