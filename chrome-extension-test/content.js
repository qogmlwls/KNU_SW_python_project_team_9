setTimeout(() => {
  const links = document.querySelectorAll(
    '#main_pack > section > div.api_subject_bx > ul > li > div > div.detail_box > div.dsc_area > a'
  );

  links.forEach((link) => {
       const rawHref = link.getAttribute('href'); // 실제 속성값 확인
  //  const url = link.href; // 자동 변환된 URL (있을 수도, 없을 수도 있음)
  // //  alert(rawHref);
    chrome.runtime.sendMessage({ type: "CHECK_AD", url:rawHref }, (result) => {
              alert(result.label);

      if (result && result.label === '광고') {
        //alert(result);
        const target = link.parentElement?.parentElement?.parentElement;
        if (target) {
          target.style.backgroundColor = 'yellow';
        }
        else{
            target.style.backgroundColor = 'blue';
        }
      }
    });
  });
}, 1000); // 1초 뒤 실행
