var now = new Date();

var dycalendar = {
  showReservedTime: function() {
    // 清空原先的tr
    const timeList = document.querySelector('#reserved-time');
    timeList.innerHTML = '';

    //const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const endOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59);

    // 格式化日期时间为 "YYYY-MM-DD HH:mm:ss" 格式
    function formatDateTime(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');

      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }

    function formatDateTime1(dateString) {
        const dateTimeParts = dateString.split(' ');
        const datePart = dateTimeParts[0];
        const timePart = dateTimeParts[1].split(':');

        const [year, month, day] = datePart.split('/');
        const hours = String(timePart[0]).padStart(2, '0');
        const minutes = String(timePart[1]).padStart(2, '0');

        return `${month}-${day} ${hours}:${minutes}`;
    }


    const requestBody = {
      start_time: formatDateTime(today),
      end_time: formatDateTime(endOfDay)
    };

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    };

    fetch('http://192.168.15.135:5000/appointment/all', requestOptions)
      .then(response => response.json())
      .then(data => {
        const reservedTime = data.data
          .filter(order => new Date(order.end_time) <= endOfDay )
          .map(order => ({
            start_time: new Date(order.start_time).toLocaleString(),
            end_time: new Date(order.end_time).toLocaleString(),
            equipment_name: order.equipment_name,
            appointment_id:order.id,
            is_sign:order.is_sign,
            is_checked:order.is_checked,
            applicant_student_id:order.applicant_student_id,
          }));
        const timeList = document.querySelector('#reserved-time');

        reservedTime.forEach(order => {
            const tr = document.createElement('tr');
            const equipmentNameTd = document.createElement('td');
            equipmentNameTd.textContent = order.equipment_name;
            tr.appendChild(equipmentNameTd);

            const applicantStudentIdTd = document.createElement('td');
            applicantStudentIdTd.textContent = order.applicant_student_id;
            tr.appendChild(applicantStudentIdTd);

            const startTimeTd = document.createElement('td');
            startTimeTd.textContent = formatDateTime1(order.start_time);
            tr.appendChild(startTimeTd);

            const endTimeTd = document.createElement('td');
            endTimeTd.textContent = formatDateTime1(order.end_time);
            tr.appendChild(endTimeTd);

            const signInTd = document.createElement('td');
            const signInButton = document.createElement('button');
            if (order.is_sign) { // 如果已签到
                signInButton.textContent = '已签到';
                signInButton.disabled = true; // 禁用点击事件
            } else if(order.is_checked){
                signInButton.textContent = '签到';
                signInButton.setAttribute('data-appointment-id', order.appointment_id);
                signInButton.addEventListener('click', () => {
                    // 处理签到逻辑
                   dycalendar.handleSignIn(order); // 修改这里
                });
            }else{
                signInButton.textContent = '未审核';
                signInButton.disabled = true; // 禁用点击事件
            }
            signInTd.appendChild(signInButton);
            tr.appendChild(signInTd);

            timeList.appendChild(tr);
        });


      })
      .catch(error => console.error(error));
  },

      handleSignIn: function(order) {
        const requestBody = {
          appointment_id: order.appointment_id
        };

        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(requestBody)
        };

        fetch('http://192.168.15.135:5000/sign/signature', requestOptions)
          .then(response => response.json())
          .then(data => {
            console.log(data);
            location.reload();
            alert(`签到成功！`);
          })
          .catch(error => console.error(error));
      },

  init: function() {
    window.print = () => {};
    window.onload = function() {
      dycalendar.showReservedTime();
    };
    // 每隔5分钟刷新一次
    setInterval(function() {
        dycalendar.showReservedTime();
    }, 5 * 60 * 1000);
  }
};

dycalendar.init();
