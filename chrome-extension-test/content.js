// setTimeout(() => {

//   // const links = document.querySelectorAll(
//   //   '#main_pack > section > div.api_subject_bx > ul > li > div > div.detail_box > div.dsc_area > a'
//   // );

//   // links.forEach((link) => {
//   //      const rawHref = link.getAttribute('href'); // 실제 속성값 확인
//   // //  const url = link.href; // 자동 변환된 URL (있을 수도, 없을 수도 있음)
//   // // //  alert(rawHref);
//   //   chrome.runtime.sendMessage({ type: "CHECK_AD", url:rawHref }, (result) => {
//   //             alert(result.label);

//   //     if (result && result.label === '광고') {
//   //       //alert(result);
//   //       const target = link.parentElement?.parentElement?.parentElement;
//   //       if (target) {
//   //         target.style.backgroundColor = 'yellow';
//   //       }
//   //       else{
//   //           target.style.backgroundColor = 'blue';
//   //       }
//   //     }
//   //   });
//   // });

//     const link = "https://blog.naver.com/chemist_sun/223856739539";
//       chrome.runtime.sendMessage({ type: "CHECK_AD", url:link }, (result) => {
//       if (result && result.label === '광고') {
//         alert('결과값 : '+result);
//         const target = link.parentElement?.parentElement?.parentElement;
//         if (target) {
//           target.style.backgroundColor = 'yellow';
//         }
//         else{
//             target.style.backgroundColor = 'blue';
//         }
//       }
//     });
// }, 1000); // 1초 뒤 실행


console.log("content.js");
const elements = document.querySelectorAll(
  '#main_pack > section > div.api_subject_bx > ul > li > div > div.detail_box > div.dsc_area > a'
);

elements.forEach((element) => {

  const rawHref = element.getAttribute('href');
  chrome.runtime.sendMessage({ type: "CHECK_AD", url:rawHref }, (result) => {
    // 문제는 응답이 content.js에 도달하지 못하는 것
    console.log("response");
    //alert('결과값 : '+result.label);
    if (result && result.label === '광고') {//
      const target = element.parentElement?.parentElement?.parentElement;
      if (target) {
        target.style.backgroundColor = 'yellow';
      }
    }
    else{
      const target = element.parentElement?.parentElement?.parentElement;
      if (target) {
        target.style.backgroundColor = 'blue';
      }
    
    }
  });

});



// let element = document.querySelector("#main_pack > section > div.api_subject_bx > ul > li:nth-child(1) > div > div.detail_box > div.title_area > a");
// const rawHref = element.getAttribute('href'); // 실제 속성값 확인
// // const link = "https://blog.naver.com/chemist_sun/223856739539";

// chrome.runtime.sendMessage({ type: "CHECK_AD", url:rawHref }, (result) => {
//   // 문제는 응답이 content.js에 도달하지 못하는 것
//   console.log("response");
//   //alert('결과값 : '+result.label);
//   if (result && result.label === '광고') {//
//     const target = element.parentElement?.parentElement?.parentElement;
//     if (target) {
//       target.style.backgroundColor = 'yellow';
//     }
//   }
//   else{
//      const target = element.parentElement?.parentElement?.parentElement;
//     if (target) {
//       target.style.backgroundColor = 'blue';
//     }
  
//   }
// });

// let element = document.querySelector("#main_pack > section > div.api_subject_bx > ul > li:nth-child(1) > div");
// element.style.backgroundColor = 'red';
// alert('실행됨');

