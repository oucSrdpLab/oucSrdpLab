dycalendar.draw()

var dycalendar = {
  showReservedTime: function() {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({op: 2})
  };

  const now = new Date().getTime();

  fetch('http://192.168.15.135:5000/database/orders', requestOptions)
    .then(response => response.json())
    .then(data => {
      const reservedTime = data
        .filter(order => Number(order.untilTime) > now && (order.orderStatus === "1"||order.orderStatus === "已签到"))
        .map(order => ({
          _id: order._id,
          startTime: new Date(Number(order.startTime)).toLocaleString(),
          endTime: new Date(Number(order.untilTime)).toLocaleString(),
          applicantName: order.applicantName,
          applicantIDNumber: order.applicantIDNumber
        }));
      const timeList = document.querySelector('#reserved-time');
      const tr = document.createElement('tr');
      const img = document.createElement('img');
      img.src = 'static/image/pro_img.png';
      tr.innerHTML = `
        <td>
          <table>
            <tbody>
              ${reservedTime.map(start => `
                <tr>
                  <td>${start.startTime} - ${start.endTime}</td>
                  
                </tr>
                <tr><td>姓名：${start.applicantName}学号：${start.applicantIDNumber}</td></tr>
              `).join('')}
            </tbody>
          </table>
        </td>
        <td><button type="button" onclick="handleSignIn(2)">签到</button></td>
      `;
      timeList.appendChild(tr);
    })
    .catch(error => console.error(error));
},



  init: function() {
    window.onload = function() {
      dycalendar.showReservedTime();
    };
  }
};

// document.addEventListener('DOMContentLoaded', function() {
//   const btnSignIn = document.querySelector('button[type="button"]');
//
//   btnSignIn.addEventListener('click', function() {
//     handleSignIn(2);
//   });
// });
//
// function handleSignIn(itemId) {
//   const requestOptions = {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ id: 3, op: 4 ,orderStatus:"已签到"})
//   };
//
//   fetch('http://192.168.15.135:5000/database/orders', requestOptions)
//     .then(response => response.json())
//     .then(data => {
//       console.log('签到成功', data);
//       // 如果需要刷新预订列表可在此处调用 showReservedTime 函数进行刷新。
//       const signInButton = document.querySelector(`button[onclick="handleSignIn('${itemId}')"`);
//       signInButton.textContent = '已签到';
//     })
//     .catch(error => console.error(error));
// }

dycalendar.init();
